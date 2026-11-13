"""Админка: список учеников, пользователи, календарь, отчёты, проверка системы."""

import io
from datetime import date

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import clock, config, scheduler
from app.api.auth import set_session_cookie
from app.deps import ADMIN, REPORT_READERS, get_db
from app.importer import ImportDiff, advisory_kind, apply_import, clean_class, clean_name, parse_rows, read_xlsx
from app.models import Advisory, AuditLog, Role, SchoolDay, Student, User
from app.services import audit
from app.services.auth import hash_password
from app.services.invites import create_invite
from app.services.normalize import normalize
from app.services.report import build_report, render_html, render_xlsx, send_report

router = APIRouter(prefix="/api", tags=["admin"])


# ---------- Загрузка списка (Ф-22) ----------


def _diff_dict(diff: ImportDiff) -> dict:
    return {
        "added": [f"{r.full_name} ({r.class_name}, {r.advisory})" for r in diff.added],
        "moved": [f"{r.full_name} → {r.class_name}" for _, r in diff.moved],
        "advisory_changed": [f"{r.full_name} → {r.advisory}" for _, r in diff.advisory_changed],
        "reactivated": [f"{r.full_name} ({r.class_name})" for _, r in diff.reactivated],
        "removed": [f"{s.full_name} ({s.class_name})" for s in diff.removed],
        "new_advisories": diff.new_advisories,
        "removed_advisories": diff.removed_advisories,
        "empty": diff.is_empty,
    }


@router.post("/admin/import")
async def import_list(
    file: UploadFile = File(...),
    apply: bool = Form(False),
    db: Session = Depends(get_db),
    user: User = Depends(ADMIN),
) -> dict:
    """Без apply — только предпросмотр: изменения откатываются."""
    content = await file.read()
    try:
        raw = read_xlsx(io.BytesIO(content))
    except Exception:
        raise HTTPException(400, "Не удалось прочитать файл. Нужен .xlsx с листом «Для журнала»")
    parsed = parse_rows(raw)
    if parsed.errors:
        raise HTTPException(400, "Список не загружен. " + " ".join(parsed.errors))
    if not parsed.rows:
        raise HTTPException(400, "В файле нет ни одного ученика")
    diff = apply_import(db, parsed.rows)
    if apply:
        audit.log(db, user, "import", students=len(parsed.rows), added=len(diff.added), removed=len(diff.removed))
        db.commit()
    else:
        db.rollback()
    return {"applied": apply, "students": len(parsed.rows), "warnings": parsed.warnings, "diff": _diff_dict(diff)}


# ---------- Ученики: точечные правки (Ф-23) ----------


class StudentIn(BaseModel):
    full_name: str
    class_name: str
    advisory_id: int | None = None
    active: bool = True


def _student_dict(s: Student) -> dict:
    return {
        "id": s.id,
        "full_name": s.full_name,
        "class_name": s.class_name,
        "advisory_id": s.advisory_id,
        "advisory": s.advisory.name,
        "active": s.active,
    }


@router.get("/admin/students")
def list_students(db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> list[dict]:
    students = db.scalars(select(Student).join(Advisory).order_by(Advisory.sort_order, Student.full_name_norm))
    return [_student_dict(s) for s in students]


def _resolve_student_fields(db: Session, body: StudentIn) -> tuple[str, str, Advisory]:
    name = clean_name(body.full_name)
    class_name = clean_class(body.class_name)
    if not name or class_name is None:
        raise HTTPException(400, "Проверьте ФИО и класс (например 7A, Alpha α1, CDC)")
    if advisory_kind(class_name).value != "group":
        # 1–5 классы, Alpha, CDC: эдвайзери равна классу
        advisory = db.scalar(select(Advisory).where(Advisory.name == class_name))
        if advisory is None:
            advisory = Advisory(name=class_name, kind=advisory_kind(class_name), sort_order=0)
            db.add(advisory)
            db.flush()
    else:
        advisory = db.get(Advisory, body.advisory_id) if body.advisory_id else None
        if advisory is None:
            raise HTTPException(400, "Для 6–12 классов выберите эдвайзери из списка")
    advisory.active = True
    return name, class_name, advisory


@router.post("/admin/students")
def create_student(body: StudentIn, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    name, class_name, advisory = _resolve_student_fields(db, body)
    if db.scalar(select(Student).where(Student.full_name == name, Student.class_name == class_name)):
        raise HTTPException(409, "Такой ученик уже есть")
    s = Student(full_name=name, full_name_norm=normalize(name), class_name=class_name, advisory=advisory)
    db.add(s)
    db.commit()
    return _student_dict(s)


@router.put("/admin/students/{student_id}")
def update_student(
    student_id: int, body: StudentIn, db: Session = Depends(get_db), user: User = Depends(ADMIN)
) -> dict:
    s = db.get(Student, student_id)
    if s is None:
        raise HTTPException(404, "Ученик не найден")
    name, class_name, advisory = _resolve_student_fields(db, body)
    s.full_name, s.full_name_norm, s.class_name, s.advisory, s.active = (
        name, normalize(name), class_name, advisory, body.active,
    )
    db.commit()
    return _student_dict(s)


@router.get("/admin/advisories")
def list_advisories(db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> list[dict]:
    counts = dict(
        db.execute(select(Student.advisory_id, func.count()).where(Student.active).group_by(Student.advisory_id)).all()
    )
    result = []
    for a in db.scalars(select(Advisory).where(Advisory.active).order_by(Advisory.sort_order, Advisory.name)):
        advisors = db.scalars(select(User).where(User.advisories.contains(a), User.active)).all()
        result.append(
            {
                "id": a.id,
                "name": a.name,
                "kind": a.kind.value,
                "students": counts.get(a.id, 0),
                "advisors": [{"name": u.display_name, "telegram": u.telegram_id is not None} for u in advisors],
            }
        )
    return result


# ---------- Пользователи и приглашения ----------


class UserIn(BaseModel):
    role: Role
    display_name: str
    username: str | None = None
    password: str | None = None
    email: str | None = None
    advisory_ids: list[int] = []
    receives_report: bool = False
    active: bool = True
    unlink_telegram: bool = False
    revoke_sessions: bool = False


def _user_dict(u: User) -> dict:
    return {
        "id": u.id,
        "role": u.role.value,
        "display_name": u.display_name,
        "username": u.username,
        "email": u.email,
        "has_password": bool(u.password_hash),
        "telegram": u.telegram_id is not None,
        "advisory_ids": [a.id for a in u.advisories],
        "receives_report": u.receives_report,
        "active": u.active,
    }


def _apply_user(db: Session, u: User, body: UserIn) -> None:
    u.role = body.role
    u.display_name = body.display_name.strip()
    u.username = body.username.strip().lower() if body.username else None
    u.email = body.email.strip().lower() if body.email else None
    if body.password:
        if len(body.password) < 8:
            raise HTTPException(400, "Пароль — не короче 8 символов")
        u.password_hash = hash_password(body.password)
        u.revoke_sessions()  # старый пароль мог утечь — выходим со всех устройств
    if body.revoke_sessions:
        u.revoke_sessions()
    # Без автосброса: занятый логин должен всплыть в _commit_user как 409, а не здесь
    with db.no_autoflush:
        u.advisories = list(db.scalars(select(Advisory).where(Advisory.id.in_(body.advisory_ids))))
    u.receives_report = body.receives_report
    u.active = body.active
    if body.unlink_telegram:
        u.telegram_id = None


def _commit_user(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Логин или почта уже заняты")


@router.get("/admin/users")
def list_users(db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> list[dict]:
    return [_user_dict(u) for u in db.scalars(select(User).order_by(User.role, User.display_name))]


@router.post("/admin/users")
def create_user(body: UserIn, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    u = User(role=body.role, display_name=body.display_name)
    db.add(u)
    _apply_user(db, u, body)
    _commit_user(db)
    return _user_dict(u)


@router.put("/admin/users/{user_id}")
def update_user(
    user_id: int, body: UserIn, response: Response, db: Session = Depends(get_db), user: User = Depends(ADMIN)
) -> dict:
    u = db.get(User, user_id)
    if u is None:
        raise HTTPException(404, "Пользователь не найден")
    if u.id == user.id and (body.role is not Role.ADMIN or not body.active):
        raise HTTPException(400, "Нельзя снять права администратора с самого себя")
    _apply_user(db, u, body)
    _commit_user(db)
    if u.id == user.id:
        # Свои остальные сеансы завершены, а этот продолжает работать
        set_session_cookie(response, u)
    return _user_dict(u)


@router.post("/admin/users/{user_id}/invite")
def invite_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    u = db.get(User, user_id)
    if u is None:
        raise HTTPException(404, "Пользователь не найден")
    return create_invite(db, u)


# ---------- Календарь ----------


class SchoolDayIn(BaseModel):
    is_working: bool
    note: str = ""


@router.get("/admin/school-days")
def list_school_days(db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> list[dict]:
    days = db.scalars(select(SchoolDay).where(SchoolDay.date >= clock.today()).order_by(SchoolDay.date))
    return [{"date": d.date.isoformat(), "is_working": d.is_working, "note": d.note or ""} for d in days]


@router.put("/admin/school-days/{d}")
def put_school_day(d: date, body: SchoolDayIn, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    day = db.get(SchoolDay, d) or SchoolDay(date=d)
    day.is_working, day.note = body.is_working, body.note.strip()
    db.add(day)
    db.commit()
    return {"ok": True}


@router.delete("/admin/school-days/{d}")
def delete_school_day(d: date, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    day = db.get(SchoolDay, d)
    if day:
        db.delete(day)
        db.commit()
    return {"ok": True}


# ---------- Отчёты (Ф-19) ----------


@router.get("/reports/{d}")
def report_json(d: date, db: Session = Depends(get_db), user: User = Depends(REPORT_READERS)) -> dict:
    return build_report(db, d)


@router.get("/reports/{d}/html", response_class=HTMLResponse)
def report_html(d: date, db: Session = Depends(get_db), user: User = Depends(REPORT_READERS)) -> str:
    return render_html(build_report(db, d))


@router.get("/reports/{d}/xlsx")
def report_xlsx(d: date, db: Session = Depends(get_db), user: User = Depends(REPORT_READERS)) -> Response:
    return Response(
        content=render_xlsx(build_report(db, d)),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": f'attachment; filename="otchet_{d.isoformat()}.xlsx"',
            "Cache-Control": "no-store",
        },
    )


@router.post("/admin/reports/{d}/send")
def report_send(d: date, db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> dict:
    return send_report(db, d)


# ---------- Проверка системы (вместо «🩺 Проверить и починить», Ф-25) ----------


@router.get("/admin/health")
def health(db: Session = Depends(get_db), user: User = Depends(ADMIN)) -> list[dict]:
    checks = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    students = db.scalar(select(func.count()).select_from(Student).where(Student.active))
    check("Список учеников загружен", students > 0, f"{students} учеников")

    empty = db.scalars(
        select(Advisory.name).where(Advisory.active, ~Advisory.students.any(Student.active))
    ).all()
    check("Нет пустых эдвайзери", not empty, ", ".join(empty))

    no_advisor = [
        a.name
        for a in db.scalars(select(Advisory).where(Advisory.active).order_by(Advisory.sort_order))
        if not db.scalar(select(func.count()).select_from(User).where(User.advisories.contains(a), User.active))
    ]
    check("У каждой эдвайзери есть эдвайзер", not no_advisor, ", ".join(no_advisor))

    unlinked = db.scalars(
        select(User.display_name).where(User.role == Role.ADVISOR, User.active, User.telegram_id.is_(None))
    ).all()
    check("Эдвайзеры подключили Telegram", not unlinked, ", ".join(unlinked))

    guards = db.scalar(select(func.count()).select_from(User).where(User.role == Role.GUARD, User.active))
    check("Есть учётная запись охраны", guards > 0, f"{guards}")

    check("Telegram-бот настроен", bool(config.TELEGRAM_BOT_TOKEN and config.TELEGRAM_BOT_USERNAME),
          f"@{config.TELEGRAM_BOT_USERNAME}" if config.TELEGRAM_BOT_USERNAME else "нет TELEGRAM_BOT_TOKEN / USERNAME")

    sched = scheduler.status()
    check("Расписание отчёта работает", sched["running"], sched["next_report"] or "планировщик выключен")

    receivers = db.scalar(
        select(func.count()).select_from(User).where(User.receives_report, User.active, User.telegram_id.is_not(None))
    )
    check("Есть кому отправлять отчёт", receivers > 0 or bool(config.REPORT_EMAILS and config.SMTP_HOST),
          f"Telegram: {receivers}, почта: {', '.join(config.REPORT_EMAILS) or '—'}")

    last = db.scalar(select(AuditLog).where(AuditLog.action == "report_sent").order_by(AuditLog.ts.desc()))
    check("Последний отчёт", last is not None, last.payload.get("date", "") if last else "ещё не отправлялся")
    return checks
