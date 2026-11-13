"""Режимы интеграции и проверки безопасности.

SIMULATION (по умолчанию) — только виртуальные терминалы; в сеть к устройствам не ходим.
READ_ONLY — разрешены GET и поиск журнала событий у реальных терминалов; ответы «success» не отправляются.
PILOT     — «success» может уйти только на терминал из HIKVISION_CONTROL_DEVICES и только при
            HIKVISION_CONTROL_ENABLED=1. Смена userType тестовой записи — только при HIKVISION_USER_WRITE_ENABLED=1
            для терминала из HIKVISION_USER_WRITE_DEVICES. Наличие этих настроек — не разрешение школы менять оборудование.

Настройки читаются из окружения при каждом вызове: так их меняют тесты и нельзя переключить режим из браузера.
"""

import enum
import logging
import os
from dataclasses import dataclass

log = logging.getLogger("hikvision")


class Mode(enum.StrEnum):
    SIMULATION = "SIMULATION"
    READ_ONLY = "READ_ONLY"
    PILOT = "PILOT"


def _csv(name: str, default: str = "") -> frozenset[str]:
    return frozenset(x.strip() for x in os.environ.get(name, default).split(",") if x.strip())


def _int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


@dataclass(frozen=True)
class HikSettings:
    mode: Mode
    control_enabled: bool
    control_devices: frozenset[str]
    pilot_employee_nos: frozenset[str]
    # Сколько ждём решение, прежде чем ответить терминалу «failed». Должно быть меньше remoteCheckTimeout (1–10 с)
    decision_budget_ms: int
    # Насколько время события может отличаться от времени сервера
    max_event_age_s: int
    # Какие subEventType принимаются как запрос на выход. 75 = Face Authentication Completed (ACET с.18)
    allowed_minors: frozenset[int]
    # Сколько после ALLOW ждём событие прохода
    passage_window_s: int
    http_timeout_s: float
    # Пауза между запросами read-only диагностики (защита от блокировки учётной записи)
    request_pause_s: float
    # Какие userType должны идти на удалённую проверку. Запрос от другого типа = нарушение изоляции → DENY
    remote_check_user_types: frozenset[str]
    # Смена userType одной записи (UserInfo/Modify): отдельный флаг и отдельный список терминалов
    user_write_enabled: bool
    user_write_devices: frozenset[str]

    def network_allowed(self) -> bool:
        """Можно ли вообще обращаться к реальным терминалам по сети."""
        return self.mode in (Mode.READ_ONLY, Mode.PILOT)

    def control_allowed(self, device) -> bool:
        """Можно ли отправить терминалу ответ «success» (то есть открыть проход)."""
        if device is None or not device.active:
            return False
        if device.simulated:
            return self.mode is Mode.SIMULATION
        return self.mode is Mode.PILOT and self.control_enabled and device.key in self.control_devices

    def user_write_allowed(self, device) -> bool:
        """Можно ли изменить userType тестовой записи на этом терминале (PUT UserInfo/Modify)."""
        if device is None or not device.active:
            return False
        if device.simulated:
            return self.mode is Mode.SIMULATION
        return self.mode is Mode.PILOT and self.user_write_enabled and device.key in self.user_write_devices

    def public(self) -> dict:
        return {
            "mode": self.mode.value,
            "remote_check_user_types": sorted(self.remote_check_user_types),
            "user_write_enabled": self.user_write_enabled,
            "user_write_devices": sorted(self.user_write_devices),
            "control_enabled": self.control_enabled,
            "control_devices": sorted(self.control_devices),
            "pilot_employee_nos": sorted(self.pilot_employee_nos),
            "decision_budget_ms": self.decision_budget_ms,
            "max_event_age_s": self.max_event_age_s,
            "allowed_minors": sorted(self.allowed_minors),
            "passage_window_s": self.passage_window_s,
        }


def load() -> HikSettings:
    raw_mode = os.environ.get("HIKVISION_MODE", Mode.SIMULATION.value).strip().upper()
    try:
        mode = Mode(raw_mode)
    except ValueError:
        # Опечатка в режиме не должна включать управление
        log.warning("Неизвестный HIKVISION_MODE=%r — работаем в SIMULATION", raw_mode)
        mode = Mode.SIMULATION
    minors = set()
    for x in _csv("HIKVISION_ALLOWED_MINORS", "75"):
        if x.isdigit():
            minors.add(int(x))
    return HikSettings(
        mode=mode,
        control_enabled=os.environ.get("HIKVISION_CONTROL_ENABLED", "0") == "1",
        control_devices=_csv("HIKVISION_CONTROL_DEVICES"),
        pilot_employee_nos=_csv("HIKVISION_PILOT_EMPLOYEE_NOS", "3818077855"),
        decision_budget_ms=max(100, min(_int("HIKVISION_DECISION_BUDGET_MS", 1500), 9000)),
        max_event_age_s=max(5, _int("HIKVISION_MAX_EVENT_AGE_S", 60)),
        allowed_minors=frozenset(minors),
        passage_window_s=max(5, _int("HIKVISION_PASSAGE_WINDOW_S", 30)),
        http_timeout_s=float(_int("HIKVISION_HTTP_TIMEOUT_S", 5)),
        request_pause_s=float(os.environ.get("HIKVISION_REQUEST_PAUSE_S", "1")),
        remote_check_user_types=_csv("HIKVISION_REMOTE_CHECK_USER_TYPES", "visitor"),
        user_write_enabled=os.environ.get("HIKVISION_USER_WRITE_ENABLED", "0") == "1",
        user_write_devices=_csv("HIKVISION_USER_WRITE_DEVICES"),
    )
