"""Защита входа: ключ сессий, отзыв сеансов, перебор паролей, вход Mini App по WebSocket."""

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app import config
from app.importer import parse_rows
from app.main import app
from app.services.auth import make_session
from tests.conftest import PASSWORD, login, student_id
from tests.test_api import _init_data, _xlsx


# ---------- SECRET_KEY ----------


@pytest.mark.parametrize("key", ["", "dev-secret-change-me", "short-key"])
def test_api_refuses_to_start_with_weak_secret(monkeypatch, key):
    monkeypatch.setattr(config, "SECRET_KEY", key)
    assert config.secret_key_problem()
    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        with TestClient(app):
            pass


def test_strong_secret_accepted(monkeypatch):
    monkeypatch.setattr(config, "SECRET_KEY", "x" * 64)
    assert config.secret_key_problem() is None


# ---------- Отзыв сеансов ----------


def _guard_id(admin) -> int:
    return next(u["id"] for u in admin.get("/api/admin/users").json() if u["username"] == "kpp")


def _guard_body(**extra) -> dict:
    return {"role": "guard", "display_name": "Охрана", "username": "kpp", "email": "kpp@hta.kz", **extra}


def test_password_change_ends_old_sessions(db, admin, guard):
    assert guard.get("/api/me").status_code == 200
    r = admin.put(f"/api/admin/users/{_guard_id(admin)}", json=_guard_body(password="new-password-1"))
    assert r.status_code == 200
    assert guard.get("/api/me").status_code == 401
    fresh = TestClient(app)
    assert fresh.post("/api/auth/login", json={"username": "kpp", "password": "new-password-1"}).status_code == 200
    assert fresh.get("/api/me").status_code == 200


def test_revoke_sessions_flag(db, admin, guard):
    uid = _guard_id(admin)
    assert admin.put(f"/api/admin/users/{uid}", json=_guard_body()).status_code == 200
    assert guard.get("/api/me").status_code == 200  # обычное сохранение сеансы не трогает
    assert admin.put(f"/api/admin/users/{uid}", json=_guard_body(revoke_sessions=True)).status_code == 200
    assert guard.get("/api/me").status_code == 401
    assert login("kpp").get("/api/me").status_code == 200


def test_admin_changing_own_password_stays_logged_in(db, admin):
    other_device = login("admin")
    me = admin.get("/api/me").json()
    body = {"role": "admin", "display_name": "Админ", "username": "admin", "password": "new-admin-pass"}
    assert admin.put(f"/api/admin/users/{me['id']}", json=body).status_code == 200
    assert admin.get("/api/me").status_code == 200
    assert other_device.get("/api/me").status_code == 401


def test_old_cookie_format_rejected(db, guard):
    me = guard.get("/api/me").json()
    from app.services.auth import _serializer

    client = TestClient(app)
    client.cookies.set("kpp_session", _serializer.dumps({"uid": me["id"]}))
    assert client.get("/api/me").status_code == 401
    client.cookies.set("kpp_session", make_session(me["id"], 0))
    assert client.get("/api/me").status_code == 200


# ---------- Перебор паролей ----------


def test_login_rate_limit(db):
    client = TestClient(app)
    for _ in range(5):
        assert client.post("/api/auth/login", json={"username": "kpp", "password": "wrong"}).status_code == 401
    r = client.post("/api/auth/login", json={"username": "kpp", "password": PASSWORD})
    assert r.status_code == 429 and "Retry-After" in r.headers
    # Другой логин с того же адреса не заблокирован
    assert client.post("/api/auth/login", json={"username": "admin", "password": PASSWORD}).status_code == 200


def test_successful_login_resets_counter(db):
    client = TestClient(app)
    for _ in range(4):
        client.post("/api/auth/login", json={"username": "kpp", "password": "wrong"})
    assert client.post("/api/auth/login", json={"username": "kpp", "password": PASSWORD}).status_code == 200
    for _ in range(4):
        assert client.post("/api/auth/login", json={"username": "kpp", "password": "wrong"}).status_code == 401


# ---------- WebSocket Mini App ----------


def test_websocket_mini_app_auth_by_first_message(db, monkeypatch):
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "123:abc")
    with TestClient(app) as client:
        with client.websocket_connect("/api/ws") as ws:
            ws.send_text("auth:" + _init_data(1001, "123:abc"))
            ws.send_text("ping")
            guard = login("kpp")
            guard.post("/api/exits", json={"student_id": student_id(db, "Ким Илья")})
            assert ws.receive_json()["type"] == "changed"


def test_websocket_rejects_forged_and_query_init_data(db, monkeypatch):
    monkeypatch.setattr(config, "TELEGRAM_BOT_TOKEN", "123:abc")
    with TestClient(app) as client:
        with client.websocket_connect("/api/ws") as ws:
            ws.send_text("auth:" + _init_data(1001, "other-token"))
            with pytest.raises(WebSocketDisconnect) as e:
                ws.receive_json()
            assert e.value.code == 4401
        # Старый способ — initData в адресе — больше не принимается
        with client.websocket_connect("/api/ws?tg=" + _init_data(1001, "123:abc")) as ws:
            ws.send_text("ping")
            with pytest.raises(WebSocketDisconnect):
                ws.receive_json()


# ---------- Импорт: классы «Б» и «В» ----------


def test_parse_rows_blocks_b_and_v_merge():
    result = parse_rows([("Ким Илья", "5Б", ""), ("Ким Ирина", "5В", "")])
    assert result.errors and "5B" in result.errors[0]


def test_parse_rows_allows_single_cyrillic_letter():
    result = parse_rows([("Ким Илья", "5Б", ""), ("Ким Ирина", "5B", ""), ("Ли Ан", "6В", "Котики")])
    assert result.errors == []
    assert {r.class_name for r in result.rows} == {"5B", "6B"}


def test_import_with_merged_classes_refused(db, admin):
    files = {"file": ("spisok.xlsx", _xlsx([("Ким Илья", "5Б", ""), ("Ким Ирина", "5в", "")]))}
    r = admin.post("/api/admin/import", files=files, data={"apply": "true"})
    assert r.status_code == 400 and "слились" in r.json()["detail"]
