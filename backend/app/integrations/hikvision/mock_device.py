"""Виртуальный терминал Hikvision для тестов и симуляции.

Воспроизводит то, что описано в документации (а не реальное устройство):
  * Digest-аутентификацию (401 + WWW-Authenticate, затем проверка ответа) — FRT §4.3.1.1, с.19;
  * запрос удалённой проверки multipart/form-data — FRT с.130/133;
  * интерпретацию ответа в синхронном режиме: открыть только при RemoteCheck.checkResult="success"
    с тем же serialNo; нет ответа/ошибка/другой serialNo → проверка не пройдена (FRT с.126: «if no result is
    received within this time, the verification fails»; offlineDevCheckOpenDoorEnabled=false);
  * ответы GET на основные endpoint’ы (форма полей — FRT с.423–428, 519–521);
  * PUT /ISAPI/AccessControl/remoteCheck (асинхронный режим).
Любой другой изменяющий запрос записывается в forbidden_calls и получает 403 — тесты проверяют, что их нет.

Модель и прошивка виртуального терминала намеренно вымышленные («MOCK»), чтобы не выдавать симуляцию за оборудование.
"""

import hashlib
import json
import re
import secrets
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

import httpx

from app import clock

BOUNDARY = "MIMEBoundaryMock"
FAKE_JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 64 + b"\xff\xd9"

SIM_SOURCE = "simulator"


@dataclass
class TerminalOutcome:
    """Что сделал бы терминал после запроса удалённой проверки."""

    serial_no: int
    door_opened: bool
    reason: str
    http_status: int | None = None
    response: dict | None = None
    latency_ms: int = 0
    local: bool = False  # открыто/закрыто по локальным правам, без запроса к kpp-journal


@dataclass
class MockUser:
    """Запись персоны. Набор полей — как в HW-выгрузке UserInfo/Search нашего терминала (USER_MANAGEMENT.md §1)."""

    employee_no: str
    name: str = "SIMULATED PERSON"
    user_type: str = "normal"
    door_right: str = "1"
    right_plan: list = field(default_factory=lambda: [{"doorNo": 1, "planTemplateNo": "1"}])
    valid: dict = field(default_factory=lambda: {"enable": True, "beginTime": "2025-08-12T13:28:17",
                                                 "endTime": "2035-08-12T23:59:59", "timeType": "local"})
    num_face: int = 1
    num_card: int = 1
    only_verify: bool = False

    def record(self) -> dict:
        return {
            "employeeNo": self.employee_no, "name": self.name, "userType": self.user_type, "onlyVerify": self.only_verify,
            "closeDelayEnabled": False, "Valid": dict(self.valid), "belongGroup": "", "password": "",
            "doorRight": self.door_right, "RightPlan": [dict(p) for p in self.right_plan], "maxOpenDoorTime": 0,
            "openDoorTime": 0, "roomNumber": 2, "floorNumber": 0, "localUIRight": False, "gender": "unknown",
            "numOfCard": self.num_card, "numOfRemoteControl": 0, "numOfFP": 0, "numOfFace": self.num_face,
            "numOfPPAndPV": 0, "PersonInfoExtends": [{"value": ""}], "picID": "3",
        }


@dataclass
class MockHikvisionDevice:
    username: str = "admin"
    password: str = field(default_factory=lambda: secrets.token_hex(8))
    realm: str = "MockDevice"
    serial: int = 1000
    remote_check_enabled: bool = True
    listen_mode: str = "sync"  # sync | async
    remote_check_timeout_s: int = 5
    supports_user_type_list: bool = True
    # Настроенный remoteCheckUserTypeList; None/пусто — «all person types require remote verification» [FRT с.126]
    remote_check_user_types: list | None = None
    # Плохие прошивки для негативных тестов
    ignores_user_type_list: bool = False  # поле принято, но не работает → проверка для всех
    modify_resets_omitted: bool = False  # Modify заменяет запись целиком → поля, которых нет в запросе, сброшены
    ignores_employee_filter: bool = False  # UserInfo/Search игнорирует EmployeeNoList
    supports_user_modify: bool = True
    http_host_configured: bool = True
    users: dict = field(default_factory=dict)  # employeeNo → MockUser; пусто — старое поведение (всегда remoteCheck)
    ip_address: str = "10.0.0.250"
    requests: list = field(default_factory=list)
    forbidden_calls: list = field(default_factory=list)
    remote_check_puts: list = field(default_factory=list)
    outcomes: list = field(default_factory=list)
    _nonce: str = field(default_factory=lambda: secrets.token_hex(8))

    # ---------- События ----------

    def next_serial(self) -> int:
        self.serial = self.serial + 1 if self.serial < 100000 else 1  # serialNo в [1,100000] [FRT с.410]
        return self.serial

    def event(self, employee_no: str | None, *, minor: int = 75, major: int = 5, remote_check: bool = True,
              when: datetime | None = None, current: bool = True, serial: int | None = None,
              time_str: str | None = None, user_type: str | None = "visitor") -> dict:
        serial = serial if serial is not None else self.next_serial()
        when = when or clock.now()
        ts = time_str if time_str is not None else when.isoformat(timespec="seconds")
        ace = {
            "deviceName": "Access Controller",
            "majorEventType": major,
            "subEventType": minor,
            "time": ts,
            "name": "SIMULATED PERSON",  # должно быть вырезано парсером
            "serialNo": serial,
            "currentEvent": current,
            "frontSerialNo": serial - 1,
            "picturesNumber": 1,
        }
        if employee_no is not None:
            ace["employeeNoString"] = employee_no
        if user_type is not None:
            ace["userType"] = user_type
        if remote_check:
            ace["remoteCheck"] = True
        return {
            "ipAddress": self.ip_address,
            "portNo": 80,
            "channelID": 1,
            "dateTime": ts,
            "activePostCount": 1,
            "eventType": "AccessControllerEvent",
            "eventState": "active",
            "eventDescription": "Access Controller Event",
            "AccessControllerEvent": ace,
        }

    @staticmethod
    def multipart(event: dict, with_picture: bool = True, line_end: bytes = b"\r\n") -> tuple[str, bytes]:
        body = json.dumps(event, ensure_ascii=False).encode()
        nl = line_end
        out = [
            b"--" + BOUNDARY.encode(),
            b'Content-Disposition: form-data; name="AccessControllerEvent"',
            b'Content-Type: application/json; charset="UTF-8"',
            b"Content-Length: " + str(len(body)).encode(),
            b"",
            body,
        ]
        if with_picture:
            out += [
                b"--" + BOUNDARY.encode(),
                b'Content-Disposition: form-data; name="Picture";filename="Picture.jpg";',
                b"Content-Type: image/jpeg",
                b"Content-Length: " + str(len(FAKE_JPEG)).encode(),
                b"",
                FAKE_JPEG,
            ]
        out.append(b"--" + BOUNDARY.encode() + b"--")
        return f"multipart/form-data;boundary={BOUNDARY}", nl.join(out) + nl

    def present_face(self, post: Callable[[str, bytes], tuple[int, bytes]], employee_no: str | None, **kw) -> TerminalOutcome:
        """Лицо опознано → POST на хост прослушивания → решение терминала.

        post(content_type, body) -> (http_status, response_body); исключение = нет связи/нет ответа.

        Если задан self.users — терминал ведёт себя по документации: неизвестное лицо отсекается локально
        (needDeviceCheck=true), тип не из remoteCheckUserTypeList проходит по локальным правам (doorRight/RightPlan)
        и только загружает событие, тип из списка — ждёт решения платформы.
        """
        if self.users:
            return self._present_registered(post, employee_no, **kw)
        ev = self.event(employee_no, **kw)
        serial = ev["AccessControllerEvent"]["serialNo"]
        ct, body = self.multipart(ev)
        return self.send(post, ct, body, serial)

    def needs_remote_check(self, user_type: str) -> bool:
        if not self.remote_check_enabled:
            return False
        if not self.supports_user_type_list or self.ignores_user_type_list or not self.remote_check_user_types:
            return True
        return user_type in self.remote_check_user_types

    def _present_registered(self, post, employee_no, **kw) -> TerminalOutcome:
        user = self.users.get(employee_no) if employee_no else None
        if user is None:
            out = TerminalOutcome(self.next_serial(), False, "лицо не найдено в базе терминала → локальный отказ, запроса нет")
            self.outcomes.append(out)
            return out
        kw.pop("user_type", None)
        if self.needs_remote_check(user.user_type):
            ev = self.event(employee_no, user_type=user.user_type, **kw)
            ct, body = self.multipart(ev)
            return self.send(post, ct, body, ev["AccessControllerEvent"]["serialNo"])
        # Локальная авторизация: удалённой проверки нет, решение по правам терминала
        ev = self.event(employee_no, user_type=user.user_type, remote_check=False, **kw)
        serial = ev["AccessControllerEvent"]["serialNo"]
        try:
            post(*self.multipart(ev))  # загрузка события на хост прослушивания, ответ не ждём
        except Exception:
            pass
        opened = bool(user.door_right) and bool(user.right_plan)
        out = TerminalOutcome(serial, opened, f"{user.user_type}: локальная авторизация, без kpp-journal → "
                                              + ("турникет открыт" if opened else "нет прав"), local=True)
        self.outcomes.append(out)
        return out

    def send(self, post, content_type: str, body: bytes, serial: int) -> TerminalOutcome:
        started = datetime.now()
        try:
            status, resp = post(content_type, body)
        except Exception as e:  # нет связи с платформой
            out = TerminalOutcome(serial, False, f"нет ответа платформы ({type(e).__name__}) → проверка не пройдена")
            self.outcomes.append(out)
            return out
        latency = int((datetime.now() - started).total_seconds() * 1000)
        if latency > self.remote_check_timeout_s * 1000:
            out = TerminalOutcome(serial, False, "ответ позже remoteCheckTimeout → проверка не пройдена", status, None, latency)
        elif self.listen_mode == "async":
            # Ответ придёт отдельным PUT; здесь только подтверждение приёма
            out = TerminalOutcome(serial, self._async_result(serial), "асинхронный режим: решение по PUT remoteCheck", status, None, latency)
        else:
            out = self._interpret_sync(serial, status, resp, latency)
        self.outcomes.append(out)
        return out

    def _interpret_sync(self, serial: int, status: int, resp: bytes, latency: int) -> TerminalOutcome:
        if status != 200:
            return TerminalOutcome(serial, False, f"HTTP {status} → проверка не пройдена", status, None, latency)
        try:
            data = json.loads(resp.decode("utf-8"))
            rc = data["RemoteCheck"]
        except Exception:
            return TerminalOutcome(serial, False, "ответ не RemoteCheck JSON → проверка не пройдена", status, None, latency)
        if int(rc.get("serialNo", -1)) != serial:
            return TerminalOutcome(serial, False, "serialNo не совпадает → проверка не пройдена", status, data, latency)
        if rc.get("checkResult") == "success":
            return TerminalOutcome(serial, True, "checkResult=success → турникет открыт", status, data, latency)
        return TerminalOutcome(serial, False, "checkResult=failed → проход закрыт", status, data, latency)

    def _async_result(self, serial: int) -> bool:
        return any(p["serialNo"] == serial and p["checkResult"] == "success" for p in self.remote_check_puts)

    # ---------- ISAPI (HTTP) ----------

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handle)

    def _check_digest(self, request: httpx.Request) -> bool:
        auth = request.headers.get("authorization", "")
        if not auth.startswith("Digest "):
            return False
        fields = dict(re.findall(r'(\w+)="?([^",]+)"?', auth[7:]))
        if fields.get("username") != self.username or fields.get("nonce") != self._nonce:
            return False

        def h(s: str) -> str:
            return hashlib.md5(s.encode()).hexdigest()

        ha1 = h(f"{self.username}:{self.realm}:{self.password}")
        ha2 = h(f"{request.method}:{fields.get('uri', '')}")
        expected = h(f"{ha1}:{self._nonce}:{fields.get('nc')}:{fields.get('cnonce')}:{fields.get('qop')}:{ha2}")
        return fields.get("response") == expected

    def handle(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        self.requests.append((request.method, path))
        if not self._check_digest(request):
            return httpx.Response(
                401,
                headers={"WWW-Authenticate": f'Digest qop="auth", realm="{self.realm}", nonce="{self._nonce}", stale="FALSE"'},
                content=b"<?xml version=\"1.0\"?><ResponseStatus><statusCode>4</statusCode><statusString>Invalid Operation</statusString></ResponseStatus>",
            )
        if request.method == "GET":
            return self._get(path)
        if request.method == "POST" and path == "/ISAPI/AccessControl/AcsEvent":
            return httpx.Response(200, json={"AcsEvent": {"searchID": "mock", "responseStatusStrg": "OK",
                                                          "numOfMatches": 0, "totalMatches": 0, "InfoList": []}})
        if request.method == "POST" and path == "/ISAPI/AccessControl/UserInfo/Search":
            return self._user_search(json.loads(request.content))
        if request.method == "PUT" and path == "/ISAPI/AccessControl/UserInfo/Modify" and self.supports_user_modify:
            return self._user_modify(json.loads(request.content))
        if request.method == "PUT" and path == "/ISAPI/AccessControl/remoteCheck":
            body = json.loads(request.content)["RemoteCheck"]
            self.remote_check_puts.append(body)
            return httpx.Response(200, json={"statusCode": 1, "statusString": "OK", "subStatusCode": "ok"})
        self.forbidden_calls.append((request.method, path))
        return httpx.Response(403, json={"statusCode": 4, "statusString": "Invalid Operation", "subStatusCode": "notSupport"})

    def _user_search(self, body: dict) -> httpx.Response:
        cond = body.get("UserInfoSearchCond", {})
        wanted = {str(x.get("employeeNo")) for x in cond.get("EmployeeNoList") or []}
        users = list(self.users.values())
        if wanted and not self.ignores_employee_filter:
            users = [u for u in users if u.employee_no in wanted]
        users = users[: int(cond.get("maxResults", 30))]
        return httpx.Response(200, json={"UserInfoSearch": {
            "searchID": cond.get("searchID", ""), "responseStatusStrg": "OK", "numOfMatches": len(users),
            "totalMatches": len(users), "UserInfo": [u.record() for u in users]}})

    def _user_modify(self, body: dict) -> httpx.Response:
        info = body.get("UserInfo", {})
        user = self.users.get(str(info.get("employeeNo")))
        if user is None:
            return httpx.Response(400, json={"statusCode": 6, "statusString": "Invalid Content",
                                             "subStatusCode": "employeeNoNotExist"})
        if self.modify_resets_omitted:
            user.door_right, user.right_plan, user.valid = "", [], {"enable": False}
        if "userType" in info:
            user.user_type = info["userType"]
        return httpx.Response(200, json={"statusCode": 1, "statusString": "OK", "subStatusCode": "ok"})

    def _get(self, path: str) -> httpx.Response:
        xml = "application/xml; charset=\"UTF-8\""
        ns = 'xmlns="http://www.isapi.org/ver20/XMLSchema" version="2.0"'
        if path == "/ISAPI/System/deviceInfo":
            return httpx.Response(200, headers={"content-type": xml}, content=(
                f"<?xml version=\"1.0\"?><DeviceInfo {ns}><deviceName>MOCK</deviceName><model>MOCK-TERMINAL</model>"
                "<serialNumber>MOCK0000000001</serialNumber><firmwareVersion>V0.0.0-mock</firmwareVersion>"
                "<firmwareReleasedDate>build 000000</firmwareReleasedDate><deviceType>accessControlTerminal</deviceType></DeviceInfo>"
            ).encode())
        if path == "/ISAPI/AccessControl/capabilities":
            return httpx.Response(200, headers={"content-type": xml}, content=(
                f"<?xml version=\"1.0\"?><AccessControl {ns}><isSupportRemoteCheck>true</isSupportRemoteCheck>"
                "<isSupportAcsCfg>true</isSupportAcsCfg><isSupportUserInfo>true</isSupportUserInfo></AccessControl>"
            ).encode())
        if path == "/ISAPI/AccessControl/AcsCfg/capabilities":
            caps = {
                "remoteCheckDoorEnabled": {"@opt": [True, False]},
                "checkChannelType": {"@opt": ["Ezviz", "ISUP", "ISAPI", "PrivateSDK", "ISAPIListen"]},
                "needDeviceCheck": {"@opt": [True, False]},
                "remoteCheckTimeout": {"@min": 1, "@max": 10},
                "remoteCheckVerifyMode": {"@opt": [1, 2, 3, 4, 5, 6, 7]},
                "offlineDevCheckOpenDoorEnabled": {"@opt": [True, False]},
                "remoteCheckWithISAPIListen": {"@opt": ["async", "sync"]},
            }
            if self.supports_user_type_list:
                caps["remoteCheckUserTypeList"] = {"@opt": ["normal", "visitor"]}
            return httpx.Response(200, json={"AcsCfg": caps})
        if path == "/ISAPI/AccessControl/AcsCfg":
            cfg = {
                "remoteCheckDoorEnabled": self.remote_check_enabled,
                "checkChannelType": "ISAPIListen",
                "needDeviceCheck": True,
                "remoteCheckTimeout": self.remote_check_timeout_s,
                "remoteCheckVerifyMode": 2,
                "offlineDevCheckOpenDoorEnabled": False,
                "remoteCheckWithISAPIListen": self.listen_mode,
                "fireAlarmInputType": "alwaysOpen",
            }
            if self.supports_user_type_list and self.remote_check_user_types is not None:
                cfg["remoteCheckUserTypeList"] = list(self.remote_check_user_types)
            return httpx.Response(200, json={"AcsCfg": cfg})
        if path == "/ISAPI/AccessControl/UserInfo/capabilities":
            funcs = "get,post,put,delete,setUp" if self.supports_user_modify else "get,post,delete"
            return httpx.Response(200, json={"UserInfo": {"supportFunction": {"@opt": funcs},
                                                          "userType": {"@opt": "normal,visitor,blackList"},
                                                          "maxRecordNum": 3000}})
        if path == "/ISAPI/AccessControl/remoteCheck/capabilities":
            return httpx.Response(200, json={"RemoteCheck": {"serialNo": {"@min": 1, "@max": 2000000000},
                                                             "checkResult": {"@opt": ["success", "failed"]},
                                                             "info": {"@min": 1, "@max": 32}}})
        if path == "/ISAPI/Event/notification/httpHosts" and not self.http_host_configured:
            return httpx.Response(200, headers={"content-type": xml},
                                  content=f"<?xml version=\"1.0\"?><HttpHostNotificationList {ns}/>".encode())
        if path in ("/ISAPI/Event/notification/httpHosts", "/ISAPI/Event/notification/httpHosts/capabilities"):
            return httpx.Response(200, headers={"content-type": xml}, content=(
                f"<?xml version=\"1.0\"?><HttpHostNotificationList {ns}><HttpHostNotification><id>1</id>"
                "<url>/hikvision/listen/sim-exit</url><protocolType>HTTP</protocolType><addressingFormatType>ipaddress</addressingFormatType>"
                "<ipAddress>10.0.0.10</ipAddress><portNo>8090</portNo><httpAuthenticationMethod>none</httpAuthenticationMethod>"
                "</HttpHostNotification></HttpHostNotificationList>"
            ).encode())
        if path == "/ISAPI/AccessControl/AcsWorkStatus":
            return httpx.Response(200, json={"AcsWorkStatus": {"doorLockStatus": [0], "doorStatus": [4], "magneticStatus": [0]}})
        if path.startswith("/ISAPI/System/capabilities") or path.startswith("/ISAPI/Security/capabilities"):
            return httpx.Response(200, headers={"content-type": xml},
                                  content=f"<?xml version=\"1.0\"?><Capabilities {ns}><isSupportSubscribeEvent>true</isSupportSubscribeEvent></Capabilities>".encode())
        return httpx.Response(404, json={"statusCode": 4, "statusString": "Invalid Operation", "subStatusCode": "notSupport"})
