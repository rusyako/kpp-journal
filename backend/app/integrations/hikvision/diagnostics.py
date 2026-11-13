"""Read-only диагностика терминала по чек-листу DEVICE_CAPABILITIES.md §2.

    # демонстрация на виртуальном терминале (сети нет)
    python -m app.integrations.hikvision.diagnostics --mock

    # реальный терминал — ТОЛЬКО после разрешения владельца оборудования
    $env:HIKVISION_MODE="READ_ONLY"; $env:HIK_DIAG_USER="admin"; $env:HIK_DIAG_PASSWORD="..."
    python -m app.integrations.hikvision.diagnostics --host 192.168.x.x --confirm-read-only [--events]

Делает только GET (и, с --events, один поиск AcsEvent по тестовому employeeNo без фото).
Никаких PUT/DELETE, RemoteControl, AcsCfg, httpHosts — клиент их не умеет (client.check_operation).
Запросы по одному, с паузой; после отказа Digest (401) — остановка, чтобы не заблокировать учётную запись.
Отчёт сохраняется в --out (по умолчанию device-snapshots/, в .gitignore); поля с паролями вырезаны.
"""

import argparse
import getpass
import json
import os
import re
import sys
import time
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace

from app import clock
from app.integrations.hikvision import settings as hik_settings
from app.integrations.hikvision.client import AuthLockout, IsapiClient, IsapiError
from app.integrations.hikvision.mock_device import MockHikvisionDevice

CHECKLIST = [
    ("deviceInfo", "/ISAPI/System/deviceInfo"),
    ("systemCapabilities", "/ISAPI/System/capabilities"),
    ("accessCapabilities", "/ISAPI/AccessControl/capabilities"),
    ("acsCfgCapabilities", "/ISAPI/AccessControl/AcsCfg/capabilities?format=json"),
    ("acsCfg", "/ISAPI/AccessControl/AcsCfg?format=json"),
    ("remoteCheckCapabilities", "/ISAPI/AccessControl/remoteCheck/capabilities?format=json"),
    ("httpHostsCapabilities", "/ISAPI/Event/notification/httpHosts/capabilities"),
    ("httpHosts", "/ISAPI/Event/notification/httpHosts"),
    ("acsEventCapabilities", "/ISAPI/AccessControl/AcsEvent/capabilities?format=json"),
    ("acsWorkStatus", "/ISAPI/AccessControl/AcsWorkStatus?format=json"),
    ("doorParam1", "/ISAPI/AccessControl/Door/param/1"),
    ("userInfoCapabilities", "/ISAPI/AccessControl/UserInfo/capabilities?format=json"),
    ("securityCapabilities", "/ISAPI/Security/capabilities"),
]

_SECRET = re.compile(r"pass|secret|token|key$|Password", re.I)
_PERSONAL = re.compile(r"^(name|cardNo|pictureURL|.*[Pp]icture.*)$")


def redact(value):
    if isinstance(value, dict):
        return {k: ("***" if _SECRET.search(k) else redact(v)) for k, v in value.items() if not _PERSONAL.match(k)}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return value


def _find(data, key):
    """Первое значение ключа на любой глубине."""
    if isinstance(data, dict):
        if key in data:
            return data[key]
        for v in data.values():
            found = _find(v, key)
            if found is not None:
                return found
    elif isinstance(data, list):
        for v in data:
            found = _find(v, key)
            if found is not None:
                return found
    return None


def verdict(results: dict) -> dict:
    """Решающая матрица DEVICE_CAPABILITIES.md §3. Всё, чего нет в ответах, — «неизвестно», а не «нет»."""
    def get(name):
        r = results.get(name) or {}
        return r.get("data") if r.get("status") == 200 else None

    acc, caps, cfg, hosts = get("accessCapabilities"), get("acsCfgCapabilities"), get("acsCfg"), get("httpHosts")
    support = _find(acc, "isSupportRemoteCheck") if acc else None
    channel_opts = _find(_find(caps, "checkChannelType") or {}, "@opt") if caps else None
    listen_opts = _find(_find(caps, "remoteCheckWithISAPIListen") or {}, "@opt") if caps else None
    out = {
        "isSupportRemoteCheck": support,
        "ISAPIListen": None if channel_opts is None else "ISAPIListen" in str(channel_opts),
        "sync": None if listen_opts is None else "sync" in str(listen_opts),
        "remoteCheckUserTypeList_in_caps": None if caps is None else _find(caps, "remoteCheckUserTypeList") is not None,
        "remoteCheckDoorEnabled_now": _find(cfg, "remoteCheckDoorEnabled") if cfg else None,
        "httpHosts_configured": None if hosts is None else _find(hosts, "HttpHostNotification") is not None,
        "firmwareReleasedDate": _find(get("deviceInfo"), "firmwareReleasedDate"),
    }
    notes = []
    if str(out["isSupportRemoteCheck"]).lower() != "true":
        notes.append("Удалённая проверка не подтверждена → Remote Verification нельзя планировать (DEVICE_CAPABILITIES.md §3)")
    if out["ISAPIListen"] and out["sync"]:
        notes.append("Есть ISAPIListen + sync → Sync Listening (рекомендован)")
    elif out["ISAPIListen"]:
        notes.append("Есть ISAPIListen без sync → Async Listening")
    if out["remoteCheckUserTypeList_in_caps"] is False:
        notes.append("remoteCheckUserTypeList нет в capabilities → изоляция по userType невозможна; пилот только на отдельном терминале")
    if out["httpHosts_configured"]:
        notes.append("Слот httpHosts уже занят → Listening не использовать без согласования с владельцем той интеграции")
    if str(out["remoteCheckDoorEnabled_now"]).lower() == "true":
        notes.append("ВНИМАНИЕ: удалённая проверка уже включена на терминале — выяснить, кем и куда")
    out["notes"] = notes
    return out


def run(client: IsapiClient, *, pause_s: float, employee_no: str | None, events: bool) -> dict:
    results: dict = {}
    steps = list(CHECKLIST)
    for i, (name, path) in enumerate(steps):
        if i:
            time.sleep(pause_s)
        try:
            r = client.request("GET", path)
            results[name] = {"path": path, "status": r.status, "latency_ms": r.latency_ms, "data": redact(r.data)}
        except AuthLockout as e:
            results[name] = {"path": path, "error": str(e)}
            results["_stopped"] = "401: дальнейшие запросы не выполнялись"
            break
        except IsapiError as e:
            results[name] = {"path": path, "error": str(e)}
    if events and employee_no and "_stopped" not in results:
        time.sleep(pause_s)
        now = clock.now()
        try:
            r = client.search_events(employee_no, (now - timedelta(days=1)).isoformat(timespec="seconds"),
                                     now.isoformat(timespec="seconds"))
            results["acsEventSearch"] = {"path": "POST /ISAPI/AccessControl/AcsEvent", "status": r.status, "data": redact(r.data)}
        except IsapiError as e:
            results["acsEventSearch"] = {"error": str(e)}
    return {"taken_at": clock.now().isoformat(timespec="seconds"), "results": results, "verdict": verdict(results)}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Read-only диагностика терминала Hikvision")
    p.add_argument("--mock", action="store_true", help="виртуальный терминал (без сети)")
    p.add_argument("--host")
    p.add_argument("--port", type=int, default=80)
    p.add_argument("--scheme", default="http", choices=["http", "https"])
    p.add_argument("--confirm-read-only", action="store_true",
                   help="подтверждаю: есть разрешение на read-only запросы к этому терминалу")
    p.add_argument("--events", action="store_true", help="также поиск AcsEvent по тестовому employeeNo за сутки")
    p.add_argument("--employee-no", default="3818077855")
    p.add_argument("--out", default="device-snapshots")
    args = p.parse_args(argv)
    try:
        sys.stdout.reconfigure(errors="replace")  # консоль Windows (cp1251) не знает «→»
    except AttributeError:
        pass

    settings = hik_settings.load()
    if args.mock:
        mock = MockHikvisionDevice()
        device = SimpleNamespace(key="mock", simulated=True, active=True, host="", port=80, scheme="http", credentials_env=None)
        client = IsapiClient(device, settings, transport=mock.transport(), credentials=(mock.username, mock.password))
        label = "mock"
    else:
        if not args.host or not args.confirm_read_only:
            print("Нужны --host и --confirm-read-only (запросы к школьным терминалам — только с разрешения)", file=sys.stderr)
            return 2
        if not settings.network_allowed():
            print(f"HIKVISION_MODE={settings.mode}: сеть к терминалам выключена. Установите READ_ONLY.", file=sys.stderr)
            return 2
        user = os.environ.get("HIK_DIAG_USER") or input("Логин терминала: ").strip()
        password = os.environ.get("HIK_DIAG_PASSWORD") or getpass.getpass("Пароль терминала: ")
        device = SimpleNamespace(key="diag", simulated=False, active=True, host=args.host, port=args.port,
                                 scheme=args.scheme, credentials_env=None)
        client = IsapiClient(device, settings, credentials=(user, password))
        label = args.host.replace(".", "-").replace(":", "_")

    with client:
        report = run(client, pause_s=0 if args.mock else settings.request_pause_s,
                     employee_no=args.employee_no, events=args.events)
    out_dir = Path(args.out) / f"{label}-{clock.now():%Y%m%d-%H%M%S}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["verdict"], ensure_ascii=False, indent=2))
    print(f"Отчёт: {out_dir / 'report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
