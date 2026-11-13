"""Экран пилота (API администратора) и отдельный приёмник терминалов (gateway)."""

import time
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app import clock
from app.hikvision_gateway import app as gateway_app
from app.integrations.hikvision import adapter as hik_adapter
from app.integrations.hikvision.mock_device import MockHikvisionDevice
from app.main import app
from app.models import HikCommand, HikDevice, HikDirection, ReleaseDecision, ReleasePermission
from tests.conftest import login

PILOT_NO = "3818077855"


@pytest.fixture(autouse=True)
def simulation(monkeypatch):
    monkeypatch.setenv("HIKVISION_MODE", "SIMULATION")
    monkeypatch.setenv("HIKVISION_PILOT_EMPLOYEE_NOS", PILOT_NO)


def iso(minutes: int) -> str:
    return (clock.now() + timedelta(minutes=minutes)).isoformat()


def to_visitor(admin: TestClient, device_key: str = "sim-exit") -> dict:
    r = admin.post("/api/pilot/simulate/user-type", json={"device_key": device_key, "to": "visitor", "apply": True,
                                                         "confirm": f"{PILOT_NO}:normal->visitor"}).json()
    assert r["ok"] and r["applied"], r
    return r


def ready(admin: TestClient, visitor: bool = True) -> None:
    assert admin.post("/api/pilot/setup").status_code == 200
    assert admin.post("/api/pilot/enabled", json={"enabled": True}).json() == {"enabled": True}
    if visitor:
        to_visitor(admin)


def test_only_admin(db, guard, advisor):
    for client in (guard, advisor, TestClient(app)):
        assert client.get("/api/pilot/status").status_code in (401, 403)
        assert client.post("/api/pilot/simulate", json={}).status_code in (401, 403)
        assert client.post("/api/pilot/permissions", json={}).status_code in (401, 403, 422)


def test_no_door_open_endpoint_anywhere():
    """Браузер не может открыть турникет: таких маршрутов нет ни в API, ни в приёмнике."""
    for application in (app, gateway_app):
        for route in application.routes:
            path = getattr(route, "path", "").lower()
            if path in ("/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"):
                continue
            assert "remotecontrol" not in path and "open" not in path and "door" not in path, path


def test_full_simulation_deny_allow_deny(db, admin):
    ready(admin)
    s = admin.get("/api/pilot/status").json()
    assert s["settings"]["mode"] == "SIMULATION" and s["pilot_enabled"] is True
    assert {d["key"] for d in s["devices"]} == {"sim-exit", "sim-entry"}
    assert s["persons"][0]["employee_no"] == PILOT_NO

    # DENY: разрешения нет
    r = admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO}).json()
    assert r["door_opened"] is False
    assert any("no_permission" in t or "Нет разрешения" in t for t in r["trace"])

    # ALLOW: создали окно
    perm = admin.post("/api/pilot/permissions", json={"employee_no": PILOT_NO, "valid_from": iso(-1),
                                                      "valid_until": iso(20), "single_use": True}).json()
    assert perm["status"] == "active" and perm["source"] == "pilot"
    r = admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO}).json()
    assert r["door_opened"] is True and r["response"]["RemoteCheck"]["checkResult"] == "success"
    allow_id = r["decision_id"]

    # Повтор того же события — не открывает
    r = admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO, "scenario": "repeat_last"}).json()
    assert r["door_opened"] is False

    # Проход подтверждён виртуальным турникетом
    p = admin.post("/api/pilot/simulate/passage", json={"decision_id": allow_id, "outcome": "passed"}).json()
    assert p["passage"] == "passed"

    # DENY: одноразовое разрешение использовано; новое — отменили
    assert admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO}).json()["door_opened"] is False
    perm2 = admin.post("/api/pilot/permissions", json={"employee_no": PILOT_NO, "valid_from": iso(-1),
                                                       "valid_until": iso(20)}).json()
    assert admin.post(f"/api/pilot/permissions/{perm2['id']}/revoke").json()["status"] == "revoked"
    assert admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO}).json()["door_opened"] is False

    s = admin.get("/api/pilot/status").json()
    results = [(d["result"], d["reason"]) for d in s["decisions"]]
    assert ("ALLOW", "permission_valid") in results
    assert ("DENY", "duplicate_event") in results and ("DENY", "permission_revoked") in results
    allow = next(d for d in s["decisions"] if d["id"] == allow_id)
    assert allow["passage"]["outcome"] == "passed" and allow["command"]["check_result"] == "success"
    assert all(c["status"] in ("simulated",) for c in s["commands"] if c["kind"] == "remote_check_sync_response")
    # В журнале событий нет ФИО
    assert all("name" not in e for e in s["events"])


def test_simulation_after_repeat_gets_new_serial(db, admin):
    """Регресс: после «повтора» и события прохода в ту же секунду новое лицо — новое событие, а не дубликат."""
    ready(admin)
    admin.post("/api/pilot/permissions", json={"employee_no": PILOT_NO, "valid_from": iso(-1), "valid_until": iso(20)})
    allow = admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO}).json()
    admin.post("/api/pilot/simulate/passage", json={"decision_id": allow["decision_id"], "outcome": "passed"})
    admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO, "scenario": "repeat_last"})
    admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO})
    reasons = [d["reason"] for d in admin.get("/api/pilot/status").json()["decisions"]]
    assert reasons[:3] == ["permission_used", "duplicate_event", "permission_valid"]


def test_simulation_scenarios(db, admin):
    ready(admin)
    admin.post("/api/pilot/permissions", json={"employee_no": PILOT_NO, "valid_from": iso(-1), "valid_until": iso(20),
                                               "single_use": False})
    sim = lambda **kw: admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO, **kw}).json()  # noqa: E731
    assert sim(scenario="server_down")["door_opened"] is False
    assert sim(scenario="stale")["door_opened"] is False
    assert sim(scenario="card")["door_opened"] is False
    # Вход — по локальным правам терминала, без kpp-journal
    entry = sim(device_key="sim-entry")
    assert entry["door_opened"] is True and entry["local"] is True and entry["decision_id"] is None
    assert sim(device_key="unknown-terminal")["door_opened"] is False
    assert sim(employee_no="0000000001")["door_opened"] is False
    assert sim()["door_opened"] is True
    assert admin.post("/api/pilot/simulate", json={"scenario": "nope"}).status_code == 400


def test_simulation_only_in_simulation_mode(db, admin, monkeypatch):
    ready(admin)
    monkeypatch.setenv("HIKVISION_MODE", "READ_ONLY")
    assert admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO}).status_code == 409


def test_permission_validation(db, admin):
    ready(admin)
    bad = [
        {"employee_no": "0000000001", "valid_from": iso(0), "valid_until": iso(10)},
        {"employee_no": PILOT_NO, "valid_from": iso(10), "valid_until": iso(0)},
        {"employee_no": PILOT_NO, "valid_from": iso(0), "valid_until": iso(60 * 13)},
    ]
    for body in bad:
        assert admin.post("/api/pilot/permissions", json=body).status_code in (400, 403)
    assert admin.post("/api/pilot/permissions/999/revoke").status_code == 404


def test_manual_confirm_and_device_check(db, admin):
    ready(admin)
    admin.post("/api/pilot/permissions", json={"employee_no": PILOT_NO, "valid_from": iso(-1), "valid_until": iso(20)})
    allow = admin.post("/api/pilot/simulate", json={"employee_no": PILOT_NO}).json()["decision_id"]
    r = admin.post(f"/api/pilot/decisions/{allow}/confirm", json={"passed": True})
    assert r.json() == {"decision_id": allow, "outcome": "passed"}
    assert admin.post(f"/api/pilot/decisions/{allow}/confirm", json={"passed": True}).status_code == 409

    c = admin.post("/api/pilot/devices/sim-exit/check").json()
    assert c["ok"] is True and c["info"]["model"] == "MOCK-TERMINAL"
    dev = next(d for d in admin.get("/api/pilot/status").json()["devices"] if d["key"] == "sim-exit")
    assert dev["last_health_ok"] is True


def test_real_device_check_blocked_in_simulation(db, admin):
    ready(admin)
    db.add(HikDevice(key="school", name="Школьный", host="192.0.2.49", direction=HikDirection.EXIT,
                     allowed_ips=["192.0.2.49"], credentials_env="SCHOOL"))
    db.commit()
    c = admin.post("/api/pilot/devices/school/check").json()
    assert c["ok"] is False and "SIMULATION" in c["error"]
    assert db.scalar(select(HikCommand).where(HikCommand.kind == "isapi_read")).status == "blocked"


# ---------- Приёмник терминалов (отдельный процесс) ----------


def _gateway_device(db, ip="testclient"):
    db.add(HikDevice(key="stand", name="Стенд", host="192.0.2.5", direction=HikDirection.EXIT, allowed_ips=[ip]))
    db.commit()


def test_gateway_sync_response(db, admin, monkeypatch):
    ready(admin)
    _gateway_device(db)
    admin.post("/api/pilot/permissions", json={"employee_no": PILOT_NO, "valid_from": iso(-1), "valid_until": iso(20)})
    monkeypatch.setenv("HIKVISION_MODE", "PILOT")
    monkeypatch.setenv("HIKVISION_CONTROL_ENABLED", "1")
    monkeypatch.setenv("HIKVISION_CONTROL_DEVICES", "stand")
    gw = TestClient(gateway_app)
    mock = MockHikvisionDevice()

    def post(ct, body):
        r = gw.post("/hikvision/listen/stand", content=body, headers={"content-type": ct})
        return r.status_code, r.content

    out = mock.present_face(post, PILOT_NO)
    assert out.door_opened is True and out.response["RemoteCheck"]["serialNo"] == out.serial_no
    out = mock.present_face(post, PILOT_NO)
    assert out.door_opened is False  # одноразовое
    assert gw.get("/hikvision/health").json() == {"ok": True, "mode": "PILOT"}


def test_gateway_rejects_untrusted_ip_and_garbage(db, admin):
    ready(admin)
    _gateway_device(db, ip="192.0.2.5")  # TestClient приходит с адреса «testclient»
    admin.post("/api/pilot/permissions", json={"employee_no": PILOT_NO, "valid_from": iso(-1), "valid_until": iso(20)})
    gw = TestClient(gateway_app)
    mock = MockHikvisionDevice()
    ct, body = mock.multipart(mock.event(PILOT_NO))
    r = gw.post("/hikvision/listen/stand", content=body, headers={"content-type": ct})
    assert r.json()["RemoteCheck"]["checkResult"] == "failed"
    r = gw.post("/hikvision/listen/stand", content=b"garbage", headers={"content-type": "application/json"})
    assert r.status_code == 400


def test_gateway_timeout_answers_failed(db, admin, monkeypatch):
    ready(admin)
    _gateway_device(db)
    admin.post("/api/pilot/permissions", json={"employee_no": PILOT_NO, "valid_from": iso(-1), "valid_until": iso(20)})
    monkeypatch.setenv("HIKVISION_MODE", "PILOT")
    monkeypatch.setenv("HIKVISION_CONTROL_ENABLED", "1")
    monkeypatch.setenv("HIKVISION_CONTROL_DEVICES", "stand")
    monkeypatch.setenv("HIKVISION_DECISION_BUDGET_MS", "200")
    real = hik_adapter.handle_device_request

    def slow(*a, **kw):
        time.sleep(0.6)
        return real(*a, **kw)

    monkeypatch.setattr("app.hikvision_gateway.handle_device_request", slow)
    gw = TestClient(gateway_app)
    mock = MockHikvisionDevice()
    ev = mock.event(PILOT_NO)
    ct, body = mock.multipart(ev)
    t0 = time.monotonic()
    r = gw.post("/hikvision/listen/stand", content=body, headers={"content-type": ct})
    assert time.monotonic() - t0 < 0.55
    assert r.json() == {"RemoteCheck": {"serialNo": ev["AccessControllerEvent"]["serialNo"], "checkResult": "failed"}}

    # Опоздавшая обработка доходит до конца, но ALLOW уже не выдаёт и разрешение не тратит
    deadline = time.monotonic() + 5
    decision = None
    while time.monotonic() < deadline and decision is None:
        time.sleep(0.1)
        db.expire_all()
        decision = db.scalar(select(ReleaseDecision))
    assert decision is not None and (decision.result, decision.reason) == ("DENY", "decision_timeout")
    assert db.scalar(select(ReleasePermission)).used_at is None
    assert db.scalar(select(HikCommand).where(HikCommand.status == "timeout")) is not None
