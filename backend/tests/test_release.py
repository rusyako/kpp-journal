"""Decision Engine и полный путь «лицо → запрос → решение → ответ → проход» на виртуальном терминале.

Сценарии A–I из задачи пилота + защитные случаи. Оборудование не нужно.
"""

import json
import time
from datetime import timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.exc import OperationalError

from app import clock
from app.integrations.hikvision import adapter as hik_adapter
from app.integrations.hikvision import settings as hik_settings
from app.integrations.hikvision.adapter import handle_device_request
from app.integrations.hikvision.client import IsapiClient
from app.integrations.hikvision.mock_device import SIM_SOURCE, MockHikvisionDevice
from app.models import (
    Exit,
    HikCommand,
    HikDevice,
    HikDirection,
    HikEvent,
    HikPassage,
    HikPerson,
    ReleaseDecision,
    ReleasePermission,
    User,
)
from app.services import pilot, release
from tests.conftest import student_id

PILOT_NO = "3818077855"


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


@pytest.fixture
def mock() -> MockHikvisionDevice:
    return MockHikvisionDevice()


def face(db, mock, emp=PILOT_NO, device_key="sim-exit", source=SIM_SOURCE, **kw):
    """Терминал опознал лицо и спрашивает kpp-journal. → (результат адаптера, что сделал терминал)."""
    holder = {}

    def post(ct, body):
        r = handle_device_request(db, device_key, source, ct, body)
        holder["r"] = r
        return r.http_status, json.dumps(r.body or {}).encode()

    outcome = mock.present_face(post, emp, **kw)
    return holder.get("r"), outcome


def permit(db, user, start_min=-5, end_min=30, single_use=True):
    now = clock.now()
    return pilot.create_permission(db, user, PILOT_NO, now + timedelta(minutes=start_min),
                                   now + timedelta(minutes=end_min), single_use)


# ---------- Сценарии A–I ----------


def test_a_no_permission_deny(db, setup, mock):
    r, out = face(db, mock)
    assert (r.decision, r.reason, r.check_result) == ("DENY", "no_permission", "failed")
    assert r.body == {"RemoteCheck": {"serialNo": out.serial_no, "checkResult": "failed"}}
    assert out.door_opened is False


def test_b_permission_not_started_deny(db, setup, mock, now):
    permit(db, setup, start_min=10, end_min=60)
    r, out = face(db, mock)
    assert (r.decision, r.reason) == ("DENY", "permission_not_started")
    assert out.door_opened is False
    # Когда окно наступило — ALLOW
    now.set(14, 11)
    r, out = face(db, mock)
    assert r.decision == "ALLOW" and out.door_opened


def test_c_valid_permission_allow(db, setup, mock):
    perm = permit(db, setup)
    r, out = face(db, mock)
    assert (r.decision, r.reason, r.check_result, r.command_status) == ("ALLOW", "permission_valid", "success", "simulated")
    # serialNo ответа совпадает с serialNo события
    assert r.body["RemoteCheck"]["serialNo"] == out.serial_no
    assert out.door_opened is True
    db.refresh(perm)
    assert perm.used_at is not None and perm.used_by_decision_id == r.decision_id


def test_d_revoked_permission_deny(db, setup, mock):
    perm = permit(db, setup)
    pilot.revoke_permission(db, setup, perm.id)
    r, out = face(db, mock)
    assert (r.decision, r.reason) == ("DENY", "permission_revoked")
    assert out.door_opened is False


def test_d_expired_permission_deny(db, setup, mock, now):
    permit(db, setup, start_min=-5, end_min=5)
    now.set(14, 6)
    r, _ = face(db, mock)
    assert (r.decision, r.reason) == ("DENY", "permission_expired")


def test_e_server_unreachable_terminal_stays_closed(db, setup, mock):
    permit(db, setup)

    def down(ct, body):
        raise ConnectionError("kpp-journal недоступен")

    out = mock.present_face(down, PILOT_NO)
    assert out.door_opened is False
    # Ничего не записано и разрешение не израсходовано
    assert db.scalar(select(ReleaseDecision)) is None
    assert db.scalar(select(ReleasePermission)).used_at is None


def test_e_decision_engine_error_is_fail_closed(db, setup, mock, monkeypatch):
    permit(db, setup)

    def broken(*a, **kw):
        raise OperationalError("SELECT", {}, Exception("БД недоступна"))

    monkeypatch.setattr(release, "_evaluate", broken)
    r, out = face(db, mock)
    assert (r.decision, r.reason, r.check_result) == ("DENY", "internal_error", "failed")
    assert out.door_opened is False


def test_e_database_down_before_event_is_stored(db, setup, mock, monkeypatch):
    permit(db, setup)

    def broken(*a, **kw):
        raise OperationalError("INSERT", {}, Exception("БД недоступна"))

    monkeypatch.setattr(hik_adapter, "_store_event", broken)
    r, out = face(db, mock)
    assert r.check_result == "failed" and r.reason == "internal_error"
    assert r.body["RemoteCheck"]["checkResult"] == "failed"
    assert out.door_opened is False


def test_f_duplicate_event_does_not_reopen(db, setup, mock):
    permit(db, setup, single_use=False)  # даже многоразовое разрешение не откроет повтор того же события
    ev = mock.event(PILOT_NO)
    ct, body = mock.multipart(ev)
    first = handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body)
    second = handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body)
    assert first.decision == "ALLOW" and first.check_result == "success"
    assert (second.decision, second.reason, second.check_result) == ("DENY", "duplicate_event", "failed")
    dup = db.get(HikEvent, second.event_id)
    assert dup.duplicate_of_id == first.event_id and dup.dedup_key is None


def test_f_single_use_permission_not_reused_by_new_event(db, setup, mock):
    permit(db, setup)
    r1, o1 = face(db, mock)
    r2, o2 = face(db, mock)
    assert o1.door_opened and not o2.door_opened
    assert (r2.decision, r2.reason) == ("DENY", "permission_used")


def test_g_unknown_person_deny(db, setup, mock):
    permit(db, setup)
    r, out = face(db, mock, emp="0000000001")
    assert (r.decision, r.reason) == ("DENY", "unknown_person")
    assert not out.door_opened
    r, _ = face(db, mock, emp=None)
    assert r.reason == "no_employee_no"


def test_h_unknown_terminal_deny(db, setup, mock):
    permit(db, setup)
    r, out = face(db, mock, device_key="unknown-terminal")
    assert (r.decision, r.reason, r.check_result) == ("DENY", "unknown_device", "failed")
    assert not out.door_opened
    assert db.get(HikEvent, r.event_id).device_id is None


def test_h_untrusted_source_ip_deny(db, setup, mock):
    permit(db, setup)
    # Виртуальный терминал не принимает запросы из сети
    r, _ = face(db, mock, source="10.1.1.1")
    assert r.reason == "untrusted_source"
    # Реальный терминал без allowed_ips никому не доверяет
    db.add(HikDevice(key="stand", name="Стенд", host="10.0.0.5", direction=HikDirection.EXIT, allowed_ips=[]))
    db.commit()
    r, _ = face(db, mock, device_key="stand", source="10.0.0.5")
    assert r.reason == "untrusted_source"


def test_i_allow_then_confirmed_passage_journal(db, setup, mock):
    permit(db, setup)
    r, out = face(db, mock)
    assert out.door_opened
    # ALLOW ≠ проход: пока события прохода нет, записи о проходе нет
    assert db.scalar(select(HikPassage)) is None

    ct, body = mock.multipart(mock.event(PILOT_NO, minor=218, remote_check=False))
    p = handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body)
    assert p.category == "passage" and p.decision is None and p.body is None

    passage = db.scalar(select(HikPassage))
    assert passage.decision_id == r.decision_id and passage.outcome == "passed" and passage.source == "device_event"
    # Тестовая учётная запись не попадает в журнал выхода учеников
    assert passage.exit_id is None and db.scalar(select(Exit)) is None

    d = next(x for x in pilot.dashboard(db)["decisions"] if x["id"] == r.decision_id)
    assert d["result"] == "ALLOW"
    assert d["command"] == {"status": "simulated", "check_result": "success"}
    assert d["passage"]["outcome"] == "passed"


def test_i_passage_timed_out(db, setup, mock):
    permit(db, setup)
    r, _ = face(db, mock)
    ct, body = mock.multipart(mock.event(PILOT_NO, minor=137, remote_check=False))
    handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body)
    assert db.scalar(select(HikPassage)).outcome == "timed_out"


def test_i_student_passage_creates_exit(db, setup, mock, monkeypatch):
    """Будущий путь для учеников: проход ученика по ALLOW создаёт отметку выхода без охранника."""
    sid = student_id(db, "Ким Илья")
    monkeypatch.setenv("HIKVISION_PILOT_EMPLOYEE_NOS", f"{PILOT_NO},S-0001")
    person = HikPerson(employee_no="S-0001", label="ученик (тест)", kind="student", student_id=sid, pilot=True)
    db.add(person)
    db.commit()
    now = clock.now()
    pilot.create_permission(db, setup, "S-0001", now - timedelta(minutes=1), now + timedelta(minutes=10))
    r, out = face(db, mock, emp="S-0001")
    assert out.door_opened
    ct, body = mock.multipart(mock.event("S-0001", minor=218, remote_check=False))
    handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body)
    ex = db.scalar(select(Exit))
    assert ex.student_id == sid and ex.guard_id is None
    assert db.scalar(select(HikPassage)).exit_id == ex.id


def test_passage_not_linked_to_blocked_allow(db, setup, mock, monkeypatch):
    """Если «success» не уходил (теневой режим), событие прохода не считается выходом по нашему решению."""
    permit(db, setup)
    monkeypatch.setenv("HIKVISION_MODE", "READ_ONLY")
    r, out = face(db, mock)
    assert r.decision == "ALLOW" and r.command_status == "blocked" and not out.door_opened
    ct, body = mock.multipart(mock.event(PILOT_NO, minor=218, remote_check=False))
    handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body)
    assert db.scalar(select(HikPassage)) is None


def test_manual_passage_confirmation(db, setup, mock):
    permit(db, setup)
    r, _ = face(db, mock)
    p = release.confirm_passage_manually(db, setup, r.decision_id, passed=False)
    assert p.outcome == "not_passed" and p.confirmed_by == setup.id
    with pytest.raises(release.PassageError):
        release.confirm_passage_manually(db, setup, r.decision_id, passed=True)
    deny, _ = face(db, mock)
    with pytest.raises(release.PassageError):
        release.confirm_passage_manually(db, setup, deny.decision_id, passed=True)


# ---------- Защитные случаи ----------


def test_wrong_direction_deny(db, setup, mock):
    permit(db, setup)
    r, out = face(db, mock, device_key="sim-entry")
    assert r.reason == "wrong_direction" and not out.door_opened


def test_pilot_switch_off_denies_everything(db, setup, mock):
    perm = permit(db, setup)
    pilot.set_enabled(db, setup, False)
    r, _ = face(db, mock)
    assert r.reason == "pilot_disabled"
    db.refresh(perm)
    assert perm.used_at is None


def test_stale_and_replayed_events_deny(db, setup, mock):
    permit(db, setup, single_use=False)
    r, _ = face(db, mock, when=clock.now() - timedelta(minutes=5))
    assert r.reason == "stale_event"
    r, _ = face(db, mock, when=clock.now() + timedelta(minutes=5))
    assert r.reason == "stale_event"
    r, _ = face(db, mock, current=False)
    assert r.reason == "not_realtime"
    r, _ = face(db, mock, time_str="вчера")
    assert r.reason == "bad_event_time"


def test_card_and_other_events_not_in_pilot(db, setup, mock):
    permit(db, setup, single_use=False)
    r, _ = face(db, mock, minor=1)  # карта
    assert r.reason == "unsupported_event"


def test_person_outside_pilot_list_deny(db, setup, mock, monkeypatch):
    permit(db, setup, single_use=False)
    monkeypatch.setenv("HIKVISION_PILOT_EMPLOYEE_NOS", "1111111111")
    r, _ = face(db, mock)
    assert r.reason == "not_in_pilot"


def test_inactive_profile_deny(db, setup, mock):
    permit(db, setup, single_use=False)
    person = db.scalar(select(HikPerson).where(HikPerson.employee_no == PILOT_NO))
    person.active = False
    db.commit()
    assert face(db, mock)[0].reason == "person_inactive"
    person.active = True
    db.get(User, person.user_id).active = False
    db.commit()
    assert face(db, mock)[0].reason == "profile_inactive"


def test_permission_only_for_pilot_employee(db, setup):
    now = clock.now()
    with pytest.raises(pilot.PilotError):
        pilot.create_permission(db, setup, "0000000001", now, now + timedelta(minutes=5))
    with pytest.raises(pilot.PilotError):
        pilot.create_permission(db, setup, PILOT_NO, now, now - timedelta(minutes=5))
    with pytest.raises(pilot.PilotError):
        pilot.create_permission(db, setup, PILOT_NO, now, now + timedelta(hours=13))


def test_deadline_passed_means_no_allow(db, setup, mock):
    perm = permit(db, setup)
    ev = mock.event(PILOT_NO)
    ct, body = mock.multipart(ev)
    r = handle_device_request(db, "sim-exit", SIM_SOURCE, ct, body, deadline=time.monotonic() - 1)
    assert (r.decision, r.reason, r.check_result) == ("DENY", "decision_timeout", "failed")
    db.refresh(perm)
    assert perm.used_at is None


# ---------- Режимы ----------


def _stand(db, mode="sync"):
    d = HikDevice(key="stand", name="Стенд", host="10.0.0.5", direction=HikDirection.EXIT, allowed_ips=["10.0.0.5"],
                  response_mode=mode, credentials_env="STAND")
    db.add(d)
    db.commit()
    return d


def test_real_device_gets_failed_unless_pilot_control_enabled(db, setup, mock, monkeypatch):
    permit(db, setup, single_use=False)
    _stand(db)
    for env in [
        dict(HIKVISION_MODE="SIMULATION"),
        dict(HIKVISION_MODE="READ_ONLY"),
        dict(HIKVISION_MODE="PILOT", HIKVISION_CONTROL_ENABLED="0", HIKVISION_CONTROL_DEVICES="stand"),
        dict(HIKVISION_MODE="PILOT", HIKVISION_CONTROL_ENABLED="1", HIKVISION_CONTROL_DEVICES="other"),
    ]:
        monkeypatch.setenv("HIKVISION_CONTROL_ENABLED", "0")
        monkeypatch.setenv("HIKVISION_CONTROL_DEVICES", "")
        for k, v in env.items():
            monkeypatch.setenv(k, v)
        r, out = face(db, mock, device_key="stand", source="10.0.0.5")
        assert r.decision == "ALLOW" and r.check_result == "failed" and r.command_status == "blocked", env
        assert not out.door_opened

    monkeypatch.setenv("HIKVISION_MODE", "PILOT")
    monkeypatch.setenv("HIKVISION_CONTROL_ENABLED", "1")
    monkeypatch.setenv("HIKVISION_CONTROL_DEVICES", "stand")
    r, out = face(db, mock, device_key="stand", source="10.0.0.5")
    assert (r.check_result, r.command_status) == ("success", "sent") and out.door_opened
    # В PILOT виртуальный терминал не открывается
    r, out = face(db, mock)
    assert r.command_status == "blocked" and not out.door_opened


def test_async_mode_sends_put_remote_check(db, setup, monkeypatch):
    permit(db, setup)
    _stand(db, mode="async")
    monkeypatch.setenv("HIKVISION_MODE", "PILOT")
    monkeypatch.setenv("HIKVISION_CONTROL_ENABLED", "1")
    monkeypatch.setenv("HIKVISION_CONTROL_DEVICES", "stand")
    mock = MockHikvisionDevice(listen_mode="async")
    s = hik_settings.load()
    factory = lambda d: IsapiClient(d, s, transport=mock.transport(), credentials=(mock.username, mock.password))  # noqa: E731

    holder = {}

    def post(ct, body):
        r = handle_device_request(db, "stand", "10.0.0.5", ct, body, client_factory=factory)
        holder["r"] = r
        return r.http_status, b""

    out = mock.present_face(post, PILOT_NO)
    r = holder["r"]
    assert r.body is None and r.http_status == 200  # на POST — только 200 OK
    assert mock.remote_check_puts == [{"serialNo": out.serial_no, "checkResult": "success"}]
    assert out.door_opened
    assert mock.forbidden_calls == []
    cmd = db.scalar(select(HikCommand).where(HikCommand.kind == "remote_check_put"))
    assert cmd.status == "sent" and cmd.http_status == 200
