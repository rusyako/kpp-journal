"""Разрешения эдвайзеров (Ф-12 … Ф-16)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import clock, events
from app.models import Advisory, Permission, Role, Student, User
from app.services import audit
from app.services.day import DayRow, get_row, load_day
from app.services.normalize import words
from app.services.time_parse import format_time, parse_time

MAX_REASON = 500


class AdvisorError(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.status = status


def visible_advisories(db: Session, user: User) -> list[Advisory]:
    """Админ и руководство видят все эдвайзери, эдвайзер — только свои."""
    query = select(Advisory).where(Advisory.active).order_by(Advisory.sort_order, Advisory.name)
    if user.role is Role.ADVISOR:
        ids = [a.id for a in user.advisories]
        query = query.where(Advisory.id.in_(ids))
    return list(db.scalars(query))


def can_edit(user: User, advisory_id: int) -> bool:
    if user.role is Role.ADMIN:
        return True
    return user.role is Role.ADVISOR and any(a.id == advisory_id for a in user.advisories)


def status_text(row: DayRow) -> str:
    """Ф-15: что видит эдвайзер в столбце «Статус у охраны»."""
    if not row.student_active:
        return "❌ ученик не найден"
    if row.raw_time and row.allowed_time is None:
        return "⚠️ время не распознано"
    if row.allowed_time:
        return f"✅ {format_time(row.allowed_time)} передано охране"
    return ""


def advisor_row(row: DayRow) -> dict:
    return {
        "student_id": row.student_id,
        "full_name": row.full_name,
        "class_name": row.class_name,
        "time": format_time(row.allowed_time) if row.allowed_time else row.raw_time,
        "reason": row.reason,
        "status": status_text(row),
        # Ф-16: «🚪 ЧЧ:ММ» для любого ученика, даже без разрешения
        "exit": f"🚪 {format_time(row.exit_time)}" if row.exit_time else "",
        "early": row.status == "early",
        "color": "green" if row.exited else ("yellow" if row.allowed_time else ""),
    }


def advisory_rows(db: Session, advisory_id: int) -> list[dict]:
    rows = load_day(db, clock.today(), advisory_id)
    # Эдвайзеру удобнее алфавитный порядок, как во вкладке, а не порядок охраны
    rows.sort(key=lambda r: words(r.full_name))
    return [advisor_row(r) for r in rows if r.student_active or r.allowed_time or r.exited]


def set_permission(db: Session, user: User, student_id: int, time_text: str, reason: str) -> dict:
    """Записать время и причину. Пустое время = отмена разрешения (Ф-13)."""
    today = clock.today()
    student = db.get(Student, student_id)
    if student is None or not student.active:
        raise AdvisorError("❌ ученик не найден", 404)
    if not can_edit(user, student.advisory_id):
        raise AdvisorError("Это ученик другой эдвайзери", 403)

    time_text = time_text.strip()[:50]
    reason = reason.strip()[:MAX_REASON]
    perm = db.scalar(select(Permission).where(Permission.date == today, Permission.student_id == student_id))
    had_time = perm is not None and perm.deleted_at is None and perm.allowed_time is not None

    if not time_text and not reason:
        if perm is not None and perm.deleted_at is None:
            perm.deleted_at = clock.now()
    else:
        if perm is None:
            perm = Permission(date=today, student_id=student_id)
            db.add(perm)
        perm.allowed_time = parse_time(time_text) if time_text else None
        perm.raw_time = time_text
        perm.reason = reason
        perm.deleted_at = None
        perm.created_by = user.id

    has_time = perm is not None and perm.deleted_at is None and perm.allowed_time is not None
    if has_time:
        audit.log(db, user, "permission_set", student_id, time=format_time(perm.allowed_time), reason=reason)
    elif had_time:
        audit.log(db, user, "permission_clear", student_id)
    db.commit()

    events.day_changed(today.isoformat(), student_id, student.advisory_id)
    return advisor_row(get_row(db, today, student_id))
