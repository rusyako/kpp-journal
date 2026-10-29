"""Отметка выхода на КПП (Ф-8 … Ф-10)."""

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import clock, events, notify
from app.config import SCHOOL_TZ
from app.models import Exit, Student, User
from app.services import audit
from app.services.day import EARLY, NO_PERMISSION, OK, DayRow, get_row
from app.services.time_parse import format_time


class ExitError(Exception):
    def __init__(self, message: str, status: int = 409):
        super().__init__(message)
        self.status = status


@dataclass
class MarkResult:
    row: DayRow
    message: str


def exit_message(row: DayRow) -> str:
    """Сообщение охране после отметки (строка 9 в старом журнале)."""
    t = format_time(row.exit_time)
    if row.status == OK:
        return f"✅ {row.full_name} — выход {t}, разрешено с {format_time(row.allowed_time)}"
    if row.status == EARLY:
        return f"🟧 {row.full_name} вышел РАНЬШЕ разрешённого времени: {t}, разрешено с {format_time(row.allowed_time)}"
    if row.status == NO_PERMISSION:
        return f"⚠️ {row.full_name} вышел БЕЗ разрешения эдвайзера ({t})"
    return f"{row.full_name} — {t}"


def _active_exit(db: Session, student_id: int) -> Exit | None:
    return db.scalar(
        select(Exit).where(Exit.date == clock.today(), Exit.student_id == student_id, Exit.cancelled_at.is_(None))
    )


def mark_exit(db: Session, user: User, student_id: int, client_time: datetime | None = None) -> MarkResult:
    """Время ставит сервер. client_time — только для отметок из офлайн-очереди КПП."""
    today = clock.today()
    student = db.get(Student, student_id)
    if student is None:
        raise ExitError("Ученик не найден", 404)
    if _active_exit(db, student_id):
        raise ExitError(f"{student.full_name} уже отмечен как вышедший")

    exit_time = clock.now_minute()
    offline = client_time is not None
    if offline:
        local = client_time.astimezone(SCHOOL_TZ) if client_time.tzinfo else client_time.replace(tzinfo=SCHOOL_TZ)
        if local.date() != today:
            raise ExitError("Отметка из офлайн-очереди за другой день — внесите её вручную", 422)
        exit_time = min(exit_time, local.time().replace(second=0, microsecond=0))

    db.add(Exit(date=today, student_id=student_id, exit_time=exit_time, guard_id=user.id, offline=offline))
    try:
        db.flush()
    except IntegrityError:
        # Второй охранник успел отметить этого же ученика
        db.rollback()
        raise ExitError(f"{student.full_name} уже отмечен как вышедший")

    row = get_row(db, today, student_id)
    audit.log(db, user, "exit", student_id, time=format_time(exit_time), status=row.status, offline=offline)
    db.commit()

    events.day_changed(today.isoformat(), student_id, row.advisory_id)
    notify.exit_changed(db, row)
    return MarkResult(row, exit_message(row))


def cancel_exit(db: Session, user: User, student_id: int) -> MarkResult:
    """Ф-10: ошибочная отметка снимается, ученик возвращается к не вышедшим."""
    today = clock.today()
    current = _active_exit(db, student_id)
    if current is None:
        raise ExitError("У ученика нет отметки выхода за сегодня", 404)
    old_row = get_row(db, today, student_id)
    current.cancelled_at = clock.now()
    current.cancelled_by = user.id
    audit.log(db, user, "exit_cancel", student_id, time=format_time(current.exit_time))
    db.commit()

    row = get_row(db, today, student_id)
    events.day_changed(today.isoformat(), student_id, row.advisory_id)
    notify.exit_changed(db, old_row, cancelled=True)
    return MarkResult(row, f"↩️ Отметка снята: {row.full_name}")
