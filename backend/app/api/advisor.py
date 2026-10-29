"""Mini App эдвайзера: свои ученики, время и причина на сегодня."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.deps import ADVISOR_READERS, ADVISOR_WRITERS, get_db
from app.models import User
from app.services.advisor import AdvisorError, advisory_rows, can_edit, set_permission, visible_advisories

router = APIRouter(prefix="/api/advisor", tags=["advisor"])


@router.get("/advisories")
def advisories(db: Session = Depends(get_db), user: User = Depends(ADVISOR_READERS)) -> list[dict]:
    return [{"id": a.id, "name": a.name, "editable": can_edit(user, a.id)} for a in visible_advisories(db, user)]


@router.get("/advisories/{advisory_id}")
def advisory(advisory_id: int, db: Session = Depends(get_db), user: User = Depends(ADVISOR_READERS)) -> dict:
    visible = {a.id: a for a in visible_advisories(db, user)}
    if advisory_id not in visible:
        raise HTTPException(403, "Это не ваша эдвайзери")
    return {
        "id": advisory_id,
        "name": visible[advisory_id].name,
        "editable": can_edit(user, advisory_id),
        "rows": advisory_rows(db, advisory_id),
    }


class PermissionIn(BaseModel):
    time: str = ""
    reason: str = ""


@router.put("/students/{student_id}/permission")
def put_permission(
    student_id: int, body: PermissionIn, db: Session = Depends(get_db), user: User = Depends(ADVISOR_WRITERS)
) -> dict:
    try:
        return set_permission(db, user, student_id, body.time, body.reason)
    except AdvisorError as e:
        raise HTTPException(e.status, str(e))
