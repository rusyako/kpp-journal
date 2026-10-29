from datetime import date, time

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.importer import (
    StudentRow,
    advisory_sort_key,
    apply_import,
    clean_class,
    parse_rows,
)
from app.models import Advisory, AdvisoryKind, Base, Permission, Student


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("5B", "5B"),
        ("5 b", "5B"),
        ("5Б", "5B"),
        ("1А", "1A"),  # кириллическая А
        ("10A", "10A"),
        ("Alpha α1", "Alpha α1"),
        ("альфа 2", "Alpha α2"),
        ("Alpha", "Alpha"),
        ("cdc", "CDC"),
        ("СДС", "CDC"),
        ("13A", None),
        ("", None),
        ("кабинет 12", None),
    ],
)
def test_clean_class(raw, expected):
    assert clean_class(raw) == expected


def test_parse_rows_cleaning():
    result = parse_rows(
        [
            ("  Ким   Илья ", "7A", "КОТИКИ"),
            ("Ахметов Арман", "8B", "Котики"),
            ("Сейітов Ақтілек", "9A", "Котики"),
            ("Тастемиров Әлихан", "1A", "2А"),  # начальная школа: эдвайзери = класс
            ("Ким Илья", "7A", "Котики"),  # повтор
            ("Гарамов Ислам", "6A", ""),  # нет эдвайзери
            ("Қали Аяулым", "??", "Котики"),  # класс не распознан
            (None, None, None),
            ("Жеңісханқызы Жансая", "Alpha", None),
        ]
    )
    assert result.rows == [
        StudentRow("Ким Илья", "7A", "Котики"),
        StudentRow("Ахметов Арман", "8B", "Котики"),
        StudentRow("Сейітов Ақтілек", "9A", "Котики"),
        StudentRow("Тастемиров Әлихан", "1A", "1A"),
        StudentRow("Жеңісханқызы Жансая", "Alpha", "Alpha"),
    ]
    assert len(result.warnings) == 3


def test_all_caps_group_gets_capitalized():
    result = parse_rows([("Ким Илья", "7A", "ЗЕЛЁНЫЕ ДРАКОНЫ"), ("Ким Ирина", "7B", "ЗЕЛЕНЫЕ ДРАКОНЫ")])
    assert {r.advisory for r in result.rows} == {"Зелёные драконы"}


def test_advisory_order():
    names = ["Котики", "2B", "CDC", "Alpha α2", "1A", "10A-группа", "Alpha α1", "1B", "Барсы"]
    # 1A … 5B, затем остальные по алфавиту (латиница раньше кириллицы)
    assert sorted(names, key=advisory_sort_key) == [
        "1A", "1B", "2B", "10A-группа", "Alpha α1", "Alpha α2", "CDC", "Барсы", "Котики",
    ]


@pytest.fixture
def session():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        yield s


FIRST = [
    StudentRow("Ким Илья", "7A", "Котики"),
    StudentRow("Ахметов Арман", "1A", "1A"),
    StudentRow("Гарамов Ислам", "8B", "Барсы"),
    StudentRow("Қали Аяулым", "2B", "2B"),
]


def test_first_import(session):
    diff = apply_import(session, FIRST)
    assert len(diff.added) == 4
    assert diff.new_advisories == ["1A", "2B", "Барсы", "Котики"]
    advisories = session.scalars(select(Advisory).order_by(Advisory.sort_order)).all()
    assert [a.name for a in advisories] == ["1A", "2B", "Барсы", "Котики"]
    assert advisories[0].kind is AdvisoryKind.PRIMARY
    assert advisories[2].kind is AdvisoryKind.GROUP
    kim = session.scalar(select(Student).where(Student.full_name == "Ким Илья"))
    assert kim.full_name_norm == "ким илья"


def test_reimport_keeps_permissions_and_history(session):
    apply_import(session, FIRST)
    kim = session.scalar(select(Student).where(Student.full_name == "Ким Илья"))
    session.add(Permission(date=date(2026, 10, 29), student_id=kim.id, allowed_time=time(15, 5), raw_time="1505"))
    session.flush()

    second = [
        StudentRow("Ким Илья", "7A", "Барсы"),  # сменил эдвайзери
        StudentRow("Ахметов Арман", "2A", "2A"),  # переведён в другой класс
        StudentRow("Новенький Тимур", "1A", "1A"),  # П-13: новенький
        # Гарамов выбыл; Қали выбыла — с ней исчезает эдвайзери 2B
    ]
    diff = apply_import(session, second)

    assert [r.full_name for r in diff.added] == ["Новенький Тимур"]
    assert [r.full_name for _, r in diff.moved] == ["Ахметов Арман"]
    assert [r.full_name for _, r in diff.advisory_changed] == ["Ким Илья"]
    assert sorted(s.full_name for s in diff.removed) == ["Гарамов Ислам", "Қали Аяулым"]
    assert diff.removed_advisories == ["2B", "Котики"]

    # Разрешение, записанное эдвайзером, никуда не делось (Ф-24)
    perm = session.scalar(select(Permission))
    assert perm.student_id == kim.id and perm.allowed_time == time(15, 5)
    assert session.get(Student, kim.id).advisory.name == "Барсы"

    garamov = session.scalar(select(Student).where(Student.full_name == "Гарамов Ислам"))
    assert garamov.active is False
    assert session.scalar(select(Advisory).where(Advisory.name == "Котики")).active is False

    # Повторная загрузка того же списка ничего не меняет
    assert apply_import(session, second).is_empty


def test_returning_student_is_reactivated(session):
    apply_import(session, FIRST)
    apply_import(session, FIRST[:3])
    diff = apply_import(session, FIRST)
    assert [r.full_name for _, r in diff.reactivated] == ["Қали Аяулым"]
    assert diff.added == []
