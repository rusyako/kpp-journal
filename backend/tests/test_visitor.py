"""Пилот userType=visitor: normal — локально, visitor — только через kpp-journal.

Всё — на виртуальном терминале (MockHikvisionDevice) по поведению, описанному в документации.
Сценарии A, I, J, K на реальном оборудовании этими тестами НЕ подтверждаются (VISITOR_PILOT_TESTS.md).
"""

import json
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from sqlalchemy import select

from app import clock
from app.integrations.hikvision import settings as hik_settings
from app.integrations.hikvision.adapter import handle_device_request
from app.integrations.hikvision.client import ForbiddenOperation, IsapiClient, IsapiError, check_operation
from app.integrations.hikvision.mock_device import SIM_SOURCE, MockHikvisionDevice, MockUser
from app.integrations.hikvision.remote_check_plan import build_plan
from app.integrations.hikvision.user_type import change_user_type, confirm_phrase
from app.integrations.hikvision.user_type import main as user_type_main
from app.models import HikDevice, HikDirection, HikEvent, HikPassage, HikPerson, ReleaseDecision, User
from app.services import pilot

PILOT_NO = "3818077855"
STAFF = "1000000001"


@pytest.fixture
def admin_user(db) -> User:
    return db.scalar(select(User).where(User.username == "admin"))


@pytest.fixture
def setup(db, admin_user, monkeypatch):
    monkeypatch.setenv("HIKVISION_MODE", "SIMULATION")
    monkeypatch.setenv("HIKVISION_PILOT_EMPLOYEE_NOS", PILOT_NO)
    pilot.ensure_setup(db, admin_user)
    pilot.set_enabled(db, admin_user, True)
    return admin_user


def terminal(**kw) -> MockHikvisionDevice:
    """Стенд: тестовая запись и сотрудник — normal; удалённая проверка только для visitor."""
    base = dict(users={PILOT_NO: MockUser(PILOT_NO), STAFF: MockUser(STAFF)}, remote_check_user_types=["visitor"])
    base.update(kw)
    return MockHikvisionDevice(**base)


def sim_device():
    return SimpleNamespace(key="sim", simulated=True, active=True, host="", port=80, scheme="http", credentials_env=None)


def client_for(mock: MockHikvisionDevice, settings=None, device=None) -> IsapiClient:
    return IsapiClient(device or sim_device(), settings or hik_settings.load(), transport=mock.transport(),
                       credentials=(mock.username, mock.password))


def face(db, mock, emp, device_key="sim-exit"):
    holder = {}

    def post(ct, body):
        r = handle_device_request(db, device_key, SIM_SOURCE, ct, body)
        holder.setdefault("all", []).append(r)
        if r.decision is not None:
            holder["r"] = r
        return r.http_status, json.dumps(r.body or {}).encode()

    out = mock.present_face(post, emp)
    return holder.get("r"), out


def make_visitor(mock):
    with client_for(mock) as c:
        rep = change_user_type(c, hik_settings.load(), PILOT_NO, "visitor", apply=True,
                               confirm=confirm_phrase(PILOT_NO, "normal", "visitor"))
    assert rep.ok, rep.problems
    return rep


def permit(db, user, start=-5, end=30):
    now = clock.now()
    return pilot.create_permission(db, user, PILOT_NO, now + timedelta(minutes=start), now + timedelta(minutes=end))


def decisions(db):
    return list(db.scalars(select(ReleaseDecision)))


# ---------- A. normal — прежняя локальная политика ----------


def test_a_normal_users_stay_local(db, setup):
    mock = terminal()
    for emp in (STAFF, PILOT_NO):  # тестовая запись тоже normal, пока не изменена
        r, out = face(db, mock, emp)
        assert out.door_opened and out.local and r is None
    assert decisions(db) == []  # kpp-journal решений не принимал
    # События normal пришли только как информация
    assert {e.category for e in db.scalars(select(HikEvent))} == {"auth_ok"}
    assert all(not e.remote_check for e in db.scalars(select(HikEvent)))


# ---------- B–H: visitor ----------


def test_b_visitor_without_permission_deny(db, setup):
    mock = terminal()
    make_visitor(mock)
    r, out = face(db, mock, PILOT_NO)
    assert (r.decision, r.reason) == ("DENY", "no_permission") and not out.door_opened and not out.local
    assert db.get(HikEvent, r.event_id).user_type == "visitor"


def test_c_visitor_with_permission_allow(db, setup):
    mock = terminal()
    make_visitor(mock)
    permit(db, setup)
    r, out = face(db, mock, PILOT_NO)
    assert (r.decision, r.check_result) == ("ALLOW", "success") and out.door_opened
    assert r.body["RemoteCheck"]["serialNo"] == out.serial_no


def test_d_visitor_too_early_deny(db, setup):
    mock = terminal()
    make_visitor(mock)
    permit(db, setup, start=10, end=40)
    r, out = face(db, mock, PILOT_NO)
    assert r.reason == "permission_not_started" and not out.door_opened


def test_e_visitor_revoked_deny(db, setup):
    mock = terminal()
    make_visitor(mock)
    pilot.revoke_permission(db, setup, permit(db, setup).id)
    r, out = face(db, mock, PILOT_NO)
    assert r.reason == "permission_revoked" and not out.door_opened


def test_f_server_down_visitor_closed_normal_unaffected(db, setup):
    mock = terminal()
    make_visitor(mock)
    permit(db, setup)

    def down(ct, body):
        raise ConnectionError("kpp-journal недоступен")

    assert mock.present_face(down, PILOT_NO).door_opened is False
    # normal не зависит от kpp-journal
    staff = mock.present_face(down, STAFF)
    assert staff.door_opened and staff.local


def test_g_same_serial_no_reopen_and_device_binding(db, setup):
    permit(db, setup)
    mock = terminal()
    make_visitor(mock)
    ev = mock.event(PILOT_NO)
    ct, body = mock.multipart(ev)
    first = handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body)
    again = handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body)
    assert first.decision == "ALLOW" and (again.reason, again.check_result) == ("duplicate_event", "failed")
    # Тот же serialNo с ДРУГОГО терминала — другое событие (решение привязано к терминалу), не дубликат
    other = handle_device_request(db, "sim-entry", SIM_SOURCE, ct, body)
    assert other.reason == "wrong_direction"
    assert db.get(HikEvent, other.event_id).duplicate_of_id is None
    d = db.get(ReleaseDecision, first.decision_id)
    e = db.get(HikEvent, d.event_id)
    assert (e.serial_no, e.device_key, d.employee_no) == (ev["AccessControllerEvent"]["serialNo"], "sim-exit", PILOT_NO)


def test_g_passage_of_other_person_not_linked(db, setup):
    permit(db, setup)
    mock = terminal()
    make_visitor(mock)
    r, out = face(db, mock, PILOT_NO)
    assert out.door_opened
    ct, body = mock.multipart(mock.event(STAFF, minor=218, remote_check=False, user_type="normal"))
    handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body)
    assert db.scalar(select(HikPassage)) is None  # чужой проход не засчитан тестовому решению


def test_h_unknown_employee(db, setup):
    mock = terminal()
    out = mock.present_face(lambda *a: (_ for _ in ()).throw(AssertionError("запроса быть не должно")), "0000000001")
    assert not out.door_opened  # терминал отсёк незарегистрированное лицо сам
    legacy = MockHikvisionDevice()  # если запрос всё же пришёл
    r, out = face(db, legacy, "0000000001")
    assert r.reason == "unknown_person" and not out.door_opened


def test_visitor_card_does_not_bypass(db, setup):
    """remoteCheckVerifyMode=6: карта visitor тоже идёт на проверку; в пилоте карта — DENY."""
    permit(db, setup)
    mock = terminal()
    make_visitor(mock)
    holder = {}

    def post(ct, body):
        r = handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body)
        holder["r"] = r
        return r.http_status, json.dumps(r.body or {}).encode()

    out = mock.present_face(post, PILOT_NO, minor=1)  # 0x01 Valid Card Swiping
    assert holder["r"].reason == "unsupported_event" and not out.door_opened


# ---------- Решения по userType ----------


def test_normal_remote_request_is_isolation_violation(db, setup):
    """K (негатив): прошивка игнорирует remoteCheckUserTypeList → normal попадает к нам → DENY и тревога."""
    permit(db, setup)
    mock = terminal(ignores_user_type_list=True)
    r, out = face(db, mock, STAFF)
    assert r.reason == "not_remote_check_type" and not out.door_opened
    r, _ = face(db, mock, PILOT_NO)  # тестовая запись ещё normal → тоже нарушение
    assert r.reason == "not_remote_check_type"
    alerts = pilot.dashboard(db)["isolation_alerts"]
    assert len(alerts) == 2


def test_event_without_user_type_uses_verified_terminal_type(db, setup):
    permit(db, setup)
    legacy = MockHikvisionDevice()
    ev = legacy.event(PILOT_NO, user_type=None)
    r = handle_device_request(db, "sim-exit", SIM_SOURCE, *legacy.multipart(ev))
    assert r.reason == "user_type_unknown"
    person = db.scalar(select(HikPerson).where(HikPerson.employee_no == PILOT_NO))
    person.terminal_user_type = "normal"
    db.commit()
    r = handle_device_request(db, "sim-exit", SIM_SOURCE, *legacy.multipart(legacy.event(PILOT_NO, user_type=None)))
    assert r.reason == "not_remote_check_type"
    person.terminal_user_type = "visitor"
    db.commit()
    r = handle_device_request(db, "sim-exit", SIM_SOURCE, *legacy.multipart(legacy.event(PILOT_NO, user_type=None)))
    assert r.decision == "ALLOW"


# ---------- I, J. Смена userType и откат ----------


def test_i_dry_run_sends_nothing(db, setup, tmp_path):
    mock = terminal()
    with client_for(mock) as c:
        rep = change_user_type(c, hik_settings.load(), PILOT_NO, "visitor", backup_dir=tmp_path)
    assert rep.ok and not rep.applied and rep.mode == "DRY_RUN"
    assert rep.request["body"] == {"UserInfo": {"employeeNo": PILOT_NO, "userType": "visitor"}}
    assert rep.confirm == "3818077855:normal->visitor"
    assert all(m != "PUT" for m, _ in mock.requests)
    assert mock.users[PILOT_NO].user_type == "normal"
    backup = json.loads(Path(rep.backup_path).read_text(encoding="utf-8"))
    assert backup["userType"] == "normal" and backup["name"].startswith("sha256:")  # ФИО не хранится


def test_i_change_keeps_face_card_and_rights(db, setup, tmp_path):
    mock = terminal()
    with client_for(mock) as c:
        rep = change_user_type(c, hik_settings.load(), PILOT_NO, "visitor", apply=True,
                               confirm="3818077855:normal->visitor", backup_dir=tmp_path)
    assert rep.ok and rep.applied, rep.problems
    assert rep.after["userType"] == "visitor"
    for k in ("numOfFace", "numOfCard", "doorRight", "RightPlan", "Valid", "onlyVerify", "name"):
        assert rep.after[k] == rep.before[k]
    assert rep.unexpected_changes == []
    # Остальные записи не тронуты; запрос — только employeeNo + userType
    assert mock.users[STAFF].user_type == "normal"
    assert {p for m, p in mock.requests if m != "GET"} == {"/ISAPI/AccessControl/UserInfo/Search",
                                                          "/ISAPI/AccessControl/UserInfo/Modify"}
    assert mock.forbidden_calls == []


def test_i_bad_firmware_resetting_fields_is_detected(db, setup):
    mock = terminal(modify_resets_omitted=True)
    with client_for(mock) as c:
        rep = change_user_type(c, hik_settings.load(), PILOT_NO, "visitor", apply=True, confirm="3818077855:normal->visitor")
    assert rep.applied and not rep.ok
    changed = {f["field"] for f in rep.unexpected_changes}
    assert {"doorRight", "RightPlan", "Valid"} <= changed


def test_j_rollback_restores_original(db, setup, tmp_path):
    mock = terminal()
    s = hik_settings.load()
    with client_for(mock) as c:
        fwd = change_user_type(c, s, PILOT_NO, "visitor", apply=True, confirm="3818077855:normal->visitor", backup_dir=tmp_path)
        original = json.loads(Path(fwd.backup_path).read_text(encoding="utf-8"))
        back = change_user_type(c, s, PILOT_NO, "normal", apply=True, confirm="3818077855:visitor->normal",
                                original=original, backup_dir=tmp_path)
    assert back.ok and back.after["userType"] == "normal" and back.restore_mismatch == []
    # После отката тестовая запись снова проходит локально
    out = mock.present_face(lambda *a: (200, b"{}"), PILOT_NO)
    assert out.door_opened and out.local


def test_k_visitor_only_config_does_not_change_normal(db, setup):
    mock = terminal(remote_check_enabled=False)  # «как сейчас»
    before = mock.present_face(lambda *a: (200, b"{}"), STAFF)
    mock.remote_check_enabled = True  # visitor-only включена
    make_visitor(mock)
    after = mock.present_face(lambda *a: (200, b"{}"), STAFF)
    assert before.door_opened and after.door_opened and before.local and after.local


# ---------- Безопасность инструмента ----------


def test_tool_refuses_other_employee_and_bad_confirm(db, setup):
    mock = terminal()
    s = hik_settings.load()
    with client_for(mock) as c:
        assert not change_user_type(c, s, STAFF, "visitor", apply=True, confirm=f"{STAFF}:normal->visitor").ok
        assert not change_user_type(c, s, PILOT_NO, "visitor", apply=True).ok
        assert not change_user_type(c, s, PILOT_NO, "visitor", apply=True, confirm="да").ok
        assert not change_user_type(c, s, PILOT_NO, "blackList").ok
        assert not change_user_type(c, s, PILOT_NO, "visitor", expected_from="visitor").ok
    assert mock.users[STAFF].user_type == "normal" and mock.users[PILOT_NO].user_type == "normal"
    assert all(m != "PUT" for m, _ in mock.requests)


def test_tool_stops_when_capabilities_do_not_confirm(db, setup):
    s = hik_settings.load()
    for mock in (terminal(supports_user_modify=False),):
        with client_for(mock) as c:
            rep = change_user_type(c, s, PILOT_NO, "visitor", apply=True, confirm="3818077855:normal->visitor")
        assert not rep.ok and "put" in rep.problems[0]
    # Терминал игнорирует фильтр EmployeeNoList → данные чужих записей отброшены, дальше не идём
    mock = terminal(ignores_employee_filter=True, users={STAFF: MockUser(STAFF), PILOT_NO: MockUser(PILOT_NO)})
    with client_for(mock) as c:
        with pytest.raises(IsapiError, match="EmployeeNoList"):
            c.get_user(PILOT_NO)


def test_user_write_gates(monkeypatch):
    real = SimpleNamespace(key="stand", simulated=False, active=True)
    body = {"UserInfo": {"employeeNo": PILOT_NO, "userType": "visitor"}}
    path = "/ISAPI/AccessControl/UserInfo/Modify?format=json"
    monkeypatch.setenv("HIKVISION_PILOT_EMPLOYEE_NOS", PILOT_NO)
    for env in [dict(HIKVISION_MODE="READ_ONLY", HIKVISION_USER_WRITE_ENABLED="1", HIKVISION_USER_WRITE_DEVICES="stand"),
                dict(HIKVISION_MODE="PILOT", HIKVISION_USER_WRITE_ENABLED="0", HIKVISION_USER_WRITE_DEVICES="stand"),
                dict(HIKVISION_MODE="PILOT", HIKVISION_USER_WRITE_ENABLED="1", HIKVISION_USER_WRITE_DEVICES="other"),
                # управление проходом не даёт права на запись персон
                dict(HIKVISION_MODE="PILOT", HIKVISION_CONTROL_ENABLED="1", HIKVISION_CONTROL_DEVICES="stand",
                     HIKVISION_USER_WRITE_ENABLED="0", HIKVISION_USER_WRITE_DEVICES="")]:
        for k, v in env.items():
            monkeypatch.setenv(k, v)
        with pytest.raises(ForbiddenOperation):
            check_operation("PUT", path, hik_settings.load(), real, body)
    monkeypatch.setenv("HIKVISION_USER_WRITE_ENABLED", "1")
    monkeypatch.setenv("HIKVISION_USER_WRITE_DEVICES", "stand")
    s = hik_settings.load()
    check_operation("PUT", path, s, real, body)
    for bad in [
        {"UserInfo": {"employeeNo": STAFF, "userType": "visitor"}},
        {"UserInfo": {"employeeNo": PILOT_NO, "userType": "visitor", "doorRight": ""}},
        {"UserInfo": {"employeeNo": PILOT_NO, "userType": "blackList"}},
        {"UserInfo": [{"employeeNo": PILOT_NO, "userType": "visitor"}]},
        {"UserInfo": {"employeeNo": PILOT_NO, "userType": "visitor"}, "extra": 1},
    ]:
        with pytest.raises(ForbiddenOperation):
            check_operation("PUT", path, s, real, bad)
    with pytest.raises(ForbiddenOperation):
        check_operation("PUT", "/ISAPI/AccessControl/UserInfo/SetUp?format=json", s, real, body)
    search = "/ISAPI/AccessControl/UserInfo/Search?format=json"
    check_operation("POST", search, s, real, {"UserInfoSearchCond": {"maxResults": 1, "EmployeeNoList": [{"employeeNo": PILOT_NO}]}})
    for bad in [None, {"UserInfoSearchCond": {"maxResults": 30, "searchResultPosition": 0}},
                {"UserInfoSearchCond": {"maxResults": 1, "EmployeeNoList": [{"employeeNo": STAFF}]}},
                {"UserInfoSearchCond": {"maxResults": 2, "EmployeeNoList": [{"employeeNo": PILOT_NO}, {"employeeNo": STAFF}]}}]:
        with pytest.raises(ForbiddenOperation):
            check_operation("POST", search, s, real, bad)


# ---------- План visitor-only Remote Verification ----------


def test_plan_go_for_stand_only(monkeypatch):
    mock = terminal(remote_check_enabled=False, http_host_configured=False, remote_check_user_types=None)
    with client_for(mock) as c:
        plan = build_plan(c)
    assert plan["verdict"] == "GO_STAND_ONLY"
    changed = {x["field"] for x in plan["global_changes_AcsCfg"]}
    assert {"remoteCheckDoorEnabled", "remoteCheckUserTypeList", "remoteCheckVerifyMode"} <= changed
    assert plan["put_body"]["AcsCfg"]["remoteCheckUserTypeList"] == ["visitor"]
    assert plan["put_body"]["AcsCfg"]["offlineDevCheckOpenDoorEnabled"] is False
    assert plan["rollback_body"]["AcsCfg"]["remoteCheckDoorEnabled"] is False
    assert all(m == "GET" for m, _ in mock.requests)  # план только читает


@pytest.mark.parametrize("kw,stop", [
    (dict(supports_user_type_list=False), "remoteCheckUserTypeList"),
    (dict(remote_check_enabled=True), "remoteCheckDoorEnabled сейчас"),
    (dict(http_host_configured=True), "httpHosts"),
])
def test_plan_stops(kw, stop):
    base = dict(remote_check_enabled=False, http_host_configured=False)
    base.update(kw)
    with client_for(terminal(**base)) as c:
        plan = build_plan(c)
    assert plan["verdict"] == "STOP" and stop in plan["verdict_text"]


# ---------- Экран и API ----------


def test_refresh_and_simulated_user_type_via_api(db, admin, monkeypatch):
    monkeypatch.setenv("HIKVISION_MODE", "SIMULATION")
    monkeypatch.setenv("HIKVISION_PILOT_EMPLOYEE_NOS", PILOT_NO)
    admin.post("/api/pilot/setup")
    r = admin.post("/api/pilot/devices/sim-exit/refresh").json()
    assert r["user_type"] == "normal" and r["numOfFace"] == 1 and r["numOfCard"] == 1
    dry = admin.post("/api/pilot/simulate/user-type", json={"to": "visitor"}).json()
    assert dry["mode"] == "DRY_RUN" and not dry["applied"] and dry["confirm"] == "3818077855:normal->visitor"
    bad = admin.post("/api/pilot/simulate/user-type", json={"to": "visitor", "apply": True, "confirm": "нет"}).json()
    assert not bad["ok"] and not bad["applied"]
    ok = admin.post("/api/pilot/simulate/user-type", json={"to": "visitor", "apply": True,
                                                           "confirm": "3818077855:normal->visitor"}).json()
    assert ok["ok"] and ok["applied"]
    s = admin.get("/api/pilot/status").json()
    assert s["persons"][0]["terminal_user_type"] == "visitor"
    dev = next(d for d in s["devices"] if d["key"] == "sim-exit")
    assert dev["remote_check"]["verdict"] in ("GO_STAND_ONLY", "STOP")
    # Не в SIMULATION — из браузера userType не меняется, реальный терминал не читается
    monkeypatch.setenv("HIKVISION_MODE", "READ_ONLY")
    assert admin.post("/api/pilot/simulate/user-type", json={"to": "normal"}).status_code == 409
    db.add(HikDevice(key="school", name="Школьный", host="192.0.2.49", direction=HikDirection.EXIT,
                     allowed_ips=["192.0.2.49"], credentials_env="SCHOOL"))
    db.commit()
    monkeypatch.setenv("HIKVISION_MODE", "SIMULATION")
    assert admin.post("/api/pilot/devices/school/refresh").status_code == 409


def test_cli_dry_run_on_mock(capsys, monkeypatch, tmp_path):
    monkeypatch.setenv("HIKVISION_MODE", "SIMULATION")
    assert user_type_main(["--mock", "--to", "visitor", "--out", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert '"mode": "DRY_RUN"' in out and "3818077855:normal->visitor" in out
    # Реальный терминал без --confirm-network — отказ без сетевых запросов
    with pytest.raises(SystemExit) as e:
        user_type_main(["--host", "192.0.2.49", "--to", "visitor"])
    assert e.value.code == 2
