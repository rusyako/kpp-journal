"""Отчёт за день (Ф-19): сводка + списки, HTML для печати, Telegram и почты."""

from datetime import date
from io import BytesIO
from pathlib import Path
import re

from jinja2 import Environment, FileSystemLoader, select_autoescape
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
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


def render_xlsx(report: dict) -> bytes:
    wb = Workbook()
    summary = wb.active
    summary.title = "Сводка"
    details = wb.create_sheet("Подробности")
    summary_rows = [
        [f"Отчёт КПП за {report['date_label']}"],
        ["Дата", report["date"]],
        ["Показатель", "Количество"],
        ["Всего учеников", report["summary"]["total"]],
        ["Вышли", report["summary"]["exited"]],
        ["Раньше времени", report["summary"]["early"]],
        ["Без разрешения", report["summary"]["no_permission"]],
        ["С разрешением, но не вышли", report["summary"]["allowed_not_exited"]],
    ]
    detail_rows = [
        [f"Отчёт КПП за {report['date_label']}"],
        ["Дата", report["date"]],
        ["Категория", "ФИО", "Класс", "Эдвайзери", "Разрешено", "Вышел", "Причина"],
    ]
    fields = ("full_name", "class_name", "advisory", "allowed_time", "exit_time", "reason")
    for group in report["lists"]:
        for row in group["rows"]:
            detail_rows.append([group["title"], *(row[field] for field in fields)])

    for ws, rows, widths in (
        (summary, summary_rows, (46, 22)),
        (details, detail_rows, (44, 32, 14, 24, 16, 16, 48)),
    ):
        for row_index, values in enumerate(rows, 1):
            for column, value in enumerate(values, 1):
                if isinstance(value, str):
                    # XML 1.0 forbids controls and surrogates; never interpret user text as formulas.
                    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff\ufffe\uffff]", "", value)
                cell = ws.cell(row_index, column, value)
                if isinstance(value, str):
                    cell.data_type = "s"
                cell.alignment = Alignment(vertical="top", wrap_text=True)
                if row_index in (1, 3):
                    cell.font = Font(name="Calibri", size=16 if row_index == 1 else 11, bold=True, color="FFFFFF")
                    cell.fill = PatternFill("solid", fgColor="17365D")
                else:
                    cell.font = Font(name="Calibri", size=11, color="243746")
                    if row_index > 3 and row_index % 2 == 0:
                        cell.fill = PatternFill("solid", fgColor="EDF3F8")
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(widths))
        ws.row_dimensions[1].height = 32
        ws.row_dimensions[3].height = 30
        for column, width in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(column)].width = width
        ws.freeze_panes = "A4"
        ws.sheet_view.showGridLines = False
    details.auto_filter.ref = f"A3:G{details.max_row}"
    output = BytesIO()
    wb.save(output)
    return output.getvalue()


def summary_text(report: dict) -> str:
    s = report["summary"]
    return (
        f"<b>Отчёт КПП за {report['date_label']}</b>\n"
        f"Всего учеников: {s['total']}\n"
        f"Вышли: {s['exited']}\n"
        f"🟧 Раньше времени: {s['early']}\n"
        f"⚠️ Без разрешения: {s['no_permission']}\n"
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
