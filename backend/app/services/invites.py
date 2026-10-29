"""Привязка Telegram к пользователю по одноразовому коду (вместо «личной ссылки», Ф-17)."""

import secrets
from datetime import timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import clock, config
from app.config import SCHOOL_TZ
from app.models import Invite, User

INVITE_DAYS = 7


def create_invite(db: Session, user: User) -> dict:
    code = secrets.token_urlsafe(16)
    expires = clock.now() + timedelta(days=INVITE_DAYS)
    db.add(Invite(code=code, user_id=user.id, expires_at=expires))
    db.commit()
    link = f"https://t.me/{config.TELEGRAM_BOT_USERNAME}?start={code}" if config.TELEGRAM_BOT_USERNAME else None
    return {"code": code, "link": link, "expires_at": expires.isoformat()}


def redeem_invite(db: Session, code: str, telegram_id: int) -> User | None:
    invite = db.get(Invite, code)
    if invite is None or invite.used_at is not None:
        return None
    expires = invite.expires_at if invite.expires_at.tzinfo else invite.expires_at.replace(tzinfo=SCHOOL_TZ)
    if expires < clock.now():
        return None
    user = db.get(User, invite.user_id)
    if user is None or not user.active:
        return None
    # Этот Telegram мог быть привязан к другому пользователю — отвязываем
    for other in db.scalars(select(User).where(User.telegram_id == telegram_id, User.id != user.id)):
        other.telegram_id = None
    db.flush()
    user.telegram_id = telegram_id
    invite.used_at = clock.now()
    db.commit()
    return user
