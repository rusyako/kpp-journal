"""Рассылка событий по WebSocket: охрана и эдвайзеры видят изменения сразу.

Событие несёт только «что изменилось»; клиент сам перечитывает свои данные,
поэтому через сокет не уходят чужие персональные данные.
"""

import asyncio
import logging

from fastapi import WebSocket

log = logging.getLogger(__name__)


class Hub:
    def __init__(self) -> None:
        self._clients: set[WebSocket] = set()
        self._loop: asyncio.AbstractEventLoop | None = None

    def bind_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        self._clients.add(ws)

    def disconnect(self, ws: WebSocket) -> None:
        self._clients.discard(ws)

    async def _send_all(self, event: dict) -> None:
        for ws in list(self._clients):
            try:
                await ws.send_json(event)
            except Exception:
                self._clients.discard(ws)

    def publish(self, event: dict) -> None:
        """Можно звать из синхронного кода (обработчики FastAPI идут в пуле потоков)."""
        loop = self._loop
        if loop is None or loop.is_closed():
            return
        try:
            running = asyncio.get_running_loop()
        except RuntimeError:
            running = None
        if running is loop:
            loop.create_task(self._send_all(event))
        else:
            asyncio.run_coroutine_threadsafe(self._send_all(event), loop)


hub = Hub()


def day_changed(date_iso: str, student_id: int, advisory_id: int) -> None:
    hub.publish({"type": "changed", "date": date_iso, "student_id": student_id, "advisory_id": advisory_id})
