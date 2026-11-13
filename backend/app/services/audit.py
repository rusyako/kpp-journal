"""Журнал действий (Ф-21)."""

from datetime import date, datetime, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import SCHOOL_TZ
from app.models import AuditLog, Student, User


def log(db: Session, user: User | None, action: str, student_id: int | None = None, **payload) -> None:
    db.add(AuditLog(user_id=user.id if user else None, action=action, student_id=student_id, payload=payload))


ACTION_TITLES = {
    "exit": "Отметил выход",
    "exit_cancel": "Снял отметку",
    "permission_set": "Разрешил выход",
    "permission_clear": "Отменил разрешение",
    "import": "Загрузил список",
    "report_sent": "Отправлен отчёт",
    "login": "Вход",
    "exit_turnstile": "Вышел через турникет",
    "passage_confirm": "Подтвердил проход",
    "pilot_setup": "Пилот: подготовка",
    "pilot_enabled": "Пилот включён",
    "pilot_disabled": "Пилот выключен",
    "pilot_permission_set": "Пилот: разрешение",
    "pilot_permission_revoke": "Пилот: отмена разрешения",
    "pilot_simulate": "Пилот: симуляция",
    "pilot_refresh": "Пилот: чтение терминала",
    "pilot_user_type": "Пилот: смена userType",
}


def entries_for_day(db: Session, d: date) -> list[dict]:
    start = datetime.combine(d, time.min, SCHOOL_TZ)
    end = datetime.combine(d, time.max, SCHOOL_TZ)
    rows = db.execute(
        select(AuditLog, User, Student)
        .outerjoin(User, AuditLog.user_id == User.id)
        .outerjoin(Student, AuditLog.student_id == Student.id)
        .where(AuditLog.ts >= start, AuditLog.ts <= end)
        .order_by(AuditLog.ts.desc(), AuditLog.id.desc())
    ).all()
    result = []
    for entry, user, student in rows:
        ts = entry.ts if entry.ts.tzinfo else entry.ts.replace(tzinfo=SCHOOL_TZ)
        result.append(
            {
                "time": ts.astimezone(SCHOOL_TZ).strftime("%H:%M:%S"),
                "user": (user.email or user.display_name) if user else "система",
                "student": f"{student.full_name} ({student.class_name})" if student else "",
                "action": ACTION_TITLES.get(entry.action, entry.action),
                "details": entry.payload,
            }
        )
    return result
