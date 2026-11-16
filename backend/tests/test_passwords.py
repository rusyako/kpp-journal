"""Временный пароль от администратора → свой пароль при первом входе."""

from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app import config
from app.main import app
from app.models import User
from app.services.passwords import PasswordError, check_new_password
from tests.conftest import PASSWORD, login, student_id
from tests.test_api import _init_data


def _user_id(admin, username: str) -> int:
    return next(u["id"] for u in admin.get("/api/admin/users").json() if u["username"] == username)


def _temp_login(admin, username: str) -> tuple[TestClient, str]:
    temp = admin.post(f"/api/admin/users/{_user_id(admin, username)}/reset-password").json()["temp_password"]
    client = TestClient(app)
    r = client.post("/api/auth/login", json={"username": username, "password": temp})
    assert r.status_code == 200 and r.json()["must_change_password"] is True
    return client, temp


def test_new_user_gets_qwerty_temp_password(db, admin):
    r = admin.post("/api/admin/users", json={"role": "guard", "display_name": "Охрана 3", "username": "kpp3"}).json()
    assert r["temp_password"] == "Qwerty123!" and r["password_status"] == "temp"
    client = TestClient(app)
    login_r = client.post("/api/auth/login", json={"username": "kpp3", "password": "Qwerty123!"})
    assert login_r.status_code == 200 and login_r.json()["must_change_password"] is True
    assert client.get("/api/me").json()["must_change_password"] is True


def test_temp_password_gives_access_only_to_password_change(db, admin):
    client, temp = _temp_login(admin, "kpp")
    me = client.get("/api/me").json()
    assert me["must_change_password"] is True and me["advisories"] == []
    assert client.get("/api/day").status_code == 403
    assert client.post("/api/exits", json={"student_id": student_id(db, "Ким Илья")}).status_code == 403
    assert client.get("/api/day").json()["detail"] == "Сначала смените временный пароль"

    r = client.post("/api/auth/change-password", json={"current_password": temp, "new_password": "Охрана на посту 2026"})
    assert r.status_code == 200, r.text
    assert client.get("/api/me").json()["must_change_password"] is False
    assert client.get("/api/day").status_code == 200

    status = next(u for u in admin.get("/api/admin/users").json() if u["username"] == "kpp")["password_status"]
    assert status == "set"
    # Временный больше не работает, свой — работает
    assert TestClient(app).post("/api/auth/login", json={"username": "kpp", "password": temp}).status_code == 401
    assert TestClient(app).post("/api/auth/login", json={"username": "kpp", "password": "Охрана на посту 2026"}).status_code == 200


def test_temp_password_expires(db, admin, now):
    uid = _user_id(admin, "kpp")
    temp = admin.post(f"/api/admin/users/{uid}/reset-password").json()["temp_password"]
    client = TestClient(app)
    assert client.post("/api/auth/login", json={"username": "kpp", "password": temp}).status_code == 200
    now.value = now.value + timedelta(hours=73)
    assert client.get("/api/me").status_code == 401  # и вошедший по нему выкинут
    r = TestClient(app).post("/api/auth/login", json={"username": "kpp", "password": temp})
    assert r.status_code == 401 and "устарел" in r.json()["detail"]
    assert next(u for u in admin.get("/api/admin/users").json() if u["id"] == uid)["password_status"] == "expired"


@pytest.mark.parametrize(
    ("new", "error"),
    [
        ("short", "не короче"),
        ("Qwerty123!", "отличаться"),
        ("qwerty123!", "отличаться"),
        ("1q2w3e4r5t", "простой"),
        ("aaaaaaaaaaaa", "простой"),
        ("my-kpp-password", "логин"),
    ],
)
def test_weak_new_passwords_rejected(db, admin, new, error):
    client, temp = _temp_login(admin, "kpp")
    r = client.post("/api/auth/change-password", json={"current_password": temp, "new_password": new})
    assert r.status_code == 400 and error in r.json()["detail"]
    assert client.get("/api/me").json()["must_change_password"] is True


def test_new_password_must_differ_from_temp():
    user = User(username="kpp")
    with pytest.raises(PasswordError, match="отличаться"):
        check_new_password(user, "Qwerty123!", "Qwerty123!")


def test_first_change_does_not_ask_temp_password_again(db, admin):
    client, _ = _temp_login(admin, "kpp")
    r = client.post("/api/auth/change-password", json={"new_password": "Охрана на посту 2026"})
    assert r.status_code == 200, r.text
    assert client.get("/api/day").status_code == 200


def test_change_password_requires_current(db, guard):
    r = guard.post("/api/auth/change-password", json={"current_password": "wrong", "new_password": "новый длинный пароль"})
    assert r.status_code == 400 and "неверно" in r.json()["detail"]


def test_admin_cannot_set_password_directly(db, admin):
    uid = _user_id(admin, "kpp")
    body = {"role": "guard", "display_name": "Охрана", "username": "kpp", "password": "admin-chosen-pass"}
    assert admin.put(f"/api/admin/users/{uid}", json=body).status_code == 200
    assert TestClient(app).post("/api/auth/login", json={"username": "kpp", "password": "admin-chosen-pass"}).status_code == 401
    assert login("kpp").get("/api/me").status_code == 200  # старый пароль не тронут


def test_admin_cannot_reset_own_password(db, admin):
    me = admin.get("/api/me").json()
    assert admin.post(f"/api/admin/users/{me['id']}/reset-password").status_code == 400


def test_new_user_without_login_gets_no_password(db, admin):
    r = admin.post("/api/admin/users", json={"role": "advisor", "display_name": "Только Telegram"}).json()
    assert "temp_password" not in r and r["password_status"] == "none"


def test_telegram_login_not_blocked_by_temp_password(db, admin, monkeypatch):
    """Эдвайзер с временным паролем всё равно работает в Mini App: Telegram пароль не использует."""
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "123:abc")
    admin.post(f"/api/admin/users/{_user_id(admin, 'kotiki')}/reset-password")
    headers = {"X-Telegram-Init-Data": _init_data(1001, "123:abc")}
    client = TestClient(app)
    assert client.get("/api/me", headers=headers).json()["must_change_password"] is False
    assert client.get("/api/advisor/advisories", headers=headers).status_code == 200


def test_audit_shows_reset_but_not_the_password(db, admin):
    """В журнале действий виден факт выдачи, но не сам пароль."""
    temp = admin.post(f"/api/admin/users/{_user_id(admin, 'kpp')}/reset-password").json()["temp_password"]
    log = login("director").get("/api/audit").json()
    assert any(e["action"] == "Выдал временный пароль" for e in log)
    assert temp not in str(log)
    assert "Qwerty" not in str(log)
