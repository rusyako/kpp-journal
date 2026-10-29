"""Telegram-бот: привязка эдвайзера по приглашению и кнопка Mini App.

    python -m app.bot

Уведомления «🚪 вышел» и отчёт отправляет API напрямую через Bot API (app/notify.py),
этому процессу достаточно принимать /start.
"""

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)
from sqlalchemy import select

from app import config
from app.db import SessionLocal
from app.models import Role, User
from app.services.invites import redeem_invite

log = logging.getLogger(__name__)
dp = Dispatcher()

ADVISOR_URL = f"{config.PUBLIC_URL}/advisor"
# Telegram открывает Mini App только по HTTPS
MINI_APP_AVAILABLE = config.PUBLIC_URL.startswith("https://")


def open_button() -> InlineKeyboardMarkup | None:
    if not MINI_APP_AVAILABLE:
        return None
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="📝 Разрешения на выход", web_app=WebAppInfo(url=ADVISOR_URL))]]
    )


def greeting(user: User) -> str:
    if user.role is Role.ADVISOR:
        groups = ", ".join(a.name for a in user.advisories) or "пока не назначена"
        return (
            f"Эдвайзери: {groups}.\n\n"
            "Чтобы разрешить ученику выйти сегодня, откройте «Разрешения на выход» и впишите время, "
            "например 15:05 или 1505. Сотрите время — разрешение отменится.\n\n"
            "Когда охрана отметит выход, я пришлю сообщение 🚪."
        )
    if user.receives_report:
        return f"Сюда будет приходить отчёт КПП за день в {config.REPORT_TIME}."
    return "Telegram привязан."


@dp.message(CommandStart())
async def start(message: Message, command: CommandObject) -> None:
    telegram_id = message.from_user.id
    with SessionLocal() as db:
        if command.args:
            user = redeem_invite(db, command.args.strip(), telegram_id)
            if user is None:
                await message.answer("Ссылка-приглашение недействительна или устарела. Попросите у администратора новую.")
                return
            header = f"✅ {user.display_name}, Telegram привязан.\n\n"
        else:
            user = db.scalar(select(User).where(User.telegram_id == telegram_id, User.active))
            if user is None:
                await message.answer("Этот Telegram не подключён к журналу. Попросите у администратора ссылку-приглашение.")
                return
            header = ""
        text = header + greeting(user)
        button = open_button() if user.role in (Role.ADVISOR, Role.ADMIN) else None
    await message.answer(text, reply_markup=button)


async def run() -> None:
    if not config.TELEGRAM_BOT_TOKEN:
        # Не падаем, чтобы docker не перезапускал контейнер по кругу
        log.warning("TELEGRAM_BOT_TOKEN не задан — бот не запущен")
        await asyncio.Event().wait()
    bot = Bot(config.TELEGRAM_BOT_TOKEN)
    if MINI_APP_AVAILABLE:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(text="Разрешения", web_app=WebAppInfo(url=ADVISOR_URL))
        )
    else:
        log.warning("PUBLIC_URL не https — кнопка Mini App отключена")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run())
