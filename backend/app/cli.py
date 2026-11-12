"""Служебные команды:

    python -m app.cli create-admin <логин> "<Имя>"     # пароль спросит или возьмёт из ADMIN_PASSWORD
    python -m app.cli send-report [ГГГГ-ММ-ДД]
    python -m app.cli demo                             # вымышленные данные для проверки
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


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
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


if __name__ == "__main__":
    main()
