"""Пилот Hikvision: тестовые разрешения, симуляция, состояние для экрана администратора.

Тестовое разрешение (source="pilot") — не согласие родителей и не выдаётся за него.
"""

import json
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import clock
from app.config import SCHOOL_TZ
from app.integrations.hikvision import settings as hik_settings
from app.integrations.hikvision.adapter import handle_device_request
from app.integrations.hikvision.client import IsapiClient, IsapiError
from app.integrations.hikvision.mock_device import SIM_SOURCE, MockHikvisionDevice, MockUser
from app.integrations.hikvision.remote_check_plan import build_plan
from app.integrations.hikvision.user_type import change_user_type
from app.integrations.hikvision.settings import HikSettings, Mode
from app.models import (
    HikCommand,
    HikConfigSnapshot,
    HikDevice,
    HikDirection,
    HikEvent,
    HikPassage,
    HikPerson,
    ReleaseDecision,
    ReleasePermission,
    User,
)
from app.services import audit
from app.services.release import aware, permission_status, pilot_state, reason_text

MAX_PERMISSION_HOURS = 12
SIM_EXIT, SIM_ENTRY = "sim-exit", "sim-entry"
STAFF_DEMO = "1000000001"

# Состояние виртуальных терминалов (база персон, настройки) живёт в процессе и сбрасывается при перезапуске.
# Каждый терминал — как настроенный стенд: удалённая проверка только для visitor; тестовая запись пока normal.
_SIM_TERMINALS: dict[str, MockHikvisionDevice] = {}


def sim_terminal(device_key: str, settings: HikSettings) -> MockHikvisionDevice:
    """Терминал выхода — visitor-only удалённая проверка; терминал входа — только локальные права."""
    mock = _SIM_TERMINALS.get(device_key)
    if mock is None:
        users = {no: MockUser(no) for no in settings.pilot_employee_nos}
        users[STAFF_DEMO] = MockUser(STAFF_DEMO)
        mock = MockHikvisionDevice(users=users, remote_check_user_types=sorted(settings.remote_check_user_types),
                                   remote_check_enabled=device_key != SIM_ENTRY)
        _SIM_TERMINALS[device_key] = mock
    return mock


def reset_sim_terminals() -> None:
    _SIM_TERMINALS.clear()


class PilotError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def _fmt(dt: datetime | None) -> str | None:
    return aware(dt).isoformat(timespec="seconds") if dt else None


def _local(dt: datetime) -> datetime:
    return dt.replace(tzinfo=SCHOOL_TZ) if dt.tzinfo is None else dt.astimezone(SCHOOL_TZ)


# ---------- Подготовка ----------


def ensure_setup(db: Session, user: User | None, settings: HikSettings | None = None) -> dict:
    """Виртуальные терминалы и запись пилота для каждого employeeNo из HIKVISION_PILOT_EMPLOYEE_NOS. Идемпотентно."""
    settings = settings or hik_settings.load()
    created = []
    for key, name, direction in ((SIM_EXIT, "Симулятор: выход", HikDirection.EXIT), (SIM_ENTRY, "Симулятор: вход", HikDirection.ENTRY)):
        if db.scalar(select(HikDevice).where(HikDevice.key == key)) is None:
            db.add(HikDevice(key=key, name=name, direction=direction, simulated=True, allowed_ips=[]))
            created.append(key)
    for emp in sorted(settings.pilot_employee_nos):
        person = db.scalar(select(HikPerson).where(HikPerson.employee_no == emp))
        if person is None:
            db.add(HikPerson(employee_no=emp, label="Пилот: тестовая учётная запись ИТ", kind="test",
                             user_id=user.id if user else None, pilot=True, active=True))
            created.append(emp)
    pilot_state(db)
    if created:
        audit.log(db, user, "pilot_setup", None, created=created)
    db.commit()
    return {"created": created}


def set_enabled(db: Session, user: User, enabled: bool) -> bool:
    state = pilot_state(db)
    state.enabled = enabled
    state.updated_at = clock.now()
    state.updated_by = user.id
    audit.log(db, user, "pilot_enabled" if enabled else "pilot_disabled", None)
    db.commit()
    return enabled


# ---------- Тестовые разрешения ----------


def _pilot_person(db: Session, employee_no: str, settings: HikSettings) -> HikPerson:
    employee_no = str(employee_no).strip()
    if employee_no not in settings.pilot_employee_nos:
        raise PilotError("Тестовые разрешения — только для employeeNo из списка пилота", 403)
    person = db.scalar(select(HikPerson).where(HikPerson.employee_no == employee_no))
    if person is None or not person.pilot:
        raise PilotError("Запись пилота не создана — нажмите «Подготовить пилот»", 404)
    return person


def create_permission(db: Session, user: User, employee_no: str, valid_from: datetime, valid_until: datetime,
                      single_use: bool = True, note: str = "", settings: HikSettings | None = None) -> ReleasePermission:
    settings = settings or hik_settings.load()
    person = _pilot_person(db, employee_no, settings)
    valid_from, valid_until = _local(valid_from), _local(valid_until)
    if valid_until <= valid_from:
        raise PilotError("Окончание должно быть позже начала")
    if valid_until - valid_from > timedelta(hours=MAX_PERMISSION_HOURS):
        raise PilotError(f"Окно разрешения пилота — не больше {MAX_PERMISSION_HOURS} ч")
    if valid_until <= clock.now():
        raise PilotError("Окно уже закончилось")
    perm = ReleasePermission(person_id=person.id, source="pilot", valid_from=valid_from, valid_until=valid_until,
                             single_use=single_use, note=note.strip()[:500], created_by=user.id, created_at=clock.now())
    db.add(perm)
    db.flush()
    audit.log(db, user, "pilot_permission_set", None, permission_id=perm.id, employee_no=person.employee_no,
              valid_from=_fmt(valid_from), valid_until=_fmt(valid_until), single_use=single_use)
    db.commit()
    return perm


def revoke_permission(db: Session, user: User, permission_id: int) -> ReleasePermission:
    perm = db.get(ReleasePermission, permission_id)
    if perm is None:
        raise PilotError("Разрешение не найдено", 404)
    if perm.revoked_at is None:
        perm.revoked_at = clock.now()
        perm.revoked_by = user.id
        audit.log(db, user, "pilot_permission_revoke", None, permission_id=perm.id)
        db.commit()
    return perm


def permission_dict(p: ReleasePermission, now: datetime) -> dict:
    return {
        "id": p.id,
        "employee_no": p.person.employee_no if p.person else None,
        "source": p.source,
        "valid_from": _fmt(p.valid_from),
        "valid_until": _fmt(p.valid_until),
        "single_use": p.single_use,
        "note": p.note,
        "status": permission_status(p, now),
        "created_at": _fmt(p.created_at),
        "revoked_at": _fmt(p.revoked_at),
        "used_at": _fmt(p.used_at),
        "used_by_decision_id": p.used_by_decision_id,
    }


# ---------- Симуляция ----------

SCENARIOS = ("face", "repeat_last", "stale", "server_down", "card")


def simulate(db: Session, user: User, device_key: str, employee_no: str, scenario: str = "face",
             settings: HikSettings | None = None) -> dict:
    """Виртуальный терминал «видит лицо» и проходит весь путь: запрос → решение → ответ → открыл ли бы он турникет."""
    settings = settings or hik_settings.load()
    if settings.mode is not Mode.SIMULATION:
        raise PilotError("Симуляция доступна только в режиме SIMULATION", 409)
    if scenario not in SCENARIOS:
        raise PilotError("Неизвестный сценарий")
    device = db.scalar(select(HikDevice).where(HikDevice.key == device_key))
    if device is not None and not device.simulated:
        raise PilotError("Симулировать можно только виртуальный терминал", 409)

    # Зарегистрированный виртуальный терминал — со своей базой персон и visitor-only проверкой;
    # незарегистрированный — «чужой» терминал, который шлёт запрос по любому лицу
    mock = sim_terminal(device_key, settings) if device is not None else MockHikvisionDevice()
    mock.serial = max(mock.serial, _last_serial(db, device_key))
    trace: list[str] = []
    seen: dict = {}

    def post(content_type: str, body: bytes):
        if scenario == "server_down":
            raise ConnectionError("kpp-journal недоступен")
        r = handle_device_request(db, device_key, SIM_SOURCE, content_type, body, settings=settings)
        seen["decision_id"] = r.decision_id
        trace.append(f"kpp-journal: решение {r.decision} ({reason_text(r.reason or '')}), ответ checkResult={r.check_result}"
                     + (" — заблокировано режимом" if r.command_status == "blocked" else ""))
        return r.http_status, json.dumps(r.body or {}).encode()

    kw: dict = {}
    if scenario == "stale":
        kw["when"] = clock.now() - timedelta(seconds=settings.max_event_age_s + 60)
    if scenario == "card":
        kw["minor"] = 1  # 0x01 Valid Card Swiping — не лицо
    if scenario == "repeat_last":
        last = db.scalar(select(HikEvent).where(HikEvent.device_key == device_key, HikEvent.remote_check.is_(True),
                                                HikEvent.duplicate_of_id.is_(None)).order_by(HikEvent.id.desc()))
        if last is None:
            raise PilotError("Нет предыдущего события для повтора")
        kw["serial"] = last.serial_no
        kw["time_str"] = last.event_time_raw
        employee_no = last.employee_no or employee_no

    known = mock.users.get(employee_no) if mock.users else None
    user_type = known.user_type if known else ("—" if mock.users else "?")
    trace.append(f"Терминал «{device_key}»: лицо, employeeNo={employee_no or '—'}, userType={user_type}")
    if not mock.users or (known and mock.needs_remote_check(known.user_type)):
        trace.append("Терминал → kpp-journal: AccessControllerEvent remoteCheck=true (дверь закрыта, ждём решения)")
    outcome = mock.present_face(post, employee_no, **kw)
    trace.append(f"Терминал: {outcome.reason}")
    audit.log(db, user, "pilot_simulate", None, device=device_key, scenario=scenario, opened=outcome.door_opened)
    db.commit()
    return {
        "serial_no": outcome.serial_no,
        "door_opened": outcome.door_opened,
        "local": outcome.local,
        "user_type": None if user_type in ("—", "?") else user_type,
        "terminal": outcome.reason,
        "response": outcome.response,
        "decision_id": seen.get("decision_id"),
        "trace": trace,
    }


# ---------- userType и состояние удалённой проверки ----------


def _client_for(device: HikDevice, settings: HikSettings) -> IsapiClient:
    if device.simulated:
        mock = sim_terminal(device.key, settings)
        return IsapiClient(device, settings, transport=mock.transport(), credentials=(mock.username, mock.password))
    return IsapiClient(device, settings)  # NetworkDisabled в SIMULATION


def _snapshot(db: Session, device: HikDevice, kind: str, path: str, content: dict) -> None:
    db.add(HikConfigSnapshot(device_id=device.id, kind=kind, path=path, http_status=200, content=content,
                             taken_at=clock.now()))


def _remember_user_type(db: Session, device: HikDevice, employee_no: str, user_type: str | None) -> None:
    person = db.scalar(select(HikPerson).where(HikPerson.employee_no == employee_no))
    if person is not None and user_type:
        person.terminal_user_type, person.terminal_checked_at, person.terminal_device_key = user_type, clock.now(), device.key


def refresh_device(db: Session, user: User, device_key: str, settings: HikSettings | None = None) -> dict:
    """Только чтение: запись тестового пользователя + план visitor-only проверки. Реальный терминал — READ_ONLY/PILOT."""
    settings = settings or hik_settings.load()
    device = db.scalar(select(HikDevice).where(HikDevice.key == device_key))
    if device is None:
        raise PilotError("Терминал не найден", 404)
    employee_no = sorted(settings.pilot_employee_nos)[0]
    try:
        with _client_for(device, settings) as client:
            record = client.get_user(employee_no)
            plan = build_plan(client)
    except IsapiError as e:
        device.last_health_at, device.last_health_ok, device.last_error = clock.now(), False, str(e)[:300]
        db.commit()
        raise PilotError(f"Чтение не выполнено: {e}", 409)
    from app.integrations.hikvision.user_type import protect

    _snapshot(db, device, "user", "/ISAPI/AccessControl/UserInfo/Search", protect(record))
    _snapshot(db, device, "remote_check_plan", "/ISAPI/AccessControl/AcsCfg", plan)
    _remember_user_type(db, device, employee_no, record.get("userType"))
    device.last_health_at, device.last_health_ok, device.last_error = clock.now(), True, None
    audit.log(db, user, "pilot_refresh", None, device=device_key, user_type=record.get("userType"), verdict=plan["verdict"])
    db.commit()
    return {"user_type": record.get("userType"), "numOfFace": record.get("numOfFace"),
            "numOfCard": record.get("numOfCard"), "verdict": plan["verdict"], "verdict_text": plan["verdict_text"],
            "checks": plan["checks"], "global_changes_AcsCfg": plan["global_changes_AcsCfg"]}


def simulate_user_type(db: Session, user: User, device_key: str, target: str, apply: bool, confirm: str | None,
                       settings: HikSettings | None = None) -> dict:
    """Тот же инструмент смены userType, что и для реального терминала, — на виртуальном терминале."""
    settings = settings or hik_settings.load()
    if settings.mode is not Mode.SIMULATION:
        raise PilotError("Из браузера userType меняется только на виртуальном терминале (SIMULATION). "
                         "Реальный терминал — CLI user_type с подтверждением", 409)
    device = db.scalar(select(HikDevice).where(HikDevice.key == device_key))
    if device is None or not device.simulated:
        raise PilotError("Только виртуальный терминал", 409)
    employee_no = sorted(settings.pilot_employee_nos)[0]
    with _client_for(device, settings) as client:
        rep = change_user_type(client, settings, employee_no, target, apply=apply, confirm=confirm)
    for kind, rec in (("user_before", rep.before), ("user_after", rep.after)):
        if rec is not None:
            _snapshot(db, device, kind, "/ISAPI/AccessControl/UserInfo/Search", rec)
    _remember_user_type(db, device, employee_no, (rep.after or rep.before or {}).get("userType"))
    if rep.applied:
        audit.log(db, user, "pilot_user_type", None, device=device_key, employee_no=employee_no,
                  to=target, ok=rep.ok)
    db.commit()
    return {k: rep.as_dict()[k] for k in ("mode", "ok", "applied", "from_type", "target", "request", "confirm",
                                          "write_allowed", "problems", "steps", "unexpected_changes")}


def _last_serial(db: Session, device_key: str) -> int:
    """Терминал нумерует события по возрастанию; повтор (repeat_last) не должен откатывать счётчик."""
    serial = db.scalar(select(func.max(HikEvent.serial_no)).where(HikEvent.device_key == device_key))
    return serial or 1000


def simulate_passage(db: Session, user: User, decision_id: int, outcome: str = "passed",
                     settings: HikSettings | None = None) -> dict:
    """Виртуальный турникет присылает событие прохода (0xda) или «не прошёл» (0x89)."""
    settings = settings or hik_settings.load()
    if settings.mode is not Mode.SIMULATION:
        raise PilotError("Симуляция доступна только в режиме SIMULATION", 409)
    decision = db.get(ReleaseDecision, decision_id)
    if decision is None or decision.device_id is None:
        raise PilotError("Решение не найдено", 404)
    device = db.get(HikDevice, decision.device_id)
    if device is None or not device.simulated:
        raise PilotError("Симулировать можно только виртуальный терминал", 409)
    minor = {"passed": 218, "timed_out": 137}.get(outcome)
    if minor is None:
        raise PilotError("outcome: passed | timed_out")
    mock = MockHikvisionDevice()
    mock.serial = _last_serial(db, device.key)
    ct, body = mock.multipart(mock.event(decision.employee_no, minor=minor, remote_check=False))
    r = handle_device_request(db, device.key, SIM_SOURCE, ct, body, settings=settings)
    passage = db.scalar(select(HikPassage).where(HikPassage.decision_id == decision_id))
    return {"event_id": r.event_id, "passage": passage.outcome if passage else None}


# ---------- Связь с терминалом (read-only) ----------


def check_device(db: Session, user: User, device_key: str, settings: HikSettings | None = None) -> dict:
    """GET /ISAPI/System/deviceInfo. Виртуальный — через mock; реальный — только в READ_ONLY/PILOT."""
    settings = settings or hik_settings.load()
    device = db.scalar(select(HikDevice).where(HikDevice.key == device_key))
    if device is None:
        raise PilotError("Терминал не найден", 404)
    ok, error, info = False, None, {}
    try:
        if device.simulated:
            mock = MockHikvisionDevice()
            client = IsapiClient(device, settings, transport=mock.transport(), credentials=(mock.username, mock.password))
        else:
            client = IsapiClient(device, settings)
        with client:
            r = client.device_info()
        ok = r.ok
        data = r.data.get("DeviceInfo", {}) if isinstance(r.data, dict) else {}
        info = {k: data.get(k) for k in ("model", "firmwareVersion", "firmwareReleasedDate", "serialNumber")}
        if ok:
            device.model, device.firmware, device.serial_number = info["model"], info["firmwareVersion"], info["serialNumber"]
        else:
            error = f"HTTP {r.status}"
        db.add(HikCommand(device_id=device.id, kind="isapi_read", method="GET", path="/ISAPI/System/deviceInfo",
                          status="simulated" if device.simulated else "sent", http_status=r.status,
                          latency_ms=r.latency_ms, created_by=user.id, created_at=clock.now()))
    except IsapiError as e:
        error = str(e)[:300]
        db.add(HikCommand(device_id=device.id, kind="isapi_read", method="GET", path="/ISAPI/System/deviceInfo",
                          status="blocked" if "режим" in error else "error", error=error, created_by=user.id,
                          created_at=clock.now()))
    device.last_health_at, device.last_health_ok, device.last_error = clock.now(), ok, error
    db.commit()
    return {"ok": ok, "error": error, "info": info}


# ---------- Экран ----------


def dashboard(db: Session, limit: int = 30) -> dict:
    settings = hik_settings.load()
    now = clock.now()
    state = pilot_state(db)
    db.commit()
    devices = list(db.scalars(select(HikDevice).order_by(HikDevice.simulated.desc(), HikDevice.key)))
    persons = list(db.scalars(select(HikPerson).where(HikPerson.pilot.is_(True)).order_by(HikPerson.employee_no)))
    perms = list(db.scalars(select(ReleasePermission).order_by(ReleasePermission.id.desc()).limit(limit)))
    events = list(db.scalars(select(HikEvent).order_by(HikEvent.id.desc()).limit(limit)))
    decisions = list(db.scalars(select(ReleaseDecision).order_by(ReleaseDecision.id.desc()).limit(limit)))
    commands = list(db.scalars(select(HikCommand).order_by(HikCommand.id.desc()).limit(limit)))
    passages = {p.decision_id: p for p in db.scalars(select(HikPassage).where(HikPassage.decision_id.in_([d.id for d in decisions])))}
    event_meta = {e.id: e for e in db.scalars(select(HikEvent).where(HikEvent.id.in_([d.event_id for d in decisions])))}
    cmd_by_decision: dict[int, HikCommand] = {}
    for c in commands:
        if c.decision_id and c.decision_id not in cmd_by_decision:
            cmd_by_decision[c.decision_id] = c
    device_keys = {d.id: d.key for d in devices}
    plans: dict[int, HikConfigSnapshot] = {}
    for snap in db.scalars(select(HikConfigSnapshot).where(HikConfigSnapshot.kind == "remote_check_plan")
                           .order_by(HikConfigSnapshot.id.desc()).limit(50)):
        plans.setdefault(snap.device_id, snap)
    isolation = list(db.scalars(select(ReleaseDecision).where(ReleaseDecision.reason == "not_remote_check_type")
                                .order_by(ReleaseDecision.id.desc()).limit(5)))

    def remote_check(d: HikDevice) -> dict | None:
        snap = plans.get(d.id)
        if snap is None:
            return None
        c = snap.content
        return {"verdict": c.get("verdict"), "verdict_text": c.get("verdict_text"), "checked_at": _fmt(snap.taken_at),
                "stops": [x["check"] for x in c.get("checks", []) if x["status"] == "STOP"],
                "changes": c.get("global_changes_AcsCfg", [])}

    return {
        "isolation_alerts": [{"decision_id": d.id, "decided_at": _fmt(d.decided_at), "device_key": device_keys.get(d.device_id),
                              "employee_no": d.employee_no} for d in isolation],
        "settings": settings.public(),
        "pilot_enabled": state.enabled,
        "now": _fmt(now),
        "devices": [
            {
                "key": d.key, "name": d.name, "direction": d.direction.value, "simulated": d.simulated,
                "host": d.host, "response_mode": d.response_mode, "active": d.active,
                "control_allowed": settings.control_allowed(d), "model": d.model, "firmware": d.firmware,
                "last_event_at": _fmt(d.last_event_at), "last_health_at": _fmt(d.last_health_at),
                "last_health_ok": d.last_health_ok, "last_error": d.last_error,
                "remote_check": remote_check(d),
            }
            for d in devices
        ],
        "persons": [
            {
                "employee_no": p.employee_no, "label": p.label, "active": p.active,
                "terminal_user_type": p.terminal_user_type, "terminal_checked_at": _fmt(p.terminal_checked_at),
                "terminal_device_key": p.terminal_device_key,
                "permissions": [permission_dict(x, now) for x in perms if x.person_id == p.id
                                and permission_status(x, now) in ("active", "pending")],
            }
            for p in persons
        ],
        "permissions": [permission_dict(p, now) for p in perms],
        "events": [
            {
                "id": e.id, "received_at": _fmt(e.received_at), "device_key": e.device_key, "serial_no": e.serial_no,
                "event_time": e.event_time_raw, "major": e.major, "minor": e.minor, "employee_no": e.employee_no,
                "user_type": e.user_type,
                "remote_check": e.remote_check, "category": e.category, "duplicate_of_id": e.duplicate_of_id,
                "simulated": e.simulated,
            }
            for e in events
        ],
        "decisions": [
            {
                "id": d.id, "decided_at": _fmt(d.decided_at), "event_id": d.event_id, "device_key": device_keys.get(d.device_id),
                "employee_no": d.employee_no, "result": d.result, "reason": d.reason, "detail": d.detail,
                "user_type": event_meta[d.event_id].user_type if d.event_id in event_meta else None,
                "serial_no": event_meta[d.event_id].serial_no if d.event_id in event_meta else None,
                "mode": d.mode, "latency_ms": d.latency_ms,
                "command": ({"status": cmd_by_decision[d.id].status, "check_result": cmd_by_decision[d.id].check_result}
                            if d.id in cmd_by_decision else None),
                "passage": ({"outcome": passages[d.id].outcome, "source": passages[d.id].source,
                             "exit_id": passages[d.id].exit_id} if d.id in passages else None),
            }
            for d in decisions
        ],
        "commands": [
            {
                "id": c.id, "created_at": _fmt(c.created_at), "device_key": device_keys.get(c.device_id), "kind": c.kind,
                "method": c.method, "path": c.path, "check_result": c.check_result, "status": c.status,
                "http_status": c.http_status, "error": c.error, "latency_ms": c.latency_ms, "decision_id": c.decision_id,
            }
            for c in commands
        ],
    }
