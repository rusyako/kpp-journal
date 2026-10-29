"""Рабочие дни: по умолчанию пн–сб, исключения — в таблице school_days."""

from datetime import date

from sqlalchemy.orm import Session

from app.models import SchoolDay


def is_working_day(db: Session, d: date) -> bool:
    override = db.get(SchoolDay, d)
    if override is not None:
        return override.is_working
    return d.weekday() < 6
