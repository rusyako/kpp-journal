from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import clock, config
from app.deps import current_user, get_db
from app.models import User
from app.services import audit
from app.services.advisor import visible_advisories
from app.services.auth import SESSION_COOKIE, make_session, verify_password
from app.services.calendar import is_working_day

router = APIRouter(prefix="/api", tags=["auth"])


class LoginIn(BaseModel):
    username: str
    password: str


@router.post("/auth/login")
def login(body: LoginIn, response: Response, db: Session = Depends(get_db)) -> dict:
    user = db.scalar(select(User).where(User.username == body.username.strip().lower()))
    if user is None or not user.active or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Неверный логин или пароль")
    audit.log(db, user, "login")
    db.commit()
    response.set_cookie(
        SESSION_COOKIE,
        make_session(user.id),
        max_age=config.SESSION_DAYS * 86400,
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite="lax",
    )
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
