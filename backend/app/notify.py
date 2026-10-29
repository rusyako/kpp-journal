"""Уведомления в Telegram и на почту. Отправка идёт в фоне и не задерживает охрану."""

import logging
import smtplib
from concurrent.futures import ThreadPoolExecutor
from email.message import EmailMessage

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import config
from app.models import Role, User, UserAdvisory
from app.services.day import EARLY, NO_PERMISSION, DayRow
from app.services.time_parse import format_time

log = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="notify")

# Тесты включают синхронную отправку, чтобы проверить, что ушло
SYNC = False


def _submit(fn, *args) -> None:
    if SYNC:
        fn(*args)
    else:
        _executor.submit(fn, *args)


def send_telegram(chat_id: int, text: str, document: tuple[str, bytes] | None = None) -> bool:
    if not config.TELEGRAM_BOT_TOKEN:
        return False
    base = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}"
    try:
        if document:
            name, content = document
            r = httpx.post(
                f"{base}/sendDocument",
                data={"chat_id": chat_id, "caption": text[:1024], "parse_mode": "HTML"},
                files={"document": (name, content)},
                timeout=20,
            )
        else:
            r = httpx.post(
                f"{base}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"},
                timeout=10,
            )
        r.raise_for_status()
        return True
    except httpx.HTTPError as e:
        log.warning("Telegram: не удалось отправить в %s: %s", chat_id, e)
        return False


def send_email(to: list[str], subject: str, html: str) -> bool:
    if not (config.SMTP_HOST and to):
        return False
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config.SMTP_FROM
    msg["To"] = ", ".join(to)
    msg.set_content("Отчёт во вложении в формате HTML.")
    msg.add_alternative(html, subtype="html")
    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=30) as smtp:
            smtp.starttls()
            if config.SMTP_USER:
                smtp.login(config.SMTP_USER, config.SMTP_PASSWORD)
            smtp.send_message(msg)
        return True
    except (OSError, smtplib.SMTPException) as e:
        log.warning("Почта: не удалось отправить отчёт: %s", e)
        return False


def advisor_chat_ids(db: Session, advisory_id: int) -> list[int]:
    return list(
        db.scalars(
            select(User.telegram_id)
            .join(UserAdvisory, UserAdvisory.user_id == User.id)
            .where(
                UserAdvisory.advisory_id == advisory_id,
                User.active,
                User.role == Role.ADVISOR,
                User.telegram_id.is_not(None),
            )
        )
    )


def report_chat_ids(db: Session) -> list[int]:
    return list(
        db.scalars(select(User.telegram_id).where(User.active, User.receives_report, User.telegram_id.is_not(None)))
    )


def exit_text(row: DayRow, cancelled: bool = False) -> str:
    who = f"{row.full_name} ({row.class_name})"
    if cancelled:
        return f"↩️ Отметка выхода снята: {who}"
    text = f"🚪 {who} вышел через КПП в {format_time(row.exit_time)}"
    if row.status == EARLY:
        text += f" — 🟧 раньше разрешённых {format_time(row.allowed_time)}"
    elif row.status == NO_PERMISSION:
        text += " — ⚠️ без разрешения"
    return text


def exit_changed(db: Session, row: DayRow, cancelled: bool = False) -> None:
    """Ф-16: эдвайзер узнаёт о выходе любого своего ученика, даже без разрешения."""
    text = exit_text(row, cancelled)
    for chat_id in advisor_chat_ids(db, row.advisory_id):
        _submit(send_telegram, chat_id, text)
