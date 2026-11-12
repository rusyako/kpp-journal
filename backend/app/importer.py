"""Загрузка списка учеников из листа «Для журнала» (Ф-22, Ф-24, правила раздела 4).

Сначала строится план изменений (diff) — его показывают администратору,
применяется он только после подтверждения:

    python -m app.importer spisok.xlsx            # показать изменения
    python -m app.importer spisok.xlsx --apply    # применить
"""

import argparse
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Advisory, AdvisoryKind, Student
from app.services.normalize import normalize

SHEET_NAME = "Для журнала"

_SPACES = re.compile(r"\s+")
_GRADE_CLASS = re.compile(r"^(\d{1,2})\s*-?\s*([A-Za-zА-Яа-я])$")
# Буквы класса пишут и кириллицей: «5Б», «5В» (похоже на B), «5А»
_CLASS_LETTERS = {"А": "A", "Б": "B", "В": "B", "С": "C", "Д": "D", "Е": "E"}
_ALPHA = re.compile(r"^(alpha|альфа)\s*(?:α|a|а)?\s*([12])?\s*$", re.IGNORECASE)
_CDC = {"cdc", "сдс"}  # второе — кириллицей


@dataclass(frozen=True)
class StudentRow:
    full_name: str
    class_name: str
    advisory: str


@dataclass
class ParseResult:
    rows: list[StudentRow]
    warnings: list[str]
    # Ошибки, при которых список загружать нельзя (например, два класса слились бы в один)
    errors: list[str] = field(default_factory=list)


def class_letter_source(text: str) -> str | None:
    """Буква класса как она записана в файле («Б» в «5 б»), до перевода в латиницу."""
    m = _GRADE_CLASS.match(clean_name(text))
    return m[2].upper() if m else None


@dataclass(frozen=True)
class ExistingStudent:
    id: int
    full_name: str
    class_name: str
    advisory: str
    active: bool


@dataclass
class ImportDiff:
    added: list[StudentRow] = field(default_factory=list)
    # Тот же ребёнок в другом классе: имя совпало ровно с одним выбывшим
    moved: list[tuple[int, StudentRow]] = field(default_factory=list)
    advisory_changed: list[tuple[int, StudentRow]] = field(default_factory=list)
    reactivated: list[tuple[int, StudentRow]] = field(default_factory=list)
    removed: list[ExistingStudent] = field(default_factory=list)
    new_advisories: list[str] = field(default_factory=list)
    removed_advisories: list[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not any(
            (self.added, self.moved, self.advisory_changed, self.reactivated,
             self.removed, self.new_advisories, self.removed_advisories)
        )


def clean_name(text: str) -> str:
    return _SPACES.sub(" ", text).strip()


def clean_class(text: str) -> str | None:
    """«5б» → «5B», «альфа 1» → «Alpha α1», «cdc» → «CDC»; нераспознанное → None."""
    s = clean_name(text)
    if not s:
        return None
    if s.casefold() in _CDC:
        return "CDC"
    if m := _ALPHA.match(s):
        return f"Alpha α{m[2]}" if m[2] else "Alpha"
    if m := _GRADE_CLASS.match(s):
        grade = int(m[1])
        letter = m[2].upper()
        letter = _CLASS_LETTERS.get(letter, letter)
        if 1 <= grade <= 12 and letter.isascii():
            return f"{grade}{letter}"
    return None


def class_grade(class_name: str) -> int | None:
    m = re.match(r"^(\d{1,2})[A-Z]$", class_name)
    return int(m[1]) if m else None


def advisory_kind(advisory: str) -> AdvisoryKind:
    if advisory == "CDC":
        return AdvisoryKind.CDC
    if advisory.startswith("Alpha"):
        return AdvisoryKind.ALPHA
    grade = class_grade(advisory)
    if grade is not None and grade <= 5:
        return AdvisoryKind.PRIMARY
    return AdvisoryKind.GROUP


def advisory_sort_key(name: str) -> tuple:
    """Порядок вкладок (Ф-12): 1A … 5B, затем остальные по алфавиту."""
    if advisory_kind(name) is AdvisoryKind.PRIMARY:
        return (0, class_grade(name), name)
    return (1, 0, name.casefold())


def _canonical_spelling(variants: Counter) -> str:
    # КОТИКИ = Котики: берём самое частое написание не капсом
    for name, _ in variants.most_common():
        if not name.isupper():
            return name
    return variants.most_common(1)[0][0].capitalize()


def parse_rows(raw_rows: Iterable[Sequence]) -> ParseResult:
    """Строки (ФИО, Класс, Эдвайзери) → очищенный список без повторов."""
    warnings: list[str] = []
    staged: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    group_variants: dict[str, Counter] = {}
    # 5B ← какие буквы были в файле: «Б» и «В» кириллицей обе становятся B
    letter_sources: dict[str, set[str]] = {}

    for line, raw in enumerate(raw_rows, start=2):  # строка 1 — заголовок
        cells = [("" if c is None else str(c)) for c in list(raw)[:3]]
        cells += [""] * (3 - len(cells))
        full_name = clean_name(cells[0])
        if not full_name:
            continue
        class_name = clean_class(cells[1])
        if class_name is None:
            warnings.append(f"Строка {line}: {full_name} — класс «{cells[1]}» не распознан, пропущено")
            continue
        key = (full_name, class_name)
        if key in seen:
            warnings.append(f"Строка {line}: {full_name} ({class_name}) — повтор, пропущено")
            continue
        seen.add(key)
        if (letter := class_letter_source(cells[1])) is not None:
            letter_sources.setdefault(class_name, set()).add(letter)

        grade = class_grade(class_name)
        if grade is None or grade <= 5:
            # 1–5 классы, Alpha и CDC: эдвайзери равна классу, что бы ни было в столбце
            advisory = class_name
        else:
            advisory = clean_name(cells[2])
            if not advisory:
                warnings.append(f"Строка {line}: {full_name} ({class_name}) — не указана эдвайзери, пропущено")
                continue
            group_variants.setdefault(normalize(advisory), Counter())[advisory] += 1
        staged.append((full_name, class_name, advisory))

    canonical = {key: _canonical_spelling(v) for key, v in group_variants.items()}
    rows = []
    for full_name, class_name, advisory in staged:
        if class_grade(class_name) and class_grade(class_name) > 5:
            advisory = canonical[normalize(advisory)]
        rows.append(StudentRow(full_name, class_name, advisory))

    errors = [
        f"Классы «{class_name[:-1]}Б» и «{class_name[:-1]}В» оба превратились бы в {class_name} "
        f"и слились в один. Исправьте букву класса в файле (латиницей: A, B, C …)"
        for class_name, letters in sorted(letter_sources.items())
        if {"Б", "В"} <= letters
    ]
    return ParseResult(rows, warnings, errors)


def read_xlsx(path: Path, sheet: str = SHEET_NAME) -> list[tuple]:
    from openpyxl import load_workbook

    wb = load_workbook(path, read_only=True, data_only=True)
    ws = wb[sheet] if sheet in wb.sheetnames else wb.worksheets[0]
    rows = list(ws.iter_rows(min_row=2, values_only=True))
    wb.close()
    return rows


def build_diff(
    rows: Sequence[StudentRow],
    existing: Sequence[ExistingStudent],
    existing_advisories: Iterable[str],
) -> ImportDiff:
    diff = ImportDiff()
    by_key = {(s.full_name, s.class_name): s for s in existing}
    matched: set[int] = set()
    unmatched_rows: list[StudentRow] = []

    for row in rows:
        old = by_key.get((row.full_name, row.class_name))
        if old is None:
            unmatched_rows.append(row)
            continue
        matched.add(old.id)
        if not old.active:
            diff.reactivated.append((old.id, row))
        elif old.advisory != row.advisory:
            diff.advisory_changed.append((old.id, row))

    leftovers = [s for s in existing if s.active and s.id not in matched]
    leftover_by_name = Counter(s.full_name for s in leftovers)
    row_by_name = Counter(r.full_name for r in unmatched_rows)
    for row in unmatched_rows:
        # Перевод в другой класс — только если имя однозначно с обеих сторон
        if leftover_by_name[row.full_name] == 1 and row_by_name[row.full_name] == 1:
            old = next(s for s in leftovers if s.full_name == row.full_name)
            diff.moved.append((old.id, row))
            matched.add(old.id)
        else:
            diff.added.append(row)
    diff.removed = [s for s in leftovers if s.id not in matched]

    old_names = set(existing_advisories)
    new_names = {r.advisory for r in rows}
    diff.new_advisories = sorted(new_names - old_names, key=advisory_sort_key)
    diff.removed_advisories = sorted(old_names - new_names, key=advisory_sort_key)
    return diff


def load_existing(session: Session) -> tuple[list[ExistingStudent], list[str]]:
    students = [
        ExistingStudent(s.id, s.full_name, s.class_name, s.advisory.name, s.active)
        for s in session.scalars(select(Student))
    ]
    advisories = [a.name for a in session.scalars(select(Advisory).where(Advisory.active))]
    return students, advisories


def apply_import(session: Session, rows: Sequence[StudentRow]) -> ImportDiff:
    """Привести БД к списку. Разрешения и выходы не трогаем: они привязаны к student_id (Ф-24)."""
    existing, advisory_names = load_existing(session)
    diff = build_diff(rows, existing, advisory_names)

    advisories = {a.name: a for a in session.scalars(select(Advisory))}
    needed = sorted({r.advisory for r in rows}, key=advisory_sort_key)
    for order, name in enumerate(needed):
        adv = advisories.get(name)
        if adv is None:
            adv = advisories[name] = Advisory(name=name, kind=advisory_kind(name))
            session.add(adv)
        adv.sort_order = order
        adv.active = True
    for name in diff.removed_advisories:
        advisories[name].active = False

    def update(student_id: int, row: StudentRow) -> None:
        s = session.get(Student, student_id)
        s.class_name = row.class_name
        s.advisory = advisories[row.advisory]
        s.active = True

    for student_id, row in diff.moved + diff.advisory_changed + diff.reactivated:
        update(student_id, row)
    for row in diff.added:
        session.add(
            Student(
                full_name=row.full_name,
                full_name_norm=normalize(row.full_name),
                class_name=row.class_name,
                advisory=advisories[row.advisory],
            )
        )
    for old in diff.removed:
        session.get(Student, old.id).active = False
    session.flush()
    return diff


def format_diff(diff: ImportDiff) -> str:
    if diff.is_empty:
        return "Изменений нет"
    lines = []

    def section(title: str, items: list[str]) -> None:
        if items:
            lines.append(f"{title}: {len(items)}")
            lines.extend(f"  {i}" for i in items)

    section("Новые", [f"{r.full_name} ({r.class_name}, {r.advisory})" for r in diff.added])
    section("Переведены", [f"{r.full_name} → {r.class_name}" for _, r in diff.moved])
    section("Сменили эдвайзери", [f"{r.full_name} → {r.advisory}" for _, r in diff.advisory_changed])
    section("Вернулись", [f"{r.full_name} ({r.class_name})" for _, r in diff.reactivated])
    section("Выбыли", [f"{s.full_name} ({s.class_name})" for s in diff.removed])
    section("Новые эдвайзери", diff.new_advisories)
    section("Исчезнувшие эдвайзери", diff.removed_advisories)
    return "\n".join(lines)


def main() -> None:
    from app.db import SessionLocal

    parser = argparse.ArgumentParser(description="Загрузить список учеников")
    parser.add_argument("xlsx", type=Path)
    parser.add_argument("--apply", action="store_true", help="применить изменения")
    args = parser.parse_args()

    parsed = parse_rows(read_xlsx(args.xlsx))
    for w in parsed.warnings:
        print("⚠️", w)
    if parsed.errors:
        for e in parsed.errors:
            print("❌", e)
        raise SystemExit("Список не загружен")
    print(f"Учеников в файле: {len(parsed.rows)}")

    with SessionLocal() as session:
        diff = apply_import(session, parsed.rows)
        print(format_diff(diff))
        if args.apply:
            session.commit()
            print("✅ Применено")
        else:
            session.rollback()
            print("Это предпросмотр. Чтобы применить, добавьте --apply")


if __name__ == "__main__":
    main()
