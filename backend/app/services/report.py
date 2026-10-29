"""Отчёт за день (Ф-19): сводка + списки, HTML для печати, Telegram и почты."""

from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app import config, notify
from app.models import Exit, Student
from app.services import audit
from app.services.day import ALLOWED, EARLY, NO_PERMISSION, OK, DayRow, load_day
from app.services.time_parse import format_time

_env = Environment(
    loader=FileSystemLoader(Path(__file__).resolve().parents[1] / "templates"),
    autoescape=select_autoescape(["html"]),
)


def _item(row: DayRow) -> dict:
    return {
        "full_name": row.full_name,
        "class_name": row.class_name,
        "advisory": row.advisory,
        "allowed_time": format_time(row.allowed_time) if row.allowed_time else "",
        "exit_time": format_time(row.exit_time) if row.exit_time else "",
        "reason": row.reason,
    }


def build_report(db: Session, d: date) -> dict:
    rows = load_day(db, d)
    by_status: dict[str, list[DayRow]] = {}
    for r in rows:
        by_status.setdefault(r.status, []).append(r)

    cancelled = db.scalars(
        select(Exit)
        .options(joinedload(Exit.student).joinedload(Student.advisory))
        .where(Exit.date == d, Exit.cancelled_at.is_not(None))
        .order_by(Exit.exit_time)
    ).all()

    exited = [r for r in rows if r.exited]
    summary = {
        "total": len([r for r in rows if r.student_active]),
        "exited": len(exited),
        "early": len(by_status.get(EARLY, [])),
        "no_permission": len(by_status.get(NO_PERMISSION, [])),
        "not_exited": len([r for r in rows if not r.exited and r.student_active]),
        "allowed_not_exited": len(by_status.get(ALLOWED, [])),
    }
    lists = [
        {"key": "early", "title": "🟧 Вышли раньше разрешённого времени", "rows": by_status.get(EARLY, [])},
        {"key": "no_permission", "title": "⚠️ Вышли без разрешения эдвайзера", "rows": by_status.get(NO_PERMISSION, [])},
        {"key": "allowed_not_exited", "title": "🟨 С разрешением, но не вышли", "rows": by_status.get(ALLOWED, [])},
        {"key": "ok", "title": "🟩 Вышли по разрешению", "rows": by_status.get(OK, [])},
        {
            "key": "cancelled",
            "title": "↩️ Отметки, снятые охраной",
            "rows": [
                DayRow(
                    student_id=e.student_id,
                    full_name=e.student.full_name,
                    class_name=e.student.class_name,
                    advisory=e.student.advisory.name,
                    advisory_id=e.student.advisory_id,
                    exit_time=e.exit_time,
                )
                for e in cancelled
            ],
        },
    ]
    for lst in lists:
        lst["rows"] = [_item(r) for r in lst["rows"]]
    return {"date": d.isoformat(), "date_label": d.strftime("%d.%m.%Y"), "summary": summary, "lists": lists}


def render_html(report: dict) -> str:
    return _env.get_template("report.html").render(report=report)


def summary_text(report: dict) -> str:
    s = report["summary"]
    return (
        f"<b>Отчёт КПП за {report['date_label']}</b>\n"
        f"Всего учеников: {s['total']}\n"
        f"Вышли: {s['exited']}\n"
        f"🟧 Раньше времени: {s['early']}\n"
        f"⚠️ Без разрешения: {s['no_permission']}\n"
        f"Не вышли: {s['not_exited']}\n"
        f"🟨 С разрешением, но не вышли: {s['allowed_not_exited']}"
    )


def send_report(db: Session, d: date) -> dict:
    """Разослать отчёт руководству. Возвращает, куда ушло."""
    report = build_report(db, d)
    html = render_html(report)
    text = summary_text(report)
    filename = f"otchet_{d.strftime('%d.%m.%Y')}.html"
    sent_tg = 0
    for chat_id in notify.report_chat_ids(db):
        if notify.send_telegram(chat_id, text, document=(filename, html.encode())):
            sent_tg += 1
    sent_email = notify.send_email(config.REPORT_EMAILS, f"Отчёт КПП за {report['date_label']}", html)
    audit.log(db, None, "report_sent", date=report["date"], telegram=sent_tg, email=sent_email)
    db.commit()
    return {"telegram": sent_tg, "email": sent_email}
