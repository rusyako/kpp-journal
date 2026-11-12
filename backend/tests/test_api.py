"""Сценарии приёмки ТЗ (раздел 11) на уровне API."""

import hashlib
import hmac
import io
import json
import time
from datetime import datetime, timedelta
from urllib.parse import urlencode

from fastapi.testclient import TestClient
from openpyxl import Workbook

from app import config
from app.config import SCHOOL_TZ
from app.main import app
from app.services.invites import create_invite, redeem_invite
from app.models import User
from tests.conftest import login, student_id


def day_rows(client: TestClient) -> list[dict]:
    r = client.get("/api/day")
    assert r.status_code == 200, r.text
    return r.json()["rows"]


def row_of(rows: list[dict], name: str) -> dict:
    return next(r for r in rows if r["full_name"] == name)


def test_roles(db):
    anon = TestClient(app)
    assert anon.get("/api/day").status_code == 401
    assert anon.post("/api/auth/login", json={"username": "kpp", "password": "wrong"}).status_code == 401

    viewer = login("director")
    assert viewer.get("/api/day").status_code == 200
    assert viewer.post("/api/exits", json={"student_id": student_id(db, "Ким Илья")}).status_code == 403

    advisor = login("kotiki")
    assert advisor.get("/api/day").status_code == 403
    assert advisor.get("/api/admin/users").status_code == 403


def test_p3_exit_without_permission(db, guard, now, sent):
    """П-3: выход без разрешения — время записано, строка внизу зелёная, сообщение ⚠️."""
    kim = student_id(db, "Ким Илья")
    now.set(15, 1)
    r = guard.post("/api/exits", json={"student_id": kim})
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "no_permission"
    assert "БЕЗ разрешения" in body["message"]
    assert body["row"]["exit_time"] == "15:01"

    rows = day_rows(guard)
    assert rows[-1]["full_name"] == "Ким Илья"
    assert rows[-1]["color"] == "green"

    # Повторная отметка не создаёт второй выход
    assert guard.post("/api/exits", json={"student_id": kim}).status_code == 409
    # Ф-16: эдвайзер Котиков узнал о выходе, даже без разрешения
    assert any(chat == 1001 and "🚪" in text and "без разрешения" in text for chat, text in sent)


def test_p5_cancel_mistaken_exit(db, guard):
    """П-5: ошибочная отметка снята — время стёрто, в журнале две записи с почтой охранника."""
    kim = student_id(db, "Ким Илья")
    guard.post("/api/exits", json={"student_id": kim})
    r = guard.post(f"/api/exits/{kim}/cancel")
    assert r.status_code == 200
    assert r.json()["row"]["exited"] is False
    assert row_of(day_rows(guard), "Ким Илья")["exit_time"] is None

    entries = [e for e in guard.get("/api/audit").json() if e["student"].startswith("Ким Илья")]
    assert [e["action"] for e in entries] == ["Снял отметку", "Отметил выход"]
    assert all(e["user"] == "kpp@hta.kz" for e in entries)

    # Снова отметить после отмены можно
    assert guard.post("/api/exits", json={"student_id": kim}).status_code == 200


def test_p6_p7_permission_then_early_exit(db, guard, advisor, now, sent):
    """П-6: эдвайзер пишет «1505» → у охраны 🟨 вверху. П-7: выход в 15:01 → 🟧, у эдвайзера «🚪 15:01»."""
    kim = student_id(db, "Ким Илья")
    r = advisor.put(f"/api/advisor/students/{kim}/permission", json={"time": "1505", "reason": "к врачу"})
    assert r.status_code == 200
    assert r.json()["status"] == "✅ 15:05 передано охране"

    first = day_rows(guard)[0]
    assert (first["full_name"], first["color"], first["allowed_time"]) == ("Ким Илья", "yellow", "15:05")

    now.set(15, 1)
    body = guard.post("/api/exits", json={"student_id": kim}).json()
    assert body["status"] == "early"
    assert "РАНЬШЕ разрешённого времени" in body["message"]
    assert row_of(day_rows(guard), "Ким Илья")["color"] == "orange"

    advisory_id = body["row"]["advisory_id"]
    adv_row = row_of(advisor.get(f"/api/advisor/advisories/{advisory_id}").json()["rows"], "Ким Илья")
    assert adv_row["exit"] == "🚪 15:01"
    assert adv_row["color"] == "green" and adv_row["early"] is True
    assert any(chat == 1001 and "раньше разрешённых 15:05" in text for chat, text in sent)


def test_exit_on_time(db, guard, advisor, now):
    kim = student_id(db, "Ким Илья")
    advisor.put(f"/api/advisor/students/{kim}/permission", json={"time": "15:05"})
    now.set(15, 10)
    body = guard.post("/api/exits", json={"student_id": kim}).json()
    assert body["status"] == "ok"
    assert body["message"].startswith("✅")


def test_p8_clear_and_unrecognized_time(db, guard, advisor):
    """П-8: стёртое время снимает подсветку; «абв» → «⚠️ время не распознано»."""
    kim = student_id(db, "Ким Илья")
    irina = student_id(db, "Ким Ирина")
    advisor.put(f"/api/advisor/students/{kim}/permission", json={"time": "1505"})
    r = advisor.put(f"/api/advisor/students/{kim}/permission", json={"time": ""})
    assert r.json()["status"] == ""
    row = row_of(day_rows(guard), "Ким Илья")
    assert row["allowed_time"] is None and row["color"] == ""

    r = advisor.put(f"/api/advisor/students/{irina}/permission", json={"time": "абв"})
    assert r.json()["status"] == "⚠️ время не распознано"
    assert r.json()["time"] == "абв"
    assert row_of(day_rows(guard), "Ким Ирина")["color"] == ""


def test_advisor_sees_only_own_advisory(db, advisor):
    """Закрывает риск «эдвайзер записал время в чужой вкладке»."""
    names = [a["name"] for a in advisor.get("/api/advisor/advisories").json()]
    assert names == ["Котики"]
    foreign = student_id(db, "Сейітов Ақтілек")
    assert advisor.put(f"/api/advisor/students/{foreign}/permission", json={"time": "15:00"}).status_code == 403
    barsy = login("barsy").get("/api/advisor/advisories").json()[0]["id"]
    assert advisor.get(f"/api/advisor/advisories/{barsy}").status_code == 403


def test_sort_order_f18(db, guard, advisor, now):
    """Ф-18: 🟨 по времени → остальные по алфавиту → вышедшие по времени выхода."""
    ids = {n: student_id(db, n) for n in ["Ким Илья", "Ким Ирина", "Гарамов Ислам", "Ахметов Арман"]}
    advisor.put(f"/api/advisor/students/{ids['Ким Ирина']}/permission", json={"time": "16:00"})
    advisor.put(f"/api/advisor/students/{ids['Ким Илья']}/permission", json={"time": "15:00"})
    now.set(14, 30)
    guard.post("/api/exits", json={"student_id": ids["Гарамов Ислам"]})
    now.set(14, 10)
    guard.post("/api/exits", json={"student_id": ids["Ахметов Арман"]})

    names = [r["full_name"] for r in day_rows(guard)]
    assert names[:2] == ["Ким Илья", "Ким Ирина"]
    assert names[-2:] == ["Ахметов Арман", "Гарамов Ислам"]
    assert names[2:-2] == ["Ахметова Дана", "Сейітов Ақтілек"]


def test_offline_queue_time(db, guard, now):
    kim = student_id(db, "Ким Илья")
    now.set(15, 30)
    earlier = now.value.replace(hour=15, minute=12).isoformat()
    body = guard.post("/api/exits", json={"student_id": kim, "client_time": earlier}).json()
    assert body["row"]["exit_time"] == "15:12" and body["row"]["exit_offline"] is True

    yesterday = (now.value - timedelta(days=1)).isoformat()
    r = guard.post("/api/exits", json={"student_id": student_id(db, "Ким Ирина"), "client_time": yesterday})
    assert r.status_code == 422


def test_p11_report(db, guard, advisor, admin, now, sent):
    """П-11: числа сводки совпадают с листом дня; отчёт уходит руководству."""
    s = {n: student_id(db, n) for n in ["Ким Илья", "Ким Ирина", "Гарамов Ислам", "Ахметов Арман", "Ахметова Дана"]}
    advisor.put(f"/api/advisor/students/{s['Ким Илья']}/permission", json={"time": "15:00", "reason": "кружок"})
    advisor.put(f"/api/advisor/students/{s['Ким Ирина']}/permission", json={"time": "15:00"})
    advisor.put(f"/api/advisor/students/{s['Гарамов Ислам']}/permission", json={"time": "16:00"})
    now.set(14, 50)
    guard.post("/api/exits", json={"student_id": s["Ким Илья"]})  # раньше
    now.set(15, 5)
    guard.post("/api/exits", json={"student_id": s["Ким Ирина"]})  # вовремя
    guard.post("/api/exits", json={"student_id": s["Ахметов Арман"]})  # без разрешения
    guard.post("/api/exits", json={"student_id": s["Ахметова Дана"]})
    guard.post(f"/api/exits/{s['Ахметова Дана']}/cancel")  # снята

    report = admin.get(f"/api/reports/{now.value.date().isoformat()}").json()
    assert report["summary"] == {
        "total": 6, "exited": 3, "early": 1, "no_permission": 1, "allowed_not_exited": 1,
    }
    lists = {lst["key"]: [r["full_name"] for r in lst["rows"]] for lst in report["lists"]}
    assert lists == {
        "early": ["Ким Илья"],
        "no_permission": ["Ахметов Арман"],
        "allowed_not_exited": ["Гарамов Ислам"],
        "ok": ["Ким Ирина"],
        "cancelled": ["Ахметова Дана"],
    }
    html = admin.get(f"/api/reports/{now.value.date().isoformat()}/html").text
    assert "Отчёт КПП за 29.10.2026" in html and "кружок" in html
    assert "<span>Не вышли</span>" not in html
    assert "С разрешением, но не вышли" in html

    sent.clear()
    r = admin.post(f"/api/admin/reports/{now.value.date().isoformat()}/send")
    assert r.json()["telegram"] == 1
    assert sent[0][0] == 2001 and "Раньше времени: 1" in sent[0][1]
    assert "\nНе вышли:" not in sent[0][1]
    assert "С разрешением, но не вышли: 1" in sent[0][1]


def _init_data(user_id: int, token: str) -> str:
    fields = {"auth_date": str(int(time.time())), "user": json.dumps({"id": user_id, "first_name": "A"})}
    check = "\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
    secret = hmac.new(b"WebAppData", token.encode(), hashlib.sha256).digest()
    fields["hash"] = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    return urlencode(fields)


def test_telegram_mini_app_auth(db, monkeypatch):
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "123:abc")
    client = TestClient(app)
    r = client.get("/api/me", headers={"X-Telegram-Init-Data": _init_data(1001, "123:abc")})
    assert r.status_code == 200 and r.json()["role"] == "advisor"
    assert [a["name"] for a in r.json()["advisories"]] == ["Котики"]

    forged = _init_data(1001, "other-token")
    assert client.get("/api/me", headers={"X-Telegram-Init-Data": forged}).status_code == 401


def test_invite_binds_telegram(db, now):
    user = db.query(User).filter_by(username="director").one()
    invite = create_invite(db, user)
    assert redeem_invite(db, invite["code"], 5555).id == user.id
    assert redeem_invite(db, invite["code"], 6666) is None  # одноразовый

    old = create_invite(db, user)
    now.value = now.value + timedelta(days=8)
    assert redeem_invite(db, old["code"], 7777) is None  # устарел


def test_websocket_notifies_guard(db):
    with TestClient(app) as client:
        client.post("/api/auth/login", json={"username": "kpp", "password": "test-pass-123"})
        with client.websocket_connect("/api/ws") as ws:
            client.post("/api/exits", json={"student_id": student_id(db, "Ким Илья")})
            event = ws.receive_json()
    assert event["type"] == "changed" and event["student_id"] == student_id(db, "Ким Илья")


def _xlsx(rows: list[tuple]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Для журнала"
    ws.append(["ФИО", "Класс", "Эдвайзери"])
    for r in rows:
        ws.append(list(r))
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


def test_p13_import_preview_and_apply(db, admin, advisor):
    """П-13: новенький появляется у своей эдвайзери, записанное время других детей на месте."""
    kim = student_id(db, "Ким Илья")
    advisor.put(f"/api/advisor/students/{kim}/permission", json={"time": "15:05"})

    content = _xlsx([
        ("Ким Илья", "7A", "КОТИКИ"), ("Ким Ирина", "8B", "Котики"), ("Гарамов Ислам", "9A", "Котики"),
        ("Ахметов Арман", "1A", "1A"), ("Ахметова Дана", "1A", ""), ("Сейітов Ақтілек", "10A", "Барсы"),
        ("Новенький  Тимур", "7A", "котики"),
    ])
    files = {"file": ("spisok.xlsx", content)}
    preview = admin.post("/api/admin/import", files=files, data={"apply": "false"}).json()
    assert preview["diff"]["added"] == ["Новенький Тимур (7A, Котики)"]
    assert admin.get("/api/admin/students").json().__len__() == 6

    applied = admin.post("/api/admin/import", files=files, data={"apply": "true"}).json()
    assert applied["applied"] is True
    advisory_id = advisor.get("/api/advisor/advisories").json()[0]["id"]
    rows = advisor.get(f"/api/advisor/advisories/{advisory_id}").json()["rows"]
    assert "Новенький Тимур" in [r["full_name"] for r in rows]
    assert row_of(rows, "Ким Илья")["time"] == "15:05"


def test_admin_users_and_health(db, admin):
    r = admin.post("/api/admin/users", json={
        "role": "guard", "display_name": "Охрана 2", "username": "KPP2", "password": "long-password",
    })
    assert r.status_code == 200 and r.json()["username"] == "kpp2"
    assert login_ok("kpp2", "long-password")
    assert admin.post("/api/admin/users", json={"role": "guard", "display_name": "X", "username": "kpp2"}).status_code == 409

    checks = {c["name"]: c for c in admin.get("/api/admin/health").json()}
    assert checks["Список учеников загружен"]["ok"] is True
    assert checks["У каждой эдвайзери есть эдвайзер"]["ok"] is False  # у 1A нет эдвайзера
    assert "1A" in checks["У каждой эдвайзери есть эдвайзер"]["detail"]


def login_ok(username: str, password: str) -> bool:
    return TestClient(app).post("/api/auth/login", json={"username": username, "password": password}).status_code == 200


def test_school_calendar(db, admin, now):
    sunday = datetime(2026, 11, 1, tzinfo=SCHOOL_TZ).date()
    admin.put(f"/api/admin/school-days/{sunday}", json={"is_working": True, "note": "отработка"})
    now.value = datetime(2026, 11, 1, 9, 0, tzinfo=SCHOOL_TZ)
    assert admin.get("/api/me").json()["working_day"] is True
    now.value = datetime(2026, 11, 8, 9, 0, tzinfo=SCHOOL_TZ)
    assert admin.get("/api/me").json()["working_day"] is False
