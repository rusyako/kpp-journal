"""План настройки Remote Verification только для visitor. ТОЛЬКО ЧТЕНИЕ: ничего не отправляет на терминал.

    python -m app.integrations.hikvision.remote_check_plan --mock
    python -m app.integrations.hikvision.remote_check_plan --device stand --confirm-network

Читает AccessControl/capabilities, AcsCfg/capabilities, AcsCfg, httpHosts/capabilities, httpHosts и строит:
  * проверки поддержки (каждая — OK / STOP / WARN);
  * точный список изменяемых глобальных полей AcsCfg (текущее → целевое);
  * тело отката (текущие значения тех же полей);
  * вердикт. Применяет изменения инженер СКУД вручную — только на стенде и только после согласования.

Источники: FRT §10.16.4 (с.130–133), AcsCfg caps/GET [§14.6.3.1, §14.6.3.3, с.423–428], remoteCheckVerifyMode [с.127].
"""

import argparse
import json

from app.integrations.hikvision import settings as hik_settings
from app.integrations.hikvision.cli_common import add_target_args, build_client, utf8_console
from app.integrations.hikvision.client import IsapiClient, IsapiError

# 6 = «Face recognition or card swipe» [FRT с.127]: карта visitor тоже идёт на удалённую проверку.
# При 2 (только лицо) карта visitor авторизуется ЛОКАЛЬНО по doorRight/RightPlan — это обход kpp-journal.
TARGET = {
    "remoteCheckDoorEnabled": True,
    "checkChannelType": "ISAPIListen",
    "needDeviceCheck": True,
    "remoteCheckTimeout": 5,
    "remoteCheckVerifyMode": 6,
    "offlineDevCheckOpenDoorEnabled": False,
    "remoteCheckWithISAPIListen": "sync",
    "remoteCheckUserTypeList": ["visitor"],
}
# Значения по умолчанию по документации — для отката полей, которых не было в текущей конфигурации
DEFAULTS = {"remoteCheckDoorEnabled": False, "offlineDevCheckOpenDoorEnabled": False, "needDeviceCheck": True}


def _find(data, key):
    if isinstance(data, dict):
        if key in data:
            return data[key]
        for v in data.values():
            r = _find(v, key)
            if r is not None:
                return r
    elif isinstance(data, list):
        for v in data:
            r = _find(v, key)
            if r is not None:
                return r
    return None


def _opts(node) -> list[str] | None:
    if node is None:
        return None
    val = node.get("@opt") if isinstance(node, dict) else node
    if val is None:
        return []
    if isinstance(val, str):
        return [x.strip() for x in val.split(",")]
    return [str(x).lower() if isinstance(x, bool) else str(x) for x in val]


def build_plan(client: IsapiClient) -> dict:
    checks: list[dict] = []

    def check(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    def get(path):
        try:
            r = client.request("GET", path)
            return r.data if r.ok else None
        except IsapiError as e:
            check(path, "STOP", str(e))
            return None

    acc = get("/ISAPI/AccessControl/capabilities")
    caps = get("/ISAPI/AccessControl/AcsCfg/capabilities?format=json")
    cfg_doc = get("/ISAPI/AccessControl/AcsCfg?format=json")
    hosts_caps = get("/ISAPI/Event/notification/httpHosts/capabilities")
    hosts = get("/ISAPI/Event/notification/httpHosts")
    current = (cfg_doc or {}).get("AcsCfg", {}) if isinstance(cfg_doc, dict) else {}

    sup = _find(acc, "isSupportRemoteCheck")
    check("isSupportRemoteCheck", "OK" if str(sup).lower() == "true" else "STOP", f"значение: {sup}")
    if caps is None:
        check("AcsCfg/capabilities", "STOP", "не получено")
    else:
        ch = _opts(_find(caps, "checkChannelType")) or []
        check("checkChannelType=ISAPIListen", "OK" if "ISAPIListen" in ch else "STOP", f"@opt: {ch}")
        mode = _opts(_find(caps, "remoteCheckWithISAPIListen"))
        check("remoteCheckWithISAPIListen=sync", "OK" if mode and "sync" in mode else ("WARN" if mode else "STOP"),
              f"@opt: {mode} (без sync — только async)")
        utl = _find(caps, "remoteCheckUserTypeList")
        utl_opts = _opts(utl)
        if utl is None:
            check("remoteCheckUserTypeList", "STOP",
                  "поля нет в capabilities → visitor-only не поддержан; включение затронет ВСЕХ (normal тоже)")
        else:
            check("remoteCheckUserTypeList", "OK" if not utl_opts or "visitor" in utl_opts else "STOP",
                  f"@opt: {utl_opts}. Поддержка поля ≠ доказанная работа: обязательна проверка на стенде (И-2…И-4)")
        vm = _opts(_find(caps, "remoteCheckVerifyMode")) or []
        check("remoteCheckVerifyMode=6 (лицо или карта)", "OK" if "6" in vm else "STOP",
              f"@opt: {vm}. Без 6 карта visitor пройдёт локально в обход kpp-journal")
        for f in ("needDeviceCheck", "offlineDevCheckOpenDoorEnabled", "remoteCheckTimeout"):
            check(f, "OK" if _find(caps, f) is not None else "WARN", "есть в capabilities" if _find(caps, f) is not None
                  else "нет в capabilities — значение по умолчанию не подтверждено")
    if current.get("remoteCheckDoorEnabled") in (True, "true"):
        check("remoteCheckDoorEnabled сейчас", "STOP", "удалённая проверка УЖЕ включена — выяснить, кем и куда")
    else:
        check("remoteCheckDoorEnabled сейчас", "OK", f"{current.get('remoteCheckDoorEnabled')}")
    host_used = _find(hosts, "HttpHostNotification") is not None if hosts is not None else None
    check("httpHosts", "STOP" if host_used else ("OK" if host_used is False else "WARN"),
          "слот занят — Listening сломает существующую интеграцию" if host_used else
          ("свободен" if host_used is False else "не прочитан"))

    changes = [{"field": k, "current": current.get(k, "<нет>"), "target": v}
               for k, v in TARGET.items() if current.get(k, "<нет>") != v]
    rollback = {k: current.get(k, DEFAULTS.get(k)) for k in TARGET if k in current or k in DEFAULTS}
    stops = [c for c in checks if c["status"] == "STOP"]
    return {
        "checks": checks,
        "global_changes_AcsCfg": changes,
        "put_body": {"AcsCfg": TARGET},
        "rollback_body": {"AcsCfg": rollback},
        "rollback_note": "Поля, которых нет в текущей конфигурации (например remoteCheckUserTypeList), откатываются "
                         "remoteCheckDoorEnabled=false; httpHosts — вернуть по снимку «до»",
        "httpHosts_plan": "добавить хост прослушивания http://<IP kpp-journal>:8090/hikvision/listen/<key> "
                          "(единственный слот [FRT с.128, 131])",
        "http_hosts_capabilities": hosts_caps,
        "verdict": "STOP" if stops else "GO_STAND_ONLY",
        "verdict_text": ("Нельзя: " + "; ".join(c["check"] for c in stops)) if stops else
        "Можно настраивать ТОЛЬКО изолированный стенд. Общий терминал — только после И-1…И-4 на стенде и отдельного решения",
    }


def main(argv: list[str] | None = None) -> int:
    utf8_console()
    p = argparse.ArgumentParser(description="План visitor-only Remote Verification (только чтение)")
    add_target_args(p)
    args = p.parse_args(argv)
    settings = hik_settings.load()
    client, _device, _db, _mock = build_client(args, settings, "3818077855")
    with client:
        plan = build_plan(client)
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0 if plan["verdict"] != "STOP" else 1


if __name__ == "__main__":
    raise SystemExit(main())
