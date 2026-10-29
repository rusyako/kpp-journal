import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import config, db as database, scheduler
from app.api import admin, advisor, auth, kpp
from app.deps import resolve_user
from app.events import hub
from app.services.auth import SESSION_COOKIE

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    hub.bind_loop(asyncio.get_running_loop())
    if config.SCHEDULER_ENABLED:
        scheduler.start()
    yield
    scheduler.stop()


app = FastAPI(title="Журнал КПП", lifespan=lifespan)
for module in (auth, kpp, advisor, admin):
    app.include_router(module.router)


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}


@app.websocket("/api/ws")
async def websocket(ws: WebSocket, tg: str | None = None) -> None:
    """Сигналы «что-то изменилось». tg — initData для Mini App (в WebSocket нельзя задать заголовок)."""
    with database.SessionLocal() as db:
        user = resolve_user(db, tg, ws.cookies.get(SESSION_COOKIE))
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
