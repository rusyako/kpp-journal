"""Экран КПП: лист дня, отметка и снятие выхода, журнал действий."""

from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import clock
from app.deps import DAY_READERS, GUARD, get_db
from app.models import User
from app.services import audit
from app.services.calendar import is_working_day
from app.services.day import load_day
from app.services.exits import ExitError, cancel_exit, mark_exit

router = APIRouter(prefix="/api", tags=["kpp"])


@router.get("/day")
def day(d: date | None = None, db: Session = Depends(get_db), user: User = Depends(DAY_READERS)) -> dict:
    d = d or clock.today()
    return {
        "date": d.isoformat(),
        "today": clock.today().isoformat(),
        "working_day": is_working_day(db, d),
        "rows": [r.to_dict() for r in load_day(db, d)],
    }


class ExitIn(BaseModel):
    student_id: int
    # Заполняется только для отметок из офлайн-очереди
    client_time: datetime | None = None


def _result(fn, *args) -> dict:
    try:
        result = fn(*args)
    except ExitError as e:
        raise HTTPException(e.status, str(e))
    return {"message": result.message, "status": result.row.status, "row": result.row.to_dict()}


@router.post("/exits")
def create_exit(body: ExitIn, db: Session = Depends(get_db), user: User = Depends(GUARD)) -> dict:
    return _result(mark_exit, db, user, body.student_id, body.client_time)


@router.post("/exits/{student_id}/cancel")
def remove_exit(student_id: int, db: Session = Depends(get_db), user: User = Depends(GUARD)) -> dict:
    return _result(cancel_exit, db, user, student_id)


@router.get("/audit")
def audit_log(d: date | None = None, db: Session = Depends(get_db), user: User = Depends(DAY_READERS)) -> list[dict]:
    return audit.entries_for_day(db, d or clock.today())
