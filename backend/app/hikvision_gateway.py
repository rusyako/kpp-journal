"""Приёмник запросов терминалов Hikvision — отдельный процесс (Listening, FRT §10.16.3–10.16.4).

    uvicorn app.hikvision_gateway:app --host <IP в сети терминалов> --port 8090

Наружу (через Caddy) не публикуется: слушает только сеть/VLAN терминалов. Кроме того, каждый реальный терминал
должен быть в БД с непустым allowed_ips — запросы с других адресов получают DENY (untrusted_source).
Управляющих endpoint’ов (открыть дверь и т.п.) здесь нет и не будет.
"""

import asyncio
import logging
import time

from fastapi import FastAPI, Request, Response
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse

from app import db as database
from app.integrations.hikvision import settings as hik_settings
from app.integrations.hikvision.adapter import handle_device_request, record_timeout, remote_check_body
from app.integrations.hikvision.parsing import MAX_BODY, peek_serial

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("hikvision.gateway")

app = FastAPI(title="kpp-journal: приёмник Hikvision", docs_url=None, redoc_url=None, openapi_url=None)


def _process(device_key: str, source_ip: str, content_type: str, body: bytes, deadline: float):
    with database.SessionLocal() as db:
        return handle_device_request(db, device_key, source_ip, content_type, body, deadline=deadline)


def _timeout(device_key: str, serial: int | None, budget_ms: int) -> None:
    try:
        with database.SessionLocal() as db:
            record_timeout(db, device_key, serial, budget_ms)
    except Exception:
        log.exception("Не удалось записать таймаут")


@app.post("/hikvision/listen/{device_key}")
async def listen(device_key: str, request: Request) -> Response:
    settings = hik_settings.load()
    budget_s = settings.decision_budget_ms / 1000
    deadline = time.monotonic() + budget_s
    body = await request.body()
    if len(body) > MAX_BODY:
        return Response(status_code=413)
    content_type = request.headers.get("content-type", "")
    source_ip = request.client.host if request.client else ""
    try:
        result = await asyncio.wait_for(
            run_in_threadpool(_process, device_key, source_ip, content_type, body, deadline), timeout=budget_s
        )
    except asyncio.TimeoutError:
        serial = peek_serial(content_type, body)
        log.warning("Решение для %s не готово за %d мс — ответ failed", device_key, settings.decision_budget_ms)
        asyncio.get_running_loop().run_in_executor(None, _timeout, device_key, serial, settings.decision_budget_ms)
        return JSONResponse(remote_check_body(serial, "failed"), headers={"Connection": "close"})
    if result.body is not None:
        return JSONResponse(result.body, status_code=result.http_status, headers={"Connection": "close"})
    return Response(status_code=result.http_status, headers={"Connection": "close"})


@app.get("/hikvision/health")
def health() -> dict:
    s = hik_settings.load()
    return {"ok": True, "mode": s.mode.value}
