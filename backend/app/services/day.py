"""Лист дня — выборка по дате: разрешения эдвайзеров + отметки КПП (раздел 4, Ф-18)."""

from dataclasses import dataclass
from datetime import date, time

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.models import Exit, Permission, Student
from app.services.normalize import words
from app.services.time_parse import format_time

# Статус строки
NONE = "none"  # нет разрешения, не вышел
ALLOWED = "allowed"  # 🟨 есть разрешение, ещё не вышел
OK = "ok"  # 🟩 вышел по разрешению
EARLY = "early"  # 🟧 вышел раньше разрешённого времени
NO_PERMISSION = "no_permission"  # 🟩 + ⚠️ вышел без разрешения

COLORS = {NONE: "", ALLOWED: "yellow", OK: "green", EARLY: "orange", NO_PERMISSION: "green"}


@dataclass
class DayRow:
    student_id: int
    full_name: str
    class_name: str
    advisory: str
    advisory_id: int
    student_active: bool = True
    allowed_time: time | None = None
    raw_time: str = ""
    reason: str = ""
    exit_time: time | None = None
    exit_offline: bool = False

    @property
    def exited(self) -> bool:
        return self.exit_time is not None

    @property
    def status(self) -> str:
        if self.exit_time is None:
            return ALLOWED if self.allowed_time else NONE
        if self.allowed_time is None:
            return NO_PERMISSION
        return EARLY if self.exit_time < self.allowed_time else OK

    @property
    def color(self) -> str:
        return COLORS[self.status]

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "full_name": self.full_name,
            "class_name": self.class_name,
            "advisory": self.advisory,
            "advisory_id": self.advisory_id,
            "allowed_time": format_time(self.allowed_time) if self.allowed_time else None,
            "reason": self.reason,
            "exited": self.exited,
            "exit_time": format_time(self.exit_time) if self.exit_time else None,
            "exit_offline": self.exit_offline,
            "status": self.status,
            "color": self.color,
        }


def load_day(db: Session, d: date, advisory_id: int | None = None) -> list[DayRow]:
    permissions = {
        p.student_id: p
        for p in db.scalars(select(Permission).where(Permission.date == d, Permission.deleted_at.is_(None)))
    }
    exits = {e.student_id: e for e in db.scalars(select(Exit).where(Exit.date == d, Exit.cancelled_at.is_(None)))}

    # Выбывшие тоже попадают в выборку, если у них есть запись за этот день
    query = (
        select(Student)
        .options(joinedload(Student.advisory))
        .where(or_(Student.active, Student.id.in_(set(permissions) | set(exits))))
    )
    if advisory_id is not None:
        query = query.where(Student.advisory_id == advisory_id)

    rows = []
    for s in db.scalars(query):
        p = permissions.get(s.id)
        e = exits.get(s.id)
        rows.append(
            DayRow(
                student_id=s.id,
                full_name=s.full_name,
                class_name=s.class_name,
                advisory=s.advisory.name,
                advisory_id=s.advisory_id,
                student_active=s.active,
                allowed_time=p.allowed_time if p else None,
                raw_time=p.raw_time if p else "",
                reason=p.reason if p else "",
                exit_time=e.exit_time if e else None,
                exit_offline=e.offline if e else False,
            )
        )
    return sort_rows(rows)


def _name_key(row: DayRow) -> list[str]:
    return words(row.full_name)


def sort_rows(rows: list[DayRow]) -> list[DayRow]:
    """Ф-18: 🟨 с разрешением (по времени) → остальные не вышедшие (по алфавиту) → вышедшие (по времени выхода)."""

    def key(r: DayRow) -> tuple:
        if r.exited:
            return (2, r.exit_time, _name_key(r))
        if r.allowed_time:
            return (0, r.allowed_time, _name_key(r))
        return (1, time(0), _name_key(r))

    return sorted(rows, key=key)


def get_row(db: Session, d: date, student_id: int) -> DayRow | None:
    student = db.get(Student, student_id)
    if student is None:
        return None
    return next((r for r in load_day(db, d, student.advisory_id) if r.student_id == student_id), None)
