"""Hikvision Adapter без оборудования: разбор запросов, ISAPI-клиент, белый список операций, mock-терминал."""

from types import SimpleNamespace

import httpx
import pytest

from app.integrations.hikvision import settings as hik_settings
from app.integrations.hikvision.client import (
    AuthLockout,
    ForbiddenOperation,
    IsapiClient,
    IsapiError,
    NetworkDisabled,
    check_operation,
)
from app.integrations.hikvision.diagnostics import redact, run
from app.integrations.hikvision.mock_device import MockHikvisionDevice
from app.integrations.hikvision.parsing import ParseError, parse_request, peek_serial

# Дословный пример запроса удалённой проверки из FRT §10.16.4.2.3, с.133 (LF вместо CRLF, как в PDF)
FRT_P133 = b"""--boundary
Content-Disposition: form-data; name="AccessControllerEvent"
Content-Type: application/json; charset="UTF-8"
Content-Length: 202

{
    "ipAddress": "10.6.123.199",
    "portNo": 80,
    "channelID": 6,
    "dateTime": "2022-11-14T13:41:56+08:00",
    "activePostCount": 1,
    "eventType": "AccessControllerEvent",
    "eventState": "active",
    "eventDescription": "Access Controller Event",
    "AccessControllerEvent": {
        "deviceName": "Access Controller",
        "majorEventType": 5,
        "subEventType": 75,
        "time": "2022-11-14T13:41:56+08:00",
        "name":  "test123",
        "employeeNoString":  "test",
        "serialNo": 1866,
        "currentEvent": true,
        "remoteCheck":  true,
        "frontSerialNo": 1865,
        "picturesNumber":  1
    }
}
--boundary
Content-Disposition: form-data; name="Picture";filename="Picture.jpg";
Content-Type: image/jpeg
Content-Length: 8

\xff\xd8\xff\xe0JPEG
--boundary--
"""


def device(**kw):
    base = dict(key="stand", simulated=False, active=True, host="192.0.2.10", port=80, scheme="http", credentials_env=None)
    base.update(kw)
    return SimpleNamespace(**base)


def settings(monkeypatch, **env) -> hik_settings.HikSettings:
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    return hik_settings.load()


# ---------- Разбор ----------


def test_parse_documentation_example():
    ev = parse_request("multipart/form-data;boundary=boundary", FRT_P133)
    assert ev.remote_check is True
    assert ev.category == "remote_check"
    assert (ev.major, ev.minor, ev.serial_no, ev.front_serial_no) == (5, 75, 1866, 1865)
    assert ev.employee_no == "test"
    assert ev.current_event is True
    assert ev.date_time is not None and ev.date_time.utcoffset().total_seconds() == 5 * 3600  # приведено к поясу школы
    assert ev.pictures_dropped == 1
    # ФИО и фото не сохраняются
    assert "name" not in ev.sanitized["AccessControllerEvent"]
    assert "picturesNumber" not in ev.sanitized["AccessControllerEvent"]


def test_parse_crlf_and_employee_no_variants():
    mock = MockHikvisionDevice()
    ev = mock.event("3818077855")
    ct, body = mock.multipart(ev, line_end=b"\r\n")
    parsed = parse_request(ct, body)
    assert parsed.employee_no == "3818077855" and isinstance(parsed.employee_no, str)

    # employeeNoString приоритетнее employeeNo (FRT с.409); без него берётся числовой employeeNo как строка
    ev["AccessControllerEvent"].pop("employeeNoString")
    ev["AccessControllerEvent"]["employeeNo"] = 3818077855
    ct, body = mock.multipart(ev, with_picture=False, line_end=b"\n")
    assert parse_request(ct, body).employee_no == "3818077855"


def test_parse_plain_json_and_xml():
    mock = MockHikvisionDevice()
    import json

    ev = mock.event("42", remote_check=False, minor=218)
    parsed = parse_request("application/json", json.dumps(ev).encode())
    assert parsed.category == "passage" and parsed.remote_check is False

    xml = (b'<?xml version="1.0"?><EventNotificationAlert xmlns="http://www.isapi.org/ver20/XMLSchema">'
           b"<dateTime>2026-10-29T14:00:00+05:00</dateTime><eventType>AccessControllerEvent</eventType>"
           b"<AccessControllerEvent><majorEventType>5</majorEventType><subEventType>75</subEventType>"
           b"<employeeNoString>42</employeeNoString><serialNo>7</serialNo><remoteCheck>true</remoteCheck>"
           b"<currentEvent>true</currentEvent></AccessControllerEvent></EventNotificationAlert>")
    parsed = parse_request("application/xml", xml)
    assert parsed.remote_check and parsed.serial_no == 7 and parsed.employee_no == "42"


@pytest.mark.parametrize(
    "ct,body",
    [
        ("multipart/form-data", b"--x\r\n\r\n{}"),  # нет boundary
        ("application/json", b"{not json"),
        ("application/json", b"[1,2]"),
        ("application/json", b'{"eventType":"AccessControllerEvent"}'),  # нет объекта события
        ("multipart/form-data;boundary=b", b'--b\r\nContent-Type: image/jpeg\r\n\r\n\xff\xd8\r\n--b--'),  # только фото
    ],
)
def test_parse_errors(ct, body):
    with pytest.raises(ParseError):
        parse_request(ct, body)


def test_peek_serial_from_broken_body():
    assert peek_serial("application/json", b'{"serialNo": 55, broken') == 55


# ---------- Белый список операций ----------


def test_forbidden_operations_in_every_mode(monkeypatch):
    for mode in ("SIMULATION", "READ_ONLY", "PILOT"):
        s = settings(monkeypatch, HIKVISION_MODE=mode, HIKVISION_CONTROL_ENABLED="1", HIKVISION_CONTROL_DEVICES="stand")
        d = device()
        for method, path in [
            ("PUT", "/ISAPI/AccessControl/RemoteControl/door/1"),
            ("PUT", "/ISAPI/AccessControl/AcsCfg?format=json"),
            ("POST", "/ISAPI/Event/notification/httpHosts"),
            ("PUT", "/ISAPI/Event/notification/httpHosts/1"),
            ("PUT", "/ISAPI/AccessControl/UserInfo/Modify?format=json"),
            ("POST", "/ISAPI/AccessControl/UserInfo/Record?format=json"),
            ("PUT", "/ISAPI/AccessControl/UserInfoDetail/Delete?format=json"),
            ("POST", "/ISAPI/Intelligent/FDLib/FaceDataRecord?format=json"),
            ("PUT", "/ISAPI/AccessControl/Door/param/1"),
            ("DELETE", "/ISAPI/Event/notification/httpHosts/1"),
            ("POST", "/ISAPI/AccessControl/UserInfo/Search?format=json"),
        ]:
            with pytest.raises(ForbiddenOperation):
                check_operation(method, path, s, d)
        # Чтение разрешено
        check_operation("GET", "/ISAPI/AccessControl/AcsCfg?format=json", s, d)
        check_operation("POST", "/ISAPI/AccessControl/AcsEvent?format=json", s, d)
        with pytest.raises(ForbiddenOperation):
            check_operation("GET", "/ISAPI/Event/notification/alertStream", s, d)


def test_remote_check_put_needs_pilot_flag_and_allowlist(monkeypatch):
    path = "/ISAPI/AccessControl/remoteCheck?format=json"
    d = device()
    for env in [
        dict(HIKVISION_MODE="SIMULATION"),
        dict(HIKVISION_MODE="READ_ONLY", HIKVISION_CONTROL_ENABLED="1", HIKVISION_CONTROL_DEVICES="stand"),
        dict(HIKVISION_MODE="PILOT", HIKVISION_CONTROL_ENABLED="0", HIKVISION_CONTROL_DEVICES="stand"),
        dict(HIKVISION_MODE="PILOT", HIKVISION_CONTROL_ENABLED="1", HIKVISION_CONTROL_DEVICES="other"),
    ]:
        with pytest.raises(ForbiddenOperation):
            check_operation("PUT", path, settings(monkeypatch, **{"HIKVISION_CONTROL_ENABLED": "0",
                                                                 "HIKVISION_CONTROL_DEVICES": "", **env}), d)
    ok = settings(monkeypatch, HIKVISION_MODE="PILOT", HIKVISION_CONTROL_ENABLED="1", HIKVISION_CONTROL_DEVICES="stand")
    check_operation("PUT", path, ok, d)
    # Отключённый терминал — нельзя, даже если он в списке
    with pytest.raises(ForbiddenOperation):
        check_operation("PUT", path, ok, device(active=False))


def test_unknown_mode_falls_back_to_simulation(monkeypatch):
    assert settings(monkeypatch, HIKVISION_MODE="pilot-please").mode is hik_settings.Mode.SIMULATION
    monkeypatch.delenv("HIKVISION_MODE")
    assert hik_settings.load().mode is hik_settings.Mode.SIMULATION


# ---------- ISAPI-клиент на mock-терминале ----------


def test_real_device_has_no_network_in_simulation(monkeypatch):
    s = settings(monkeypatch, HIKVISION_MODE="SIMULATION")
    with pytest.raises(NetworkDisabled):
        IsapiClient(device(), s, credentials=("u", "p"))


def test_credentials_come_from_env_only(monkeypatch):
    s = settings(monkeypatch, HIKVISION_MODE="READ_ONLY")
    with pytest.raises(IsapiError, match="нет учётных данных"):
        IsapiClient(device(credentials_env="stand"), s)
    monkeypatch.setenv("HIK_STAND_USER", "admin")
    monkeypatch.setenv("HIK_STAND_PASSWORD", "secret")
    mock = MockHikvisionDevice(username="admin", password="secret")
    with IsapiClient(device(credentials_env="stand"), s, transport=mock.transport()) as c:
        assert c.device_info().ok


def test_digest_and_read_only_requests(monkeypatch):
    s = settings(monkeypatch, HIKVISION_MODE="READ_ONLY")
    mock = MockHikvisionDevice()
    with IsapiClient(device(), s, transport=mock.transport(), credentials=(mock.username, mock.password)) as c:
        info = c.device_info()
        assert info.ok and info.data["DeviceInfo"]["model"] == "MOCK-TERMINAL"
        assert c.access_capabilities().data["AccessControl"]["isSupportRemoteCheck"] == "true"
        assert c.acs_cfg().data["AcsCfg"]["remoteCheckWithISAPIListen"] == "sync"
        assert c.search_events("3818077855", "2026-10-28T00:00:00+05:00", "2026-10-29T00:00:00+05:00").ok
        with pytest.raises(ForbiddenOperation):
            c.put_remote_check(1, "success")
    # Первый запрос каждого обмена — 401-вызов Digest, затем повтор с Authorization
    assert ("GET", "/ISAPI/System/deviceInfo") in mock.requests
    assert mock.forbidden_calls == [] and mock.remote_check_puts == []


def test_wrong_password_locks_client(monkeypatch):
    s = settings(monkeypatch, HIKVISION_MODE="READ_ONLY")
    mock = MockHikvisionDevice(password="right")
    c = IsapiClient(device(), s, transport=mock.transport(), credentials=("admin", "wrong"))
    with pytest.raises(AuthLockout):
        c.device_info()
    sent = len(mock.requests)
    assert sent == 2  # вызов + одна попытка Digest, без повторов
    with pytest.raises(AuthLockout):
        c.acs_cfg()
    assert len(mock.requests) == sent  # после 401 в сеть больше не ходим


def test_network_timeout_is_isapi_error(monkeypatch):
    s = settings(monkeypatch, HIKVISION_MODE="READ_ONLY")

    def boom(request):
        raise httpx.ReadTimeout("timeout", request=request)

    with IsapiClient(device(), s, transport=httpx.MockTransport(boom), credentials=("a", "b")) as c:
        with pytest.raises(IsapiError, match="таймаут"):
            c.device_info()


def test_diagnostics_on_mock_is_read_only(monkeypatch):
    s = settings(monkeypatch, HIKVISION_MODE="SIMULATION")
    mock = MockHikvisionDevice(supports_user_type_list=False)
    dev = device(simulated=True, host="")
    with IsapiClient(dev, s, transport=mock.transport(), credentials=(mock.username, mock.password)) as c:
        report = run(c, pause_s=0, employee_no="3818077855", events=True)
    v = report["verdict"]
    assert v["isSupportRemoteCheck"] == "true" and v["ISAPIListen"] and v["sync"]
    assert v["remoteCheckUserTypeList_in_caps"] is False
    assert any("изоляция по userType невозможна" in n for n in v["notes"])
    assert all(m in ("GET", "POST") for m, _ in mock.requests)
    assert {p for m, p in mock.requests if m == "POST"} == {"/ISAPI/AccessControl/AcsEvent"}
    assert mock.forbidden_calls == []


def test_redact_hides_passwords_and_names():
    data = {"Door": {"superPassword": "123", "doorName": "A"}, "InfoList": [{"name": "Иванов", "employeeNoString": "1"}]}
    assert redact(data) == {"Door": {"superPassword": "***", "doorName": "A"}, "InfoList": [{"employeeNoString": "1"}]}
