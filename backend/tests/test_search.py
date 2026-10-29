import json
from pathlib import Path

import pytest

from app.services.normalize import normalize
from app.services.search import Candidate, search

CASES_FILE = Path(__file__).resolve().parents[2] / "shared" / "search_cases.json"
DATA = json.loads(CASES_FILE.read_text(encoding="utf-8"))
STUDENTS = [Candidate(**s) for s in DATA["students"]]


@pytest.mark.parametrize("case", DATA["cases"], ids=lambda c: c["query"])
def test_shared_cases(case):
    result = search(case["query"], STUDENTS)
    assert [c.full_name for c in result.items] == case["names"]
    assert result.total == case["total"]
    assert result.hint == case["hint"]


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Ақтілекқызы", "актилеккызы"),
        ("ӘҒҚҢӨҰҮҺІ", "агкноуухи"),
        ("Гилёва", "гилева"),
        ("Ма'руфов  Азиз", "маруфов азиз"),
        ("Абу-Бакир", "абу бакир"),
        ("  КИМ   илья ", "ким илья"),
    ],
)
def test_normalize(raw, expected):
    assert normalize(raw) == expected


def test_kazakh_query_finds_plain_spelling():
    # Охрана может набрать казахскую букву, а в списке — русская, и наоборот
    result = search("Ақтіл", STUDENTS)
    assert result.total == 4


def test_exited_go_after_not_exited():
    students = [Candidate(1, "Абаев Ален", exited=True), Candidate(2, "Абаев Тимур")]
    assert [c.id for c in search("абаев", students).items] == [2, 1]
