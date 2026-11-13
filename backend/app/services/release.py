"""Decision Engine: можно ли выпустить человека через турникет прямо сейчас.

Терминал Hikvision только опознаёт человека (employeeNo). Решение принимает эта функция — до открытия прохода.
Правила fail-closed: любая непроверенная ситуация — DENY.

Решение (release_decisions), команда терминалу (hik_commands) и фактический проход (hik_passages) — разные
записи. ALLOW ≠ «вышел»: выход фиксируется только по событию прохода или ручному подтверждению.
"""

import logging
import time
from dataclasses import dataclass
from datetime import datetime, timedelta

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import clock
from app.config import SCHOOL_TZ
from app.integrations.hikvision.settings import HikSettings
from app.models import (
    Exit,
    HikCommand,
    HikDevice,
    HikDirection,
    HikEvent,
    HikPassage,
    HikPerson,
    HikPilotState,
    ReleaseDecision,
    ReleasePermission,
    Student,
    User,
)
from app.services import audit

log = logging.getLogger("hikvision.release")

ALLOW, DENY = "ALLOW", "DENY"

REASONS = {
    "permission_valid": "Действующее тестовое разрешение пилота",
    "duplicate_event": "Повтор уже обработанного события — повторного открытия нет",
    "unknown_device": "Событие от неизвестного терминала",
    "device_inactive": "Терминал отключён в kpp-journal",
    "untrusted_source": "Запрос пришёл не с разрешённого адреса терминала",
    "wrong_direction": "Терминал не на выход — автоматический выпуск не применяется",
    "pilot_disabled": "Пилот выключен",
    "unsupported_event": "Тип события/способ опознания не участвует в пилоте",
    "not_realtime": "Событие не в реальном времени (догрузка из журнала)",
    "bad_event_time": "Не удалось прочитать время события",
    "stale_event": "Событие устарело или время терминала расходится с сервером",
    "no_employee_no": "В событии нет employeeNo",
    "unknown_person": "employeeNo не связан ни с одним профилем",
    "person_inactive": "Связь employeeNo отключена",
    "profile_inactive": "Профиль ученика/сотрудника неактивен",
    "not_in_pilot": "Человек не участвует в пилоте",
    "not_remote_check_type": "НАРУШЕНИЕ ИЗОЛЯЦИИ: запрос от userType, который не должен идти на удалённую проверку",
    "user_type_unknown": "userType не подтверждён (нет в событии и не прочитан с терминала)",
    "no_permission": "Нет разрешения",
    "permission_not_started": "Разрешение ещё не начало действовать",
    "permission_expired": "Срок разрешения истёк",
    "permission_revoked": "Разрешение отменено",
    "permission_used": "Одноразовое разрешение уже использовано",
    "decision_timeout": "Решение не успело в отведённое время",
    "internal_error": "Внутренняя ошибка — автоматический выпуск запрещён",
}


def reason_text(code: str) -> str:
    return REASONS.get(code, code)


def aware(dt: datetime | None) -> datetime | None:
    """SQLite возвращает время без пояса; всё время в БД — в поясе школы."""
    if dt is None:
        return None
    return dt.replace(tzinfo=SCHOOL_TZ) if dt.tzinfo is None else dt.astimezone(SCHOOL_TZ)


@dataclass
class ExitRequest:
    """Запрос удалённой проверки, уже записанный в hik_events."""

    event: HikEvent
    device: HikDevice | None
    source_trusted: bool
    duplicate: bool = False


# ---------- Состояние пилота ----------


def pilot_state(db: Session) -> HikPilotState:
    state = db.get(HikPilotState, 1)
    if state is None:
        state = HikPilotState(id=1, enabled=False)
        db.add(state)
        try:
            db.flush()
        except IntegrityError:
            db.rollback()
            state = db.get(HikPilotState, 1)
    return state


def permission_status(p: ReleasePermission, now: datetime) -> str:
    if p.revoked_at is not None:
        return "revoked"
    if p.single_use and p.used_at is not None:
        return "used"
    if now < aware(p.valid_from):
        return "pending"
    if now >= aware(p.valid_until):
        return "expired"
    return "active"


_STATUS_REASON = {
    "revoked": "permission_revoked",
    "used": "permission_used",
    "pending": "permission_not_started",
    "expired": "permission_expired",
}


# ---------- Проверки ----------


def _evaluate(db: Session, req: ExitRequest, settings: HikSettings, now: datetime):
    """→ (allow, reason, person, permission). Порядок проверок важен: первая неудача и есть причина."""
    ev, device = req.event, req.device
    if req.duplicate:
        return False, "duplicate_event", None, None
    if device is None:
        return False, "unknown_device", None, None
    if not device.active:
        return False, "device_inactive", None, None
    if not req.source_trusted:
        return False, "untrusted_source", None, None
    if device.direction is not HikDirection.EXIT:
        return False, "wrong_direction", None, None
    if not pilot_state(db).enabled:
        return False, "pilot_disabled", None, None
    # Удалённая проверка должна приходить только для visitor. Запрос от normal значит, что фильтр
    # remoteCheckUserTypeList на терминале не работает — сотрудникам kpp-journal решений не выдаёт
    if ev.user_type is not None and ev.user_type not in settings.remote_check_user_types:
        return False, "not_remote_check_type", None, None
    if ev.major != 5 or ev.minor not in settings.allowed_minors:
        return False, "unsupported_event", None, None
    if ev.current_event is False:
        return False, "not_realtime", None, None
    event_time = aware(ev.event_time)
    if event_time is None:
        return False, "bad_event_time", None, None
    if abs((now - event_time).total_seconds()) > settings.max_event_age_s:
        return False, "stale_event", None, None
    if not ev.employee_no:
        return False, "no_employee_no", None, None

    person = db.scalar(select(HikPerson).where(HikPerson.employee_no == ev.employee_no))
    if person is None:
        return False, "unknown_person", None, None
    if not person.active:
        return False, "person_inactive", person, None
    if person.student_id is not None:
        student = db.get(Student, person.student_id)
        if student is None or not student.active:
            return False, "profile_inactive", person, None
    if person.user_id is not None:
        user = db.get(User, person.user_id)
        if user is None or not user.active:
            return False, "profile_inactive", person, None
    if not person.pilot or person.employee_no not in settings.pilot_employee_nos:
        return False, "not_in_pilot", person, None
    if ev.user_type is None:
        # Терминал не прислал userType — опираемся только на тип, проверенно прочитанный с терминала
        if person.terminal_user_type is None:
            return False, "user_type_unknown", person, None
        if person.terminal_user_type not in settings.remote_check_user_types:
            return False, "not_remote_check_type", person, None

    perms = list(
        db.scalars(
            select(ReleasePermission)
            .where(ReleasePermission.person_id == person.id, ReleasePermission.source == "pilot")
            .order_by(ReleasePermission.created_at.desc(), ReleasePermission.id.desc())
        )
    )
    active = [p for p in perms if permission_status(p, now) == "active"]
    if active:
        # Первым расходуем то, что раньше истекает
        active.sort(key=lambda p: aware(p.valid_until))
        return True, "permission_valid", person, active[0]
    if not perms:
        return False, "no_permission", person, None
    latest = perms[0]
    return False, _STATUS_REASON.get(permission_status(latest, now), "no_permission"), person, latest


def decide_exit(db: Session, req: ExitRequest, settings: HikSettings, deadline: float | None = None) -> ReleaseDecision:
    """Решение по одному событию удалённой проверки. Сохраняется и коммитится.

    deadline — time.monotonic(), после которого ALLOW уже не выдаём (терминал перестанет ждать).
    """
    t0 = time.perf_counter()
    now = clock.now()
    try:
        allow, reason, person, permission = _evaluate(db, req, settings, now)
    except Exception:
        log.exception("Ошибка проверки разрешения для события %s", req.event.id)
        db.rollback()
        allow, reason, person, permission = False, "internal_error", None, None

    if allow and deadline is not None and time.monotonic() > deadline:
        allow, reason = False, "decision_timeout"

    decision = ReleaseDecision(
        event_id=req.event.id,
        device_id=req.device.id if req.device else None,
        person_id=person.id if person else None,
        permission_id=permission.id if permission else None,
        employee_no=req.event.employee_no,
        direction=req.device.direction.value if req.device else "",
        result=ALLOW if allow else DENY,
        reason=reason,
        detail=reason_text(reason),
        mode=settings.mode.value,
        decided_at=now,
    )
    db.add(decision)
    db.flush()

    if allow and permission is not None and permission.single_use:
        # Атомарно: два одновременных запроса не израсходуют одно разрешение дважды
        res = db.execute(
            update(ReleasePermission)
            .where(
                ReleasePermission.id == permission.id,
                ReleasePermission.used_at.is_(None),
                ReleasePermission.revoked_at.is_(None),
            )
            .values(used_at=now, used_by_decision_id=decision.id)
            .execution_options(synchronize_session=False)
        )
        if res.rowcount != 1:
            decision.result, decision.reason, decision.detail = DENY, "permission_used", reason_text("permission_used")

    decision.latency_ms = int((time.perf_counter() - t0) * 1000)
    # Журнал решений — сама таблица release_decisions; в журнал действий КПП каждое лицо не пишем
    db.commit()
    log.info("Решение %s/%s для employeeNo=%s (событие %s, %d мс)", decision.result, decision.reason,
             decision.employee_no, req.event.id, decision.latency_ms)
    return decision


# ---------- Фактический проход ----------

PASSAGE_OUTCOMES = {"passage": "passed", "passage_timeout": "timed_out", "reverse_passage": "reverse"}


def _delivered_allow(db: Session, decision_id: int) -> bool:
    """ALLOW считается выданным, только если ответ success реально ушёл (или ушёл бы в симуляции)."""
    return db.scalar(
        select(HikCommand.id).where(
            HikCommand.decision_id == decision_id,
            HikCommand.check_result == "success",
            HikCommand.status.in_(("sent", "simulated")),
        )
    ) is not None


def _create_exit(db: Session, person: HikPerson | None) -> int | None:
    """Для ученика — отметка выхода «по турникету». Тестовая учётная запись пилота в журнал КПП не попадает."""
    if person is None or person.student_id is None:
        return None
    today = clock.today()
    existing = db.scalar(
        select(Exit).where(Exit.date == today, Exit.student_id == person.student_id, Exit.cancelled_at.is_(None))
    )
    if existing is not None:
        return existing.id
    ex = Exit(date=today, student_id=person.student_id, exit_time=clock.now_minute(), guard_id=None, offline=False)
    db.add(ex)
    db.flush()
    audit.log(db, None, "exit_turnstile", person.student_id, time=ex.exit_time.strftime("%H:%M"))
    return ex.id


def record_device_passage(db: Session, event: HikEvent, settings: HikSettings) -> HikPassage | None:
    """Событие прохода (0xda / 0x89 / 0x86) привязываем к последнему выданному ALLOW на этом терминале."""
    outcome = PASSAGE_OUTCOMES.get(event.category)
    if outcome is None or event.device_id is None:
        return None
    since = aware(event.received_at) - timedelta(seconds=settings.passage_window_s)
    q = (
        select(ReleaseDecision)
        .outerjoin(HikPassage, HikPassage.decision_id == ReleaseDecision.id)
        .where(
            ReleaseDecision.device_id == event.device_id,
            ReleaseDecision.result == ALLOW,
            ReleaseDecision.decided_at >= since,
            HikPassage.id.is_(None),
        )
        .order_by(ReleaseDecision.decided_at.desc(), ReleaseDecision.id.desc())
    )
    if event.employee_no:
        q = q.where(ReleaseDecision.employee_no == event.employee_no)
    for decision in db.scalars(q):
        if not _delivered_allow(db, decision.id):
            continue
        person = db.get(HikPerson, decision.person_id) if decision.person_id else None
        passage = HikPassage(
            decision_id=decision.id,
            event_id=event.id,
            person_id=decision.person_id,
            device_id=event.device_id,
            outcome=outcome,
            source="device_event",
            recorded_at=clock.now(),
        )
        if outcome == "passed":
            passage.exit_id = _create_exit(db, person)
        db.add(passage)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return None
        log.info("Проход %s по решению %s (событие %s)", outcome, decision.id, event.id)
        return passage
    db.commit()
    return None


class PassageError(Exception):
    pass


def confirm_passage_manually(db: Session, user: User, decision_id: int, passed: bool) -> HikPassage:
    """Охрана/инженер видели, прошёл ли человек (если турникет не шлёт событие прохода)."""
    decision = db.get(ReleaseDecision, decision_id)
    if decision is None:
        raise PassageError("Решение не найдено")
    if decision.result != ALLOW or not _delivered_allow(db, decision.id):
        raise PassageError("Подтверждать проход можно только по выданному ALLOW")
    if db.scalar(select(HikPassage).where(HikPassage.decision_id == decision_id)) is not None:
        raise PassageError("Результат прохода по этому решению уже записан")
    person = db.get(HikPerson, decision.person_id) if decision.person_id else None
    passage = HikPassage(
        decision_id=decision.id,
        person_id=decision.person_id,
        device_id=decision.device_id,
        outcome="passed" if passed else "not_passed",
        source="manual",
        recorded_at=clock.now(),
        confirmed_by=user.id,
    )
    if passed:
        passage.exit_id = _create_exit(db, person)
    db.add(passage)
    audit.log(db, user, "passage_confirm", None, decision_id=decision.id, passed=passed)
    db.commit()
    return passage
