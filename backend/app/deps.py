from dataclasses import dataclass
from typing import Iterator, Literal

from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import config, db as database
from app.models import Role, User
from app.services.auth import SESSION_COOKIE, read_session, validate_init_data
from app.services.passwords import temp_password_expired

TG_HEADER = "X-Telegram-Init-Data"
MUST_CHANGE_PASSWORD = "Сначала смените временный пароль"


def get_db() -> Iterator[Session]:
    with database.SessionLocal() as session:
        yield session


@dataclass
class Auth:
    user: User
    via: Literal["telegram", "password"]

    @property
    def needs_password_change(self) -> bool:
        # Вход через Telegram пароль не использует — временный пароль его не ограничивает
        return self.via == "password" and self.user.must_change_password


def resolve_auth(db: Session, init_data: str | None, session_token: str | None) -> Auth | None:
    """Telegram Mini App присылает initData, браузер — cookie сессии."""
    if init_data:
        tg = validate_init_data(init_data, config.TELEGRAM_BOT_TOKEN)
        if tg and "id" in tg:
            user = db.scalar(select(User).where(User.telegram_id == int(tg["id"])))
            if user is not None and user.active:
                return Auth(user, "telegram")
    if session_token:
        session = read_session(session_token)
        if session is not None:
            uid, version = session
            user = db.get(User, uid)
            # Номер не совпал — сеанс завершён: сменили пароль или нажали «Завершить сеансы»
            if user is not None and user.active and user.session_version == version:
                if temp_password_expired(user):
                    return None
                return Auth(user, "password")
    return None


def resolve_user(db: Session, init_data: str | None, session_token: str | None) -> User | None:
    """Пользователь с полным доступом (без незаменённого временного пароля)."""
    auth = resolve_auth(db, init_data, session_token)
    return auth.user if auth is not None and not auth.needs_password_change else None


def current_auth(request: Request, db: Session = Depends(get_db)) -> Auth:
    """Вход есть, даже если пароль ещё временный: только для /me и смены пароля."""
    auth = resolve_auth(db, request.headers.get(TG_HEADER), request.cookies.get(SESSION_COOKIE))
    if auth is None:
        raise HTTPException(401, "Нужно войти")
    return auth


def current_user(auth: Auth = Depends(current_auth)) -> User:
    if auth.needs_password_change:
        raise HTTPException(403, MUST_CHANGE_PASSWORD)
    return auth.user


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
