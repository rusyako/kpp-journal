from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import clock, config
from app.deps import current_user, get_db
from app.models import User
from app.services import audit, login_limit
from app.services.advisor import visible_advisories
from app.services.auth import SESSION_COOKIE, make_session, verify_password
from app.services.calendar import is_working_day

router = APIRouter(prefix="/api", tags=["auth"])


class LoginIn(BaseModel):
    username: str
    password: str


def set_session_cookie(response: Response, user: User) -> None:
    response.set_cookie(
        SESSION_COOKIE,
        make_session(user.id, user.session_version),
        max_age=config.SESSION_DAYS * 86400,
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite="lax",
    )


@router.post("/auth/login")
def login(body: LoginIn, request: Request, response: Response, db: Session = Depends(get_db)) -> dict:
    username = body.username.strip().lower()
    ip = request.client.host if request.client else "?"
    if wait := login_limit.retry_after(ip, username):
        minutes = (wait + 59) // 60
        raise HTTPException(429, f"Слишком много неудачных попыток. Попробуйте через {minutes} мин.",
                            headers={"Retry-After": str(wait)})
    user = db.scalar(select(User).where(User.username == username))
    if user is None or not user.active or not verify_password(body.password, user.password_hash):
        login_limit.failed(ip, username)
        raise HTTPException(401, "Неверный логин или пароль")
    login_limit.succeeded(ip, username)
    audit.log(db, user, "login")
    db.commit()
    set_session_cookie(response, user)
    return {"ok": True}


@router.post("/auth/logout")
def logout(response: Response) -> dict:
    response.delete_cookie(SESSION_COOKIE)
    return {"ok": True}


@router.get("/me")
def me(user: User = Depends(current_user), db: Session = Depends(get_db)) -> dict:
    today = clock.today()
    return {
        "id": user.id,
        "role": user.role.value,
        "display_name": user.display_name,
        "advisories": [{"id": a.id, "name": a.name} for a in visible_advisories(db, user)],
        "today": today.isoformat(),
        "working_day": is_working_day(db, today),
    }
