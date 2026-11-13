"""Приём запроса терминала → журнал события → Decision Engine → ответ терминалу.

Синхронный режим (рекомендован, REMOTE_VERIFICATION.md §4): решение уходит в теле ответа на POST терминала
как {"RemoteCheck":{"serialNo":N,"checkResult":"success|failed"}} [FRT §10.16.4.1 шаг 4b, с.131–133].
serialNo берём из события («should be the same as that in the uploaded event message», FRT с.520–521;
в примере на с.133 стоит 1 — это расхождение документации, см. MVP_IMPLEMENTATION.md).

«success» уходит, только если: решение ALLOW И settings.control_allowed(device). Иначе — «failed»,
а в hik_commands записывается status="blocked" (теневое решение).
"""

import logging
import time
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import clock
from app.integrations.hikvision import settings as hik_settings
from app.integrations.hikvision.client import IsapiClient, IsapiError
from app.integrations.hikvision.mock_device import SIM_SOURCE
from app.integrations.hikvision.parsing import ParsedEvent, ParseError, parse_request
from app.integrations.hikvision.settings import HikSettings
from app.models import HikCommand, HikDevice, HikEvent, ReleaseDecision
from app.services import release

log = logging.getLogger("hikvision.adapter")


@dataclass
class GatewayResult:
    http_status: int
    body: dict | None
    event_id: int | None = None
    decision_id: int | None = None
    decision: str | None = None
    reason: str | None = None
    check_result: str | None = None
    command_status: str | None = None
    category: str | None = None


def remote_check_body(serial_no: int | None, check_result: str) -> dict:
    return {"RemoteCheck": {"serialNo": int(serial_no or 0), "checkResult": check_result}}


def is_trusted(device: HikDevice | None, source_ip: str) -> bool:
    if device is None:
        return False
    if device.simulated:
        # Виртуальный терминал — только изнутри приложения, не из сети
        return source_ip == SIM_SOURCE
    return bool(device.allowed_ips) and source_ip in device.allowed_ips


def _store_event(db: Session, parsed: ParsedEvent, device: HikDevice | None, device_key: str, source_ip: str) -> tuple[HikEvent, bool]:
    """Идемпотентная запись. → (событие, это_повтор)."""
    fields = dict(
        device_id=device.id if device else None,
        device_key=device_key[:50],
        source_ip=source_ip[:64],
        serial_no=parsed.serial_no,
        front_serial_no=parsed.front_serial_no,
        event_time=parsed.date_time,
        event_time_raw=parsed.date_time_raw,
        received_at=clock.now(),
        event_type=parsed.event_type[:50],
        major=parsed.major,
        minor=parsed.minor,
        employee_no=parsed.employee_no,
        user_type=parsed.user_type,
        remote_check=parsed.remote_check,
        current_event=parsed.current_event,
        category=parsed.category,
        simulated=bool(device and device.simulated),
        payload=parsed.sanitized,
    )
    key = parsed.dedup_key(device_key if device else f"unknown:{device_key}:{source_ip}")
    ev = HikEvent(dedup_key=key, **fields)
    db.add(ev)
    try:
        db.commit()
        return ev, False
    except IntegrityError:
        db.rollback()
    original = db.scalar(select(HikEvent).where(HikEvent.dedup_key == key))
    dup = HikEvent(dedup_key=None, duplicate_of_id=original.id if original else None, **fields)
    db.add(dup)
    db.commit()
    return dup, True


def _record_command(db: Session, **kw) -> HikCommand:
    cmd = HikCommand(created_at=clock.now(), **kw)
    db.add(cmd)
    db.commit()
    return cmd


def handle_device_request(
    db: Session,
    device_key: str,
    source_ip: str,
    content_type: str,
    body: bytes,
    *,
    settings: HikSettings | None = None,
    deadline: float | None = None,
    client_factory=None,
) -> GatewayResult:
    """Обработать один POST терминала. Никогда не выбрасывает исключение наружу: при сбое — failed."""
    settings = settings or hik_settings.load()
    t0 = time.perf_counter()
    try:
        parsed = parse_request(content_type, body)
    except ParseError as e:
        log.warning("Не разобран запрос от %s (%s): %s", device_key, source_ip, e)
        try:
            _record_command(db, kind="parse_error", status="error", error=str(e)[:300], check_result="failed",
                            payload={"device_key": device_key[:50], "source_ip": source_ip[:64]})
        except Exception:
            db.rollback()
        return GatewayResult(400, None, check_result="failed", command_status="error")

    try:
        return _process(db, parsed, device_key, source_ip, settings, deadline, client_factory, t0)
    except Exception:
        # БД недоступна, ошибка в коде и т.п. — нового автоматического разрешения нет
        log.exception("Сбой обработки запроса от %s — ответ failed", device_key)
        try:
            db.rollback()
        except Exception:
            pass
        body = remote_check_body(parsed.serial_no, "failed") if parsed.remote_check else None
        return GatewayResult(200, body, reason="internal_error", check_result="failed", command_status="error",
                             category=parsed.category)


def _process(db, parsed: ParsedEvent, device_key, source_ip, settings, deadline, client_factory, t0) -> GatewayResult:
    device = db.scalar(select(HikDevice).where(HikDevice.key == device_key))
    event, duplicate = _store_event(db, parsed, device, device_key, source_ip)
    if device is not None:
        device.last_event_at = event.received_at
        db.commit()

    if not parsed.remote_check:
        # Не запрос, а факт: проход, дверь, heartbeat… Решений не принимаем, только журнал
        if not duplicate and is_trusted(device, source_ip):
            release.record_device_passage(db, event, settings)
        return GatewayResult(200, None, event_id=event.id, category=event.category)

    decision = release.decide_exit(
        db, release.ExitRequest(event=event, device=device, source_trusted=is_trusted(device, source_ip), duplicate=duplicate),
        settings, deadline,
    )
    return _respond(db, settings, device, event, decision, parsed, t0, client_factory)


def _respond(db, settings, device, event, decision: ReleaseDecision, parsed, t0, client_factory) -> GatewayResult:
    allowed_to_open = decision.result == release.ALLOW and settings.control_allowed(device)
    check_result = "success" if allowed_to_open else "failed"
    if decision.result == release.ALLOW and not allowed_to_open:
        status = "blocked"  # теневое решение: режим не разрешает открывать этот терминал
    elif device is not None and device.simulated:
        status = "simulated"
    else:
        status = "sent"

    body = remote_check_body(parsed.serial_no, check_result)
    base = dict(device_id=device.id if device else None, decision_id=decision.id, event_id=event.id, check_result=check_result)

    if device is not None and device.response_mode == "async" and status != "blocked":
        # Асинхронный режим: 200 на POST, решение — отдельным PUT /ISAPI/AccessControl/remoteCheck
        status, http_status, error = _put_async(settings, device, parsed.serial_no, check_result, client_factory)
        _record_command(db, kind="remote_check_put", method="PUT", path="/ISAPI/AccessControl/remoteCheck",
                        status=status, http_status=http_status, error=error,
                        latency_ms=int((time.perf_counter() - t0) * 1000), payload=body, **base)
        return GatewayResult(200, None, event.id, decision.id, decision.result, decision.reason, check_result, status, event.category)

    _record_command(db, kind="remote_check_sync_response", method="RESP", status=status, http_status=200,
                    latency_ms=int((time.perf_counter() - t0) * 1000), payload=body, **base)
    return GatewayResult(200, body, event.id, decision.id, decision.result, decision.reason, check_result, status, event.category)


def _put_async(settings, device, serial_no, check_result, client_factory) -> tuple[str, int | None, str | None]:
    try:
        factory = client_factory or (lambda d: IsapiClient(d, settings))
        with factory(device) as client:
            r = client.put_remote_check(serial_no, check_result)
        return ("simulated" if device.simulated else "sent") if r.ok else "error", r.status, None if r.ok else str(r.data)[:300]
    except IsapiError as e:
        log.warning("PUT remoteCheck на «%s» не выполнен: %s", device.key, e)
        return "error", None, str(e)[:300]


def record_timeout(db: Session, device_key: str, serial_no: int | None, budget_ms: int) -> None:
    """Терминалу ответили failed по истечении бюджета времени."""
    device = db.scalar(select(HikDevice).where(HikDevice.key == device_key))
    _record_command(db, device_id=device.id if device else None, kind="remote_check_sync_response", method="RESP",
                    status="timeout", http_status=200, check_result="failed", latency_ms=budget_ms,
                    error=f"решение не готово за {budget_ms} мс", payload=remote_check_body(serial_no, "failed"))
