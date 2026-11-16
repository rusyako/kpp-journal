from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import clock, config
from app.deps import Auth, current_auth, get_db
from app.models import User
from app.services import audit, login_limit
from app.services.advisor import visible_advisories
from app.services.auth import SESSION_COOKIE, make_session, verify_password
from app.services.calendar import is_working_day
from app.services.passwords import PasswordError, check_new_password, set_own_password, temp_password_expired

router = APIRouter(prefix="/api", tags=["auth"])


class LoginIn(BaseModel):
    username: str
    password: str


class ChangePasswordIn(BaseModel):
    # Не нужен сразу после входа с временным паролем: человек только что его ввёл
    current_password: str = ""
    new_password: str


def set_session_cookie(response: Response, user: User) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        make_session(user.id, user.session_version),
        max_age=config.SESSION_DAYS * 86400,
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite="lax",
    )


def _client_ip(request: Request) -> str:
    return request.client.host if request.client else "?"


def _check_rate_limit(ip: str, username: str) -> None:
    if wait := login_limit.retry_after(ip, username):
        minutes = (wait + 59) // 60
        raise HTTPException(429, f"Слишком много неудачных попыток. Попробуйте через {minutes} мин.",
                            headers={"Retry-After": str(wait)})


@router.post("/auth/login")
def login(body: LoginIn, request: Request, response: Response, db: Session = Depends(get_db)) -> dict:
    username = body.username.strip().lower()
    ip = _client_ip(request)
    _check_rate_limit(ip, username)
    user = db.scalar(select(User).where(User.username == username))
    if user is None or not user.active or not verify_password(body.password, user.password_hash):
        login_limit.failed(ip, username)
        raise HTTPException(401, "Неверный логин или пароль")
    if temp_password_expired(user):
        raise HTTPException(401, "Временный пароль устарел. Попросите администратора выдать новый")
    login_limit.succeeded(ip, username)
    audit.log(db, user, "login")
    db.commit()
    set_session_cookie(response, user)
    return {"ok": True, "must_change_password": user.must_change_password}


@router.post("/auth/change-password")
def change_password(
    body: ChangePasswordIn,
    request: Request,
    response: Response,
    auth: Auth = Depends(current_auth),
    db: Session = Depends(get_db),
) -> dict:
    """Сменить пароль на свой. Работает и с временным паролем — для этого он и выдан."""
    user = db.get(User, auth.user.id)
    if not user.username or not user.password_hash:
        raise HTTPException(400, "У вас вход только через Telegram — пароль не нужен")
    if not auth.needs_password_change:
        # Смена своего постоянного пароля — только зная текущий
        ip, key = _client_ip(request), user.username
        _check_rate_limit(ip, key)
        if not verify_password(body.current_password, user.password_hash):
            login_limit.failed(ip, key)
            raise HTTPException(400, "Текущий пароль введён неверно")
    try:
        check_new_password(user, body.new_password, body.current_password)
    except PasswordError as e:
        raise HTTPException(400, str(e))
    set_own_password(user, body.new_password)
    audit.log(db, user, "password_changed")
    db.commit()
    # Остальные устройства выйдут, это — остаётся в системе
    set_session_cookie(response, user)
    return {"ok": True}


@router.post("/auth/logout")
def logout(response: Response) -> dict:
    response.delete_cookie(SESSION_COOKIE)
    return {"ok": True}


@router.get("/me")
def me(auth: Auth = Depends(current_auth), db: Session = Depends(get_db)) -> dict:
    user = auth.user
    today = clock.today()
    base = {
        "id": user.id,
        "role": user.role.value,
        "display_name": user.display_name,
        "username": user.username,
        "has_password": bool(user.password_hash),
        "must_change_password": auth.needs_password_change,
        "today": today.isoformat(),
    }
    if auth.needs_password_change:
        # До смены пароля — ничего лишнего
        return {**base, "advisories": [], "working_day": False}
    return {
        **base,
        "advisories": [{"id": a.id, "name": a.name} for a in visible_advisories(db, user)],
        "working_day": is_working_day(db, today),
    }
