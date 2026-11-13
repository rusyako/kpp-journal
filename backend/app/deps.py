from typing import Iterator

from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import config, db as database
from app.models import Role, User
from app.services.auth import SESSION_COOKIE, read_session, validate_init_data

TG_HEADER = "X-Telegram-Init-Data"


def get_db() -> Iterator[Session]:
    with database.SessionLocal() as session:
        yield session


def resolve_user(db: Session, init_data: str | None, session_token: str | None) -> User | None:
    """Telegram Mini App присылает initData, браузер — cookie сессии."""
    user = None
    if init_data:
        tg = validate_init_data(init_data, config.TELEGRAM_BOT_TOKEN)
        if tg and "id" in tg:
            user = db.scalar(select(User).where(User.telegram_id == int(tg["id"])))
    if user is None and session_token:
        session = read_session(session_token)
        if session is not None:
            uid, version = session
            user = db.get(User, uid)
            if user is not None and user.session_version != version:
                user = None  # сеанс завершён: сменили пароль или нажали «Завершить сеансы»
    return user if user is not None and user.active else None


def current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user = resolve_user(db, request.headers.get(TG_HEADER), request.cookies.get(SESSION_COOKIE))
    if user is None:
        raise HTTPException(401, "Нужно войти")
    return user


def require(*roles: Role):
    def dependency(user: User = Depends(current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(403, "Недостаточно прав")
        return user

    return dependency


ADMIN = require(Role.ADMIN)
GUARD = require(Role.GUARD, Role.ADMIN)
DAY_READERS = require(Role.GUARD, Role.ADMIN, Role.VIEWER)
ADVISOR_READERS = require(Role.ADVISOR, Role.ADMIN, Role.VIEWER)
ADVISOR_WRITERS = require(Role.ADVISOR, Role.ADMIN)
REPORT_READERS = require(Role.ADMIN, Role.VIEWER)
