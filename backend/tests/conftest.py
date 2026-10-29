import os

os.environ.setdefault("SCHEDULER_ENABLED", "0")
os.environ.setdefault("COOKIE_SECURE", "0")
os.environ.setdefault("STATIC_DIR", "/nonexistent")

from datetime import datetime  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine, select  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app import clock, db as database, notify  # noqa: E402
from app.config import SCHOOL_TZ  # noqa: E402
from app.events import hub  # noqa: E402
from app.importer import StudentRow, apply_import  # noqa: E402
from app.main import app  # noqa: E402
from app.models import Advisory, Base, Role, Student, User  # noqa: E402
from app.services.auth import hash_password  # noqa: E402

PASSWORD = "test-pass-123"
_HASH = hash_password(PASSWORD)

STUDENTS = [
    StudentRow("Ким Илья", "7A", "Котики"),
    StudentRow("Ким Ирина", "8B", "Котики"),
    StudentRow("Гарамов Ислам", "9A", "Котики"),
    StudentRow("Ахметов Арман", "1A", "1A"),
    StudentRow("Ахметова Дана", "1A", "1A"),
    StudentRow("Сейітов Ақтілек", "10A", "Барсы"),
]


class Clock:
    def __init__(self) -> None:
        # Четверг, рабочий день
        self.value = datetime(2026, 10, 29, 14, 0, tzinfo=SCHOOL_TZ)

    def set(self, hh: int, mm: int) -> None:
        self.value = self.value.replace(hour=hh, minute=mm)


@pytest.fixture
def now(monkeypatch) -> Clock:
    c = Clock()
    monkeypatch.setattr(clock, "now", lambda: c.value)
    return c


@pytest.fixture
def sent(monkeypatch) -> list:
    """Что ушло бы в Telegram: [(chat_id, text)]."""
    messages: list = []
    monkeypatch.setattr(notify, "SYNC", True)
    monkeypatch.setattr(notify, "send_telegram", lambda chat_id, text, document=None: messages.append((chat_id, text)) or True)
    return messages


@pytest.fixture
def db(monkeypatch, now, sent):
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(database, "SessionLocal", factory)
    monkeypatch.setattr(hub, "_loop", None)

    with factory() as s:
        apply_import(s, STUDENTS)
        s.flush()
        adv = {a.name: a for a in s.scalars(select(Advisory))}
        users = [
            User(username="admin", role=Role.ADMIN, display_name="Админ", password_hash=_HASH),
            User(username="kpp", role=Role.GUARD, display_name="Охрана", email="kpp@hta.kz", password_hash=_HASH),
            User(username="kotiki", role=Role.ADVISOR, display_name="Эдвайзер Котиков", password_hash=_HASH,
                 telegram_id=1001, advisories=[adv["Котики"]]),
            User(username="barsy", role=Role.ADVISOR, display_name="Эдвайзер Барсов", password_hash=_HASH,
                 telegram_id=1002, advisories=[adv["Барсы"]]),
            User(username="director", role=Role.VIEWER, display_name="Директор", password_hash=_HASH,
                 telegram_id=2001, receives_report=True),
        ]
        s.add_all(users)
        s.commit()
    with factory() as s:
        yield s


def login(username: str) -> TestClient:
    client = TestClient(app)
    r = client.post("/api/auth/login", json={"username": username, "password": PASSWORD})
    assert r.status_code == 200, r.text
    return client


@pytest.fixture
def guard(db) -> TestClient:
    return login("kpp")


@pytest.fixture
def advisor(db) -> TestClient:
    return login("kotiki")


@pytest.fixture
def admin(db) -> TestClient:
    return login("admin")


def student_id(db, name: str) -> int:
    return db.scalar(select(Student.id).where(Student.full_name == name))
