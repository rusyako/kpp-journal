"""Смена userType ОДНОЙ записи пилота (normal ↔ visitor) с проверкой «до/после» и откатом.

    # DRY_RUN (по умолчанию): читает capabilities и запись, показывает точный запрос, сохраняет резервную копию
    python -m app.integrations.hikvision.user_type --mock --to visitor
    python -m app.integrations.hikvision.user_type --device stand --confirm-network --to visitor

    # Реальное изменение — только после отдельного подтверждения владельца оборудования:
    #   HIKVISION_MODE=PILOT, HIKVISION_USER_WRITE_ENABLED=1, HIKVISION_USER_WRITE_DEVICES=<key>
    python -m app.integrations.hikvision.user_type --device stand --confirm-network --to visitor \
        --apply --confirm "3818077855:normal->visitor"

    # Откат с проверкой против резервной копии
    python -m app.integrations.hikvision.user_type --device stand --confirm-network --to normal \
        --backup device-snapshots/<…>-before.json --apply --confirm "3818077855:visitor->normal"

Источники: поток редактирования персоны [FRT §10.15.2.5, с.123] (supportFunction содержит «put»);
типы персон [с.5, 393, 410, 507]. Схемы тела UserInfo/Modify в нашем наборе документации НЕТ — поэтому отправляется
минимальный запрос {employeeNo, userType}, а сохранность остальных полей проверяется повторным чтением.
Запись не удаляется и не создаётся заново; лицо, карта, Valid, doorRight, RightPlan не отправляются.
"""

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from app import clock
from app.integrations.hikvision import settings as hik_settings
from app.integrations.hikvision.cli_common import add_target_args, build_client, utf8_console
from app.integrations.hikvision.client import USER_TYPES, IsapiClient, IsapiError
from app.integrations.hikvision.settings import HikSettings

# Персональные/секретные поля: в отчётах и копиях только хэш (сравнивать можно, прочитать нельзя)
_HASHED = ("name", "password", "PersonInfoExtends")
# Учётные данные, которые не должны пропасть
_CREDENTIAL_COUNTS = ("numOfFace", "numOfCard", "numOfFP")


def protect(record: dict) -> dict:
    out = {}
    for k, v in record.items():
        if k in _HASHED and isinstance(v, str) and v.startswith("sha256:"):
            out[k] = v  # уже из резервной копии
        elif k in _HASHED:
            raw = json.dumps(v, ensure_ascii=False, sort_keys=True)
            out[k] = "sha256:" + hashlib.sha256(raw.encode()).hexdigest()[:16] if v not in ("", None, []) else v
        else:
            out[k] = v
    return out


def diff(before: dict, after: dict, ignore: tuple = ()) -> list[dict]:
    a, b = protect(before), protect(after)
    return [{"field": k, "before": a.get(k, "<нет>"), "after": b.get(k, "<нет>")}
            for k in sorted(set(a) | set(b)) if k not in ignore and a.get(k, "<нет>") != b.get(k, "<нет>")]


def _opt(caps, key: str) -> str | None:
    """Значение @opt (строка или список) у поля на любой глубине."""
    if isinstance(caps, dict):
        if key in caps:
            node = caps[key]
            val = node.get("@opt") if isinstance(node, dict) else node
            return ",".join(map(str, val)) if isinstance(val, list) else (str(val) if val is not None else None)
        for v in caps.values():
            found = _opt(v, key)
            if found is not None:
                return found
    return None


def confirm_phrase(employee_no: str, from_type: str, to_type: str) -> str:
    return f"{employee_no}:{from_type}->{to_type}"


@dataclass
class ChangeReport:
    employee_no: str
    target: str
    mode: str = "DRY_RUN"
    ok: bool = False
    applied: bool = False
    from_type: str | None = None
    request: dict | None = None
    confirm: str | None = None
    write_allowed: bool = False
    before: dict | None = None
    after: dict | None = None
    unexpected_changes: list = field(default_factory=list)
    restore_mismatch: list = field(default_factory=list)
    problems: list = field(default_factory=list)
    steps: list = field(default_factory=list)
    backup_path: str | None = None

    def as_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


def change_user_type(client: IsapiClient, settings: HikSettings, employee_no: str, target: str, *,
                     apply: bool = False, confirm: str | None = None, expected_from: str | None = None,
                     original: dict | None = None, backup_dir: Path | None = None) -> ChangeReport:
    rep = ChangeReport(employee_no=str(employee_no), target=target, mode="APPLY" if apply else "DRY_RUN")

    def stop(msg: str) -> ChangeReport:
        rep.problems.append(msg)
        rep.steps.append(f"СТОП: {msg}")
        return rep

    if rep.employee_no not in settings.pilot_employee_nos:
        return stop(f"employeeNo {employee_no} не в списке пилота HIKVISION_PILOT_EMPLOYEE_NOS")
    if target not in USER_TYPES:
        return stop("целевой userType — только normal или visitor")

    # 1. Возможности терминала
    try:
        caps = client.user_info_capabilities()
    except IsapiError as e:
        return stop(f"UserInfo/capabilities: {e}")
    if not caps.ok:
        return stop(f"UserInfo/capabilities: HTTP {caps.status} — изменение персон не подтверждено")
    funcs = _opt(caps.data, "supportFunction") or ""
    rep.steps.append(f"UserInfo/capabilities: supportFunction={funcs or '—'}")
    if "put" not in [f.strip() for f in funcs.split(",")]:
        return stop("supportFunction не содержит «put» — UserInfo/Modify не поддержан [FRT с.123]")
    types = _opt(caps.data, "userType")
    rep.steps.append(f"UserInfo/capabilities: userType={types or '— (не указано)'}")
    if not types or target not in [t.strip() for t in types.split(",")]:
        return stop(f"userType «{target}» не подтверждён capabilities терминала")

    # 2. Запись «до»
    try:
        before = client.get_user(rep.employee_no)
    except IsapiError as e:
        return stop(str(e))
    rep.before = protect(before)
    rep.from_type = before.get("userType")
    rep.steps.append(f"Запись прочитана: userType={rep.from_type}, numOfFace={before.get('numOfFace')}, "
                     f"numOfCard={before.get('numOfCard')}, doorRight={before.get('doorRight')!r}, "
                     f"RightPlan={before.get('RightPlan')}")
    if expected_from and rep.from_type != expected_from:
        return stop(f"ожидался userType={expected_from}, на терминале {rep.from_type}")
    if not before.get("numOfFace"):
        return stop("у записи нет лица (numOfFace=0) — пилот по лицу невозможен")

    if backup_dir is not None:
        backup_dir.mkdir(parents=True, exist_ok=True)
        path = backup_dir / f"user-{rep.employee_no}-{clock.now():%Y%m%d-%H%M%S}-before.json"
        path.write_text(json.dumps(protect(before), ensure_ascii=False, indent=2), encoding="utf-8")
        rep.backup_path = str(path)
        rep.steps.append(f"Резервная копия записи (ФИО/пароль — хэш): {path}")

    if rep.from_type == target:
        rep.ok = True
        rep.steps.append(f"userType уже {target} — изменений не требуется")
        if original is not None:
            rep.restore_mismatch = diff(original, before)
            rep.ok = not rep.restore_mismatch
        return rep

    rep.request = {"method": "PUT", "path": "/ISAPI/AccessControl/UserInfo/Modify?format=json",
                   "body": {"UserInfo": {"employeeNo": rep.employee_no, "userType": target}}}
    rep.confirm = confirm_phrase(rep.employee_no, rep.from_type, target)
    rep.write_allowed = settings.user_write_allowed(client.device)
    rep.steps.append("Запрос подготовлен: " + json.dumps(rep.request["body"], ensure_ascii=False))

    if not apply:
        rep.ok = True
        rep.steps.append(f"DRY_RUN: на терминал ничего не отправлено. Для изменения: --apply --confirm \"{rep.confirm}\""
                         + ("" if rep.write_allowed else " (и включить запись: HIKVISION_MODE=PILOT, "
                                                         "HIKVISION_USER_WRITE_ENABLED=1, HIKVISION_USER_WRITE_DEVICES)"))
        return rep

    # 3. Изменение
    if confirm != rep.confirm:
        return stop(f"нужно подтверждение --confirm \"{rep.confirm}\"")
    if not rep.write_allowed:
        return stop("запись запрещена настройками (HIKVISION_MODE/USER_WRITE_ENABLED/USER_WRITE_DEVICES)")
    try:
        r = client.modify_user_type(rep.employee_no, target)
    except IsapiError as e:
        return stop(f"UserInfo/Modify: {e}")
    rep.applied = True
    rep.steps.append(f"UserInfo/Modify → HTTP {r.status} {r.data if isinstance(r.data, dict) else ''}")
    if not r.ok:
        rep.problems.append(f"UserInfo/Modify вернул HTTP {r.status}")

    # 4. Запись «после» и сверка
    try:
        after = client.get_user(rep.employee_no)
    except IsapiError as e:
        return stop(f"повторное чтение не удалось: {e} — проверить вручную и при необходимости откатить")
    rep.after = protect(after)
    if after.get("userType") != target:
        rep.problems.append(f"после изменения userType={after.get('userType')}, ожидался {target}")
    rep.unexpected_changes = diff(before, after, ignore=("userType",))
    for f in rep.unexpected_changes:
        rep.problems.append(f"изменилось поле {f['field']}: {f['before']} → {f['after']}")
    for k in _CREDENTIAL_COUNTS:
        if (after.get(k) or 0) < (before.get(k) or 0):
            rep.problems.append(f"{k} уменьшилось: {before.get(k)} → {after.get(k)} (учётные данные потеряны!)")
    if original is not None:
        rep.restore_mismatch = diff(original, after)
        for f in rep.restore_mismatch:
            rep.problems.append(f"отличие от резервной копии: {f['field']}: {f['before']} → {f['after']}")
    rep.ok = not rep.problems
    rep.steps.append("Проверка после изменения: " + ("OK — изменился только userType" if rep.ok else "ПРОБЛЕМЫ, см. problems"))
    if backup_dir is not None:
        path = backup_dir / f"user-{rep.employee_no}-{clock.now():%Y%m%d-%H%M%S}-after.json"
        path.write_text(json.dumps(protect(after), ensure_ascii=False, indent=2), encoding="utf-8")
    return rep


def _record_in_db(device_key: str, rep: ChangeReport) -> None:
    """Сохранить снимки и прочитанный userType в kpp-journal (только для --device)."""
    from sqlalchemy import select

    from app.db import SessionLocal
    from app.models import HikConfigSnapshot, HikDevice, HikPerson

    with SessionLocal() as db:
        device = db.scalar(select(HikDevice).where(HikDevice.key == device_key))
        person = db.scalar(select(HikPerson).where(HikPerson.employee_no == rep.employee_no))
        for kind, rec in (("user_before", rep.before), ("user_after", rep.after)):
            if rec is not None and device is not None:
                db.add(HikConfigSnapshot(device_id=device.id, kind=kind, path="/ISAPI/AccessControl/UserInfo/Search",
                                         http_status=200, content=rec, taken_at=clock.now()))
        current = (rep.after or rep.before or {}).get("userType")
        if person is not None and current:
            person.terminal_user_type, person.terminal_checked_at, person.terminal_device_key = current, clock.now(), device_key
        db.commit()


def main(argv: list[str] | None = None) -> int:
    utf8_console()
    p = argparse.ArgumentParser(description="Смена userType одной записи пилота (по умолчанию DRY_RUN)")
    add_target_args(p)
    p.add_argument("--employee-no", default="3818077855")
    p.add_argument("--to", required=True, choices=list(USER_TYPES))
    p.add_argument("--expect-from", choices=list(USER_TYPES))
    p.add_argument("--apply", action="store_true", help="выполнить изменение (иначе DRY_RUN)")
    p.add_argument("--confirm", help='фраза подтверждения, например "3818077855:normal->visitor"')
    p.add_argument("--backup", help="резервная копия «до» (для отката: сверить, что всё вернулось)")
    p.add_argument("--out", default="device-snapshots")
    args = p.parse_args(argv)

    settings = hik_settings.load()
    client, device, db_device, _mock = build_client(args, settings, args.employee_no)
    original = json.loads(Path(args.backup).read_text(encoding="utf-8")) if args.backup else None
    with client:
        rep = change_user_type(client, settings, args.employee_no, args.to, apply=args.apply, confirm=args.confirm,
                               expected_from=args.expect_from, original=original,
                               backup_dir=Path(args.out) / f"{device.key}".replace(":", "_"))
    if db_device is not None:
        _record_in_db(db_device.key, rep)
    for s in rep.steps:
        print("•", s)
    print(json.dumps({k: rep.as_dict()[k] for k in ("mode", "ok", "applied", "from_type", "target", "request",
                                                    "confirm", "write_allowed", "problems")}, ensure_ascii=False, indent=2))
    if rep.applied and not rep.ok:
        print(f"\n⚠ Откат: --to {rep.from_type} --backup {rep.backup_path} --apply "
              f"--confirm \"{confirm_phrase(rep.employee_no, rep.target, rep.from_type or '')}\"")
    return 0 if rep.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
