"""Подключение к терминалу для CLI-инструментов: --mock | --device KEY (из БД) | --host IP."""

import argparse
import getpass
import os
import sys
from types import SimpleNamespace

from sqlalchemy import select

from app.integrations.hikvision.client import IsapiClient
from app.integrations.hikvision.mock_device import MockHikvisionDevice, MockUser
from app.integrations.hikvision.settings import HikSettings

STAFF_DEMO = "1000000001"


def add_target_args(p: argparse.ArgumentParser) -> None:
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--mock", action="store_true", help="виртуальный терминал (без сети)")
    g.add_argument("--device", help="ключ терминала из kpp-journal (pilot-device), учётные данные из HIK_<X>_USER/_PASSWORD")
    g.add_argument("--host", help="IP терминала; учётные данные из HIK_DIAG_USER/HIK_DIAG_PASSWORD или ввод")
    p.add_argument("--port", type=int, default=80)
    p.add_argument("--scheme", default="http", choices=["http", "https"])
    p.add_argument("--confirm-network", action="store_true",
                   help="подтверждаю: есть разрешение на запросы к этому терминалу (для --device/--host)")


def demo_mock(pilot_no: str) -> MockHikvisionDevice:
    """Виртуальный терминал «как сейчас»: удалённая проверка выключена, httpHosts свободен;
    тестовая запись (normal, 1 лицо, 1 карта) и сотрудник normal."""
    return MockHikvisionDevice(users={pilot_no: MockUser(pilot_no), STAFF_DEMO: MockUser(STAFF_DEMO)},
                               remote_check_enabled=False, http_host_configured=False)


def build_client(args, settings: HikSettings, pilot_no: str):
    """→ (client, device, db_device | None, mock | None). Выход с кодом 2, если запросы не разрешены."""
    def stop(msg: str):
        print(msg, file=sys.stderr)
        raise SystemExit(2)

    if args.mock:
        mock = demo_mock(pilot_no)
        device = SimpleNamespace(key="mock", simulated=True, active=True, host="", port=80, scheme="http", credentials_env=None)
        return IsapiClient(device, settings, transport=mock.transport(), credentials=(mock.username, mock.password)), device, None, mock
    if not args.confirm_network:
        stop("Запросы к реальному терминалу — только с разрешения: добавьте --confirm-network")
    if not settings.network_allowed():
        stop(f"HIKVISION_MODE={settings.mode}: сеть к терминалам выключена (нужен READ_ONLY или PILOT)")
    if args.device:
        from app.db import SessionLocal
        from app.models import HikDevice

        with SessionLocal() as db:
            device = db.scalar(select(HikDevice).where(HikDevice.key == args.device))
            if device is None or device.simulated:
                stop(f"Терминал «{args.device}» не зарегистрирован (python -m app.cli pilot-device …)")
            db.expunge(device)
        return IsapiClient(device, settings), device, device, None
    user = os.environ.get("HIK_DIAG_USER") or input("Логин терминала: ").strip()
    password = os.environ.get("HIK_DIAG_PASSWORD") or getpass.getpass("Пароль терминала: ")
    device = SimpleNamespace(key=args.host, simulated=False, active=True, host=args.host, port=args.port,
                             scheme=args.scheme, credentials_env=None)
    return IsapiClient(device, settings, credentials=(user, password)), device, None, None


def utf8_console() -> None:
    try:
        sys.stdout.reconfigure(errors="replace")
    except AttributeError:
        pass
