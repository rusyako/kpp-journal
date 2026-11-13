"""Экран пилота Hikvision — только администратор.

Здесь НЕТ и не должно быть команды открытия двери/турникета. Браузер не управляет проходом:
открыть может только ответ «success» на конкретный запрос терминала, привязанный к событию распознавания.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app import clock
from app.deps import ADMIN, get_db
from app.models import User
from app.services import pilot
from app.services.release import PassageError, confirm_passage_manually, permission_status

router = APIRouter(prefix="/api/pilot", tags=["pilot"])


def _call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except pilot.PilotError as e:
        raise HTTPException(e.status, str(e))
    except PassageError as e:
        raise HTTPException(409, str(e))


@router.get("/status")
def status(db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    return pilot.dashboard(db)


@router.post("/setup")
def setup(db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    return pilot.ensure_setup(db, user)


class EnabledIn(BaseModel):
    enabled: bool


@router.post("/enabled")
def enabled(body: EnabledIn, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    return {"enabled": pilot.set_enabled(db, user, body.enabled)}


class PermissionIn(BaseModel):
    employee_no: str = Field(min_length=1, max_length=32)
    valid_from: datetime
    valid_until: datetime
    single_use: bool = True
    note: str = Field(default="", max_length=500)


@router.post("/permissions")
def create_permission(body: PermissionIn, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    perm = _call(pilot.create_permission, db, user, body.employee_no, body.valid_from, body.valid_until,
                 body.single_use, body.note)
    return pilot.permission_dict(perm, clock.now())


@router.post("/permissions/{permission_id}/revoke")
def revoke_permission(permission_id: int, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    perm = _call(pilot.revoke_permission, db, user, permission_id)
    return {"id": perm.id, "status": permission_status(perm, clock.now())}


class SimulateIn(BaseModel):
    device_key: str = Field(default=pilot.SIM_EXIT, max_length=50)
    employee_no: str = Field(default="", max_length=32)
    scenario: str = "face"


@router.post("/simulate")
def simulate(body: SimulateIn, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    return _call(pilot.simulate, db, user, body.device_key, body.employee_no.strip(), body.scenario)


class SimPassageIn(BaseModel):
    decision_id: int
    outcome: str = "passed"


@router.post("/simulate/passage")
def simulate_passage(body: SimPassageIn, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    return _call(pilot.simulate_passage, db, user, body.decision_id, body.outcome)


class ConfirmIn(BaseModel):
    passed: bool


@router.post("/decisions/{decision_id}/confirm")
def confirm(decision_id: int, body: ConfirmIn, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    """Ручная отметка «прошёл / не прошёл» по уже выданному ALLOW. Дверью не управляет."""
    p = _call(confirm_passage_manually, db, user, decision_id, body.passed)
    return {"decision_id": decision_id, "outcome": p.outcome}


@router.post("/devices/{device_key}/refresh")
def refresh_device(device_key: str, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    """Только чтение: userType тестовой записи и проверка поддержки visitor-only Remote Verification."""
    return _call(pilot.refresh_device, db, user, device_key)


class UserTypeIn(BaseModel):
    device_key: str = Field(default=pilot.SIM_EXIT, max_length=50)
    to: str
    apply: bool = False
    confirm: str | None = Field(default=None, max_length=80)


@router.post("/simulate/user-type")
def simulate_user_type(body: UserTypeIn, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    """Смена userType тестовой записи на ВИРТУАЛЬНОМ терминале (DRY_RUN по умолчанию)."""
    if body.to not in ("normal", "visitor"):
        raise HTTPException(400, "to: normal | visitor")
    return _call(pilot.simulate_user_type, db, user, body.device_key, body.to, body.apply, body.confirm)


@router.post("/devices/{device_key}/check")
def check_device(device_key: str, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    """Read-only: GET /ISAPI/System/deviceInfo."""
    return _call(pilot.check_device, db, user, device_key)
