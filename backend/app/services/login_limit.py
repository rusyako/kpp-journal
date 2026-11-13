"""Ограничение попыток входа: защита паролей от перебора.

Хранится в памяти процесса — API работает одним воркером (см. Dockerfile).
После перезапуска счётчики обнуляются, это допустимо.
"""

import threading
import time
from collections import defaultdict, deque

WINDOW = 15 * 60  # секунд
# Неудачных попыток за окно:
PER_IP_AND_USER = 5  # с одного адреса под одним логином
PER_IP = 30  # с одного адреса под любыми логинами
PER_USER = 50  # под одним логином с любых адресов (подбор с многих адресов)

_lock = threading.Lock()
_failures: dict[tuple, deque] = defaultdict(deque)


def _keys(ip: str, username: str) -> list[tuple[tuple, int]]:
    return [(("iu", ip, username), PER_IP_AND_USER), (("ip", ip), PER_IP), (("u", username), PER_USER)]


def _trim(q: deque, now: float) -> None:
    while q and now - q[0] > WINDOW:
        q.popleft()


def retry_after(ip: str, username: str) -> int:
    """0 — можно пробовать; иначе через сколько секунд."""
    now = time.monotonic()
    wait = 0
    with _lock:
        for key, limit in _keys(ip, username):
            q = _failures.get(key)
            if not q:
                continue
            _trim(q, now)
            if len(q) >= limit:
                wait = max(wait, int(WINDOW - (now - q[0])) + 1)
    return wait


def failed(ip: str, username: str) -> None:
    now = time.monotonic()
    with _lock:
        for key, _ in _keys(ip, username):
            q = _failures[key]
            _trim(q, now)
            q.append(now)


def succeeded(ip: str, username: str) -> None:
    with _lock:
        _failures.pop(("iu", ip, username), None)


def reset() -> None:
    with _lock:
        _failures.clear()
