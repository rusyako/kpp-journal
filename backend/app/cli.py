"""Служебные команды:

    python -m app.cli create-admin <логин> "<Имя>"     # пароль спросит или возьмёт из ADMIN_PASSWORD
    python -m app.cli send-report [ГГГГ-ММ-ДД]
    python -m app.cli demo                             # вымышленные данные для проверки
    python -m app.cli pilot-setup                      # виртуальные терминалы + запись пилота Hikvision
    python -m app.cli pilot-device <key> --host IP --allowed-ips IP --credentials-env STAND   # зарегистрировать терминал
"""

import argparse
import getpass
import os
from datetime import date

from sqlalchemy import select

from app import clock
from app.db import SessionLocal
from app.importer import StudentRow, apply_import
from app.models import Advisory, Role, User
from app.services.auth import hash_password
from app.services.report import send_report


def create_admin(username: str, name: str) -> None:
    password = os.environ.get("ADMIN_PASSWORD") or getpass.getpass("Пароль: ")
    if len(password) < 8:
        raise SystemExit("Пароль — не короче 8 символов")
    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.username == username.lower()))
        if user is None:
            user = User(username=username.lower(), role=Role.ADMIN, display_name=name)
            db.add(user)
        user.role, user.display_name, user.active = Role.ADMIN, name, True
        user.password_hash = hash_password(password)
        user.revoke_sessions()
        db.commit()
    print(f"✅ Администратор {username} готов")


DEMO_STUDENTS = [
    ("Ахметов Арман", "1A"), ("Ахметова Дана", "1A"), ("Ақтілекқызы Аружан", "1B"),
    ("Тастемиров Әлихан", "2A"), ("Қали Аяулым", "2A"), ("Гилёва Мария", "5B"),
    ("Ким Илья", "7A", "Котики"), ("Ким Ирина", "8B", "Котики"), ("Гарамов Ислам", "9A", "Котики"),
    ("Сейітов Ақтілек", "10A", "Барсы"), ("Гарамова Дана", "11B", "Барсы"), ("Ма'руфов Азиз", "12A", "Барсы"),
    ("Жеңісханқызы Жансая", "Alpha α1"), ("Нұрланов Тимур", "CDC"),
]


def demo() -> None:
    """Вымышленные ученики и пользователи (пароль у всех: demo-pass-123)."""
    rows = [StudentRow(n, c, a[0] if a else c) for n, c, *a in DEMO_STUDENTS]
    pw = hash_password("demo-pass-123")
    with SessionLocal() as db:
        apply_import(db, rows)
        db.flush()
        advisories = {a.name: a for a in db.scalars(select(Advisory))}
        for username, role, name, adv in [
            ("admin", Role.ADMIN, "Администратор", []),
            ("kpp", Role.GUARD, "Охрана КПП", []),
            ("kotiki", Role.ADVISOR, "Эдвайзер Котиков", ["Котики"]),
            ("primary", Role.ADVISOR, "Эдвайзер 1A", ["1A"]),
            ("director", Role.VIEWER, "Руководство", []),
        ]:
            user = db.scalar(select(User).where(User.username == username))
            if user is None:
                user = User(username=username, role=role, display_name=name, password_hash=pw)
                db.add(user)
            user.advisories = [advisories[a] for a in adv]
        db.commit()
    print("✅ Демо-данные: admin / kpp / kotiki / primary / director, пароль demo-pass-123")


def pilot_setup() -> None:
    from app.services.pilot import ensure_setup

    with SessionLocal() as db:
        print(ensure_setup(db, None))


def pilot_device(args) -> None:
    """Зарегистрировать терминал в kpp-journal. На само устройство ничего не отправляет."""
    from app.models import HikDevice, HikDirection

    with SessionLocal() as db:
        device = db.scalar(select(HikDevice).where(HikDevice.key == args.key))
        if device is None:
            device = HikDevice(key=args.key, name=args.name or args.key, direction=HikDirection(args.direction))
            db.add(device)
        device.name = args.name or device.name
        device.host, device.port, device.scheme = args.host, args.port, args.scheme
        device.direction = HikDirection(args.direction)
        device.allowed_ips = [ip.strip() for ip in args.allowed_ips.split(",") if ip.strip()]
        device.credentials_env = args.credentials_env
        device.response_mode = args.response_mode
        device.door_no = args.door_no
        device.simulated, device.active = False, not args.inactive
        db.commit()
    print(f"✅ Терминал {args.key}: {args.host}, {args.direction}, приём событий с {args.allowed_ips or '— (никого)'}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pilot-setup")
    p = sub.add_parser("pilot-device")
    p.add_argument("key")
    p.add_argument("--name")
    p.add_argument("--host", required=True)
    p.add_argument("--port", type=int, default=80)
    p.add_argument("--scheme", default="http", choices=["http", "https"])
    p.add_argument("--direction", default="exit", choices=["exit", "entry"])
    p.add_argument("--allowed-ips", default="", help="с каких IP принимать события (через запятую)")
    p.add_argument("--credentials-env", help="префикс HIK_<X>_USER / HIK_<X>_PASSWORD")
    p.add_argument("--response-mode", default="sync", choices=["sync", "async"])
    p.add_argument("--door-no", type=int, default=1)
    p.add_argument("--inactive", action="store_true")
    p = sub.add_parser("create-admin")
    p.add_argument("username")
    p.add_argument("name")
    p = sub.add_parser("send-report")
    p.add_argument("day", nargs="?", type=date.fromisoformat)
    sub.add_parser("demo")
    args = parser.parse_args()

    if args.cmd == "create-admin":
        create_admin(args.username, args.name)
    elif args.cmd == "send-report":
        with SessionLocal() as db:
            print(send_report(db, args.day or clock.today()))
    elif args.cmd == "demo":
        demo()
    elif args.cmd == "pilot-setup":
        pilot_setup()
    elif args.cmd == "pilot-device":
        pilot_device(args)


if __name__ == "__main__":
    main()
