"""Текущее время школы. Тесты подменяют now()."""

from datetime import date, datetime, time

from app.config import SCHOOL_TZ


def now() -> datetime:
    return datetime.now(SCHOOL_TZ)


def today() -> date:
    return now().date()


def now_minute() -> time:
    """Время выхода с точностью до минуты (ЧЧ:ММ, Ф-9)."""
    t = now()
    return time(t.hour, t.minute)
