import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import config, db as database, scheduler
from app.api import admin, advisor, auth, kpp, pilot
from app.deps import resolve_user
from app.events import hub
from app.services.auth import SESSION_COOKIE

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    if problem := config.secret_key_problem():
        raise RuntimeError(f"{problem}. Задайте в deploy/.env случайную строку: openssl rand -hex 32")
    hub.bind_loop(asyncio.get_running_loop())
    if config.SCHEDULER_ENABLED:
        scheduler.start()
    yield
    scheduler.stop()


app = FastAPI(title="Журнал КПП", lifespan=lifespan)
for module in (auth, kpp, advisor, admin, pilot):
    app.include_router(module.router)


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


WS_AUTH_PREFIX = "auth:"
WS_AUTH_TIMEOUT = 10  # секунд


def _ws_user(init_data: str | None, session_token: str | None):
    with database.SessionLocal() as db:
        return resolve_user(db, init_data, session_token)


@app.websocket("/api/ws")
async def websocket(ws: WebSocket) -> None:
    """Сигналы «что-то изменилось».

    Браузер входит по cookie. Mini App cookie не имеет и шлёт initData первым сообщением
    «auth:<initData>»: в адресе его передавать нельзя — адреса попадают в журналы сервера.
    """
    await ws.accept()
    user = _ws_user(None, ws.cookies.get(SESSION_COOKIE))
    if user is None:
        try:
            first = await asyncio.wait_for(ws.receive_text(), timeout=WS_AUTH_TIMEOUT)
        except asyncio.TimeoutError:
            first = ""
        except WebSocketDisconnect:
            return
        if first.startswith(WS_AUTH_PREFIX):
            user = _ws_user(first[len(WS_AUTH_PREFIX):], None)
    if user is None:
        await ws.close(code=4401)
        return
    await hub.connect(ws)
    try:
        while True:
            await ws.receive_text()  # клиент шлёт ping, ответ не нужен
    except WebSocketDisconnect:
        pass
    finally:
        hub.disconnect(ws)


# Собранный React: /assets/* — файлы, всё остальное (кроме /api) — index.html
if (config.STATIC_DIR / "index.html").exists():
    app.mount("/assets", StaticFiles(directory=config.STATIC_DIR / "assets"), name="assets")

    @app.get("/{path:path}", include_in_schema=False)
    def spa(path: str) -> FileResponse:
        if path.startswith("api/"):
            raise HTTPException(404)
        file = (config.STATIC_DIR / path).resolve()
        if path and file.is_file() and config.STATIC_DIR.resolve() in file.parents:
            return FileResponse(file)
        return FileResponse(config.STATIC_DIR / "index.html")
