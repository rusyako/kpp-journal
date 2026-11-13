"""ISAPI-клиент: HTTP Digest (FRT §4.1, с.10), белый список операций.

Разрешено:
  * GET — чтение (только в READ_ONLY/PILOT или для виртуального терминала);
  * POST /ISAPI/AccessControl/AcsEvent — поиск в журнале (R*, данные не меняет; FRT §14.6.1.5, с.396–399);
  * PUT  /ISAPI/AccessControl/remoteCheck — ответ на ожидающий запрос удалённой проверки
    (FRT §14.6.15.2, с.520–521), только если settings.control_allowed(device).
  * POST /ISAPI/AccessControl/UserInfo/Search — только одна запись из списка пилота (EmployeeNoList, maxResults=1);
  * PUT  /ISAPI/AccessControl/UserInfo/Modify — только {"employeeNo", "userType"∈normal|visitor} записи из списка пилота,
    только если settings.user_write_allowed(device).
Всё остальное (RemoteControl/door, AcsCfg, httpHosts, прочие UserInfo, FDLib, CardInfo, права, расписания…) —
ForbiddenOperation. Конфигурацию терминала (AcsCfg, httpHosts) клиент менять не умеет.

После неудачной Digest-аутентификации (итоговый 401) клиент блокируется и больше не шлёт запросов:
терминал блокирует учётную запись после 5 ошибок на 30 минут (AUTHENTICATION.md §3).
"""

import logging
import os
import re
import time
from dataclasses import dataclass

import httpx

from app.integrations.hikvision.parsing import parse_xml
from app.integrations.hikvision.settings import HikSettings

log = logging.getLogger("hikvision.client")

_READ_POSTS = (re.compile(r"^/ISAPI/AccessControl/AcsEvent$"),)
_CONTROL_PUTS = (re.compile(r"^/ISAPI/AccessControl/remoteCheck$"),)
# Явный запрет для любых изменяющих методов — на случай ошибки в белом списке
_NEVER = re.compile(
    r"RemoteControl|/AcsCfg$|/httpHosts|/UserInfo/(SetUp|Modify|Record)|UserInfoDetail|/FDLib/(FaceDataRecord|FDSetUp|FDModify)"
    r"|FDSearch/Delete|/CardInfo/(SetUp|Modify|Record|Delete)|/UserRight|DoorStatusWeekPlanCfg|/Door/param/\d+$"
    r"|/System/(reboot|factoryReset|updateFirmware)|/Security/users",
    re.I,
)


class IsapiError(Exception):
    pass


class ForbiddenOperation(IsapiError):
    pass


class NetworkDisabled(IsapiError):
    pass


class AuthLockout(IsapiError):
    """Терминал отклонил Digest. Дальнейшие запросы этим клиентом запрещены."""


@dataclass
class IsapiResponse:
    method: str
    path: str
    status: int
    data: dict | str | None
    latency_ms: int

    @property
    def ok(self) -> bool:
        return self.status == 200


def credentials_for(device) -> tuple[str, str] | None:
    """HIK_<credentials_env>_USER / _PASSWORD. В БД и логах паролей нет."""
    if not device.credentials_env:
        return None
    prefix = f"HIK_{device.credentials_env.upper()}"
    user, password = os.environ.get(f"{prefix}_USER"), os.environ.get(f"{prefix}_PASSWORD")
    return (user, password) if user and password else None


_USER_SEARCH = re.compile(r"^/ISAPI/AccessControl/UserInfo/Search$")
_USER_MODIFY = re.compile(r"^/ISAPI/AccessControl/UserInfo/Modify$")
USER_TYPES = ("normal", "visitor")


def _check_user_search(body, settings: HikSettings) -> None:
    """Поиск только ОДНОЙ записи пилота по EmployeeNoList — не выгрузка списка (в ответе были бы ФИО всех)."""
    try:
        cond = body["UserInfoSearchCond"]
        emp_list = cond["EmployeeNoList"]
        assert isinstance(emp_list, list) and len(emp_list) == 1
        emp = str(emp_list[0]["employeeNo"])
        assert int(cond.get("maxResults", 0)) == 1
    except (KeyError, TypeError, ValueError, AssertionError):
        raise ForbiddenOperation("UserInfo/Search: разрешён только поиск одной записи по EmployeeNoList") from None
    if emp not in settings.pilot_employee_nos:
        raise ForbiddenOperation(f"UserInfo/Search: employeeNo {emp} не в списке пилота")


def _check_user_modify(body, settings: HikSettings, device) -> None:
    """Изменение ТОЛЬКО userType ОДНОЙ записи пилота. Другие поля отправлять нельзя."""
    if not settings.user_write_allowed(device):
        raise ForbiddenOperation(f"UserInfo/Modify: запись запрещена в режиме {settings.mode} для «{getattr(device, 'key', '?')}»")
    info = body.get("UserInfo") if isinstance(body, dict) and set(body) == {"UserInfo"} else None
    if not isinstance(info, dict) or set(info) != {"employeeNo", "userType"}:
        raise ForbiddenOperation("UserInfo/Modify: допустимы только поля employeeNo и userType")
    if str(info["employeeNo"]) not in settings.pilot_employee_nos:
        raise ForbiddenOperation(f"UserInfo/Modify: employeeNo {info['employeeNo']} не в списке пилота")
    if info["userType"] not in USER_TYPES:
        raise ForbiddenOperation("UserInfo/Modify: userType только normal или visitor")


def check_operation(method: str, path: str, settings: HikSettings, device, body=None) -> None:
    """Поднимает ForbiddenOperation, если операция не в белом списке для текущего режима."""
    method = method.upper()
    bare = path.split("?", 1)[0]
    if method == "POST" and _USER_SEARCH.match(bare):
        _check_user_search(body, settings)
        return
    if method == "PUT" and _USER_MODIFY.match(bare):
        _check_user_modify(body, settings, device)
        return
    if method == "PUT" and any(p.match(bare) for p in _CONTROL_PUTS):
        if not settings.control_allowed(device):
            raise ForbiddenOperation(f"PUT {bare}: управление запрещено в режиме {settings.mode} для «{device.key}»")
        return
    if method == "GET":
        if "alertStream" in bare:
            raise ForbiddenOperation("постоянное соединение alertStream клиентом не открывается")
        return
    if _NEVER.search(bare):
        raise ForbiddenOperation(f"{method} {bare}: операция запрещена адаптеру")
    if method == "POST" and any(p.match(bare) for p in _READ_POSTS):
        return
    raise ForbiddenOperation(f"{method} {bare}: нет в белом списке")


class IsapiClient:
    def __init__(self, device, settings: HikSettings, *, transport: httpx.BaseTransport | None = None,
                 credentials: tuple[str, str] | None = None):
        self.device = device
        self.settings = settings
        self.locked = False
        if device.simulated:
            if transport is None:
                raise NetworkDisabled("виртуальному терминалу нужен mock-транспорт")
        elif transport is None and not settings.network_allowed():
            raise NetworkDisabled(f"режим {settings.mode}: сетевые запросы к реальным терминалам выключены")
        creds = credentials or credentials_for(device)
        if creds is None:
            raise IsapiError(f"нет учётных данных для «{device.key}» (HIK_{(device.credentials_env or '?').upper()}_USER/_PASSWORD)")
        base = f"{device.scheme}://{device.host}:{device.port}" if device.host else "http://mock-device"
        self._http = httpx.Client(
            base_url=base,
            auth=httpx.DigestAuth(*creds),
            transport=transport,
            timeout=httpx.Timeout(settings.http_timeout_s, connect=min(5.0, settings.http_timeout_s)),
            headers={"Accept": "application/json, application/xml"},
            follow_redirects=False,
        )

    def close(self) -> None:
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def request(self, method: str, path: str, *, json: dict | None = None) -> IsapiResponse:
        if self.locked:
            raise AuthLockout("клиент заблокирован после отказа в аутентификации")
        check_operation(method, path, self.settings, self.device, json)
        t0 = time.perf_counter()
        try:
            r = self._http.request(method, path, json=json)
        except httpx.TimeoutException as e:
            raise IsapiError(f"таймаут {method} {path.split('?')[0]}") from e
        except httpx.HTTPError as e:
            raise IsapiError(f"сеть: {type(e).__name__}") from e
        latency = int((time.perf_counter() - t0) * 1000)
        if r.status_code == 401:
            # httpx уже сделал одно Digest-рукопожатие; повторять нельзя
            self.locked = True
            log.warning("ISAPI 401 от «%s» на %s %s — запросы остановлены", self.device.key, method, path.split("?")[0])
            raise AuthLockout("терминал отклонил логин/пароль (401); повторных попыток не делаем")
        data: dict | str | None = None
        ct = r.headers.get("content-type", "").lower()
        if r.content:
            if "json" in ct:
                try:
                    data = r.json()
                except ValueError:
                    data = r.text[:2000]
            elif "xml" in ct or r.content.lstrip().startswith(b"<"):
                try:
                    data = parse_xml(r.content)
                except ValueError:
                    data = r.text[:2000]
            else:
                data = r.text[:2000]
        log.info("ISAPI %s %s → %s (%d мс)", method, path.split("?")[0], r.status_code, latency)
        return IsapiResponse(method, path, r.status_code, data, latency)

    # ---------- Чтение ----------

    def device_info(self) -> IsapiResponse:
        return self.request("GET", "/ISAPI/System/deviceInfo")

    def access_capabilities(self) -> IsapiResponse:
        return self.request("GET", "/ISAPI/AccessControl/capabilities")

    def acs_cfg_capabilities(self) -> IsapiResponse:
        return self.request("GET", "/ISAPI/AccessControl/AcsCfg/capabilities?format=json")

    def acs_cfg(self) -> IsapiResponse:
        return self.request("GET", "/ISAPI/AccessControl/AcsCfg?format=json")

    def remote_check_capabilities(self) -> IsapiResponse:
        return self.request("GET", "/ISAPI/AccessControl/remoteCheck/capabilities?format=json")

    def search_events(self, employee_no: str, start: str, end: str, max_results: int = 30) -> IsapiResponse:
        """Поиск в журнале одного человека, без фото [FRT §14.6.1.5, с.396–397]."""
        body = {
            "AcsEventCond": {
                "searchID": f"kpp-{int(time.time())}",
                "searchResultPosition": 0,
                "maxResults": max(1, min(max_results, 30)),
                "major": 0,
                "minor": 0,
                "startTime": start,
                "endTime": end,
                "employeeNoString": employee_no,
                "picEnable": False,
                "timeReverseOrder": True,
            }
        }
        return self.request("POST", "/ISAPI/AccessControl/AcsEvent?format=json", json=body)

    def user_info_capabilities(self) -> IsapiResponse:
        """supportFunction (нужен «put» для Modify) и допустимые userType [FRT §10.15.2.5, с.123]."""
        return self.request("GET", "/ISAPI/AccessControl/UserInfo/capabilities?format=json")

    def get_user(self, employee_no: str) -> dict:
        """Одна запись по employeeNo. Ответ проверяется: ровно одна запись и именно с этим employeeNo.

        Формат EmployeeNoList в UserInfoSearchCond в нашем наборе документации не описан (USER_MANAGEMENT.md §2):
        если терминал проигнорирует фильтр и вернёт других людей — это ошибка, данные отбрасываются.
        """
        body = {"UserInfoSearchCond": {"searchID": f"kpp-{int(time.time() * 1000)}", "searchResultPosition": 0,
                                       "maxResults": 1, "EmployeeNoList": [{"employeeNo": str(employee_no)}]}}
        r = self.request("POST", "/ISAPI/AccessControl/UserInfo/Search?format=json", json=body)
        if not r.ok or not isinstance(r.data, dict):
            raise IsapiError(f"UserInfo/Search: HTTP {r.status}")
        result = r.data.get("UserInfoSearch") or {}
        users = result.get("UserInfo") or []
        if isinstance(users, dict):
            users = [users]
        if len(users) != 1 or str(users[0].get("employeeNo")) != str(employee_no):
            raise IsapiError("UserInfo/Search вернул не одну запись с этим employeeNo — фильтр EmployeeNoList, "
                             "вероятно, не поддержан; данные отброшены")
        if result.get("numOfMatches") not in (None, 1, "1"):
            raise IsapiError("UserInfo/Search: numOfMatches ≠ 1")
        return users[0]

    def modify_user_type(self, employee_no: str, user_type: str) -> IsapiResponse:
        """PUT UserInfo/Modify только с employeeNo и userType [FRT §10.15.2.5, с.123]. Разрешение — check_operation."""
        return self.request("PUT", "/ISAPI/AccessControl/UserInfo/Modify?format=json",
                            json={"UserInfo": {"employeeNo": str(employee_no), "userType": user_type}})

    # ---------- Управление (только PILOT/SIMULATION, см. check_operation) ----------

    def put_remote_check(self, serial_no: int, check_result: str, info: str | None = None) -> IsapiResponse:
        """Асинхронный ответ на запрос удалённой проверки. В URL нет security/iv: см. REMOTE_VERIFICATION.md §2.6."""
        if check_result not in ("success", "failed"):
            raise ValueError("checkResult: success | failed")
        payload: dict = {"serialNo": int(serial_no), "checkResult": check_result}
        if info:
            payload["info"] = info[:32]
        return self.request("PUT", "/ISAPI/AccessControl/remoteCheck?format=json", json={"RemoteCheck": payload})
