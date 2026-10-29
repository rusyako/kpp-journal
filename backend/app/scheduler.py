"""Расписание: отчёт за день в REPORT_TIME по рабочим дням (Ф-19).

Листы дня и архивацию по расписанию создавать больше не нужно: день — это дата в БД.
Работает внутри процесса API, поэтому uvicorn запускается с одним воркером.
"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app import clock, config
from app.db import SessionLocal
from app.services.calendar import is_working_day
from app.services.report import send_report

log = logging.getLogger(__name__)
_scheduler: BackgroundScheduler | None = None


def daily_report() -> None:
    today = clock.today()
    with SessionLocal() as db:
        if not is_working_day(db, today):
            log.info("Отчёт за %s не отправлен: нерабочий день", today)
            return
        result = send_report(db, today)
        log.info("Отчёт за %s отправлен: %s", today, result)


def start() -> None:
    global _scheduler
    hour, minute = (int(x) for x in config.REPORT_TIME.split(":"))
    _scheduler = BackgroundScheduler(timezone=config.SCHOOL_TZ)
    _scheduler.add_job(
        daily_report,
        CronTrigger(hour=hour, minute=minute, timezone=config.SCHOOL_TZ),
        id="daily_report",
        misfire_grace_time=3600,
        coalesce=True,
    )
    _scheduler.start()


def stop() -> None:
    if _scheduler is not None and _scheduler.running:
        _scheduler.shutdown(wait=False)


def status() -> dict:
    if _scheduler is None or not _scheduler.running:
        return {"running": False, "next_report": None}
    job = _scheduler.get_job("daily_report")
    next_run = job.next_run_time if job else None
    return {"running": True, "next_report": next_run.strftime("следующий: %d.%m.%Y %H:%M") if next_run else None}
