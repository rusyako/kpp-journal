"""Поиск ученика на КПП (Ф-4 … Ф-7).

На экране КПП тот же алгоритм работает в браузере (frontend/src/lib/search.ts),
здесь — эталон для тестов и для поиска на сервере.
"""

from dataclasses import dataclass
from typing import Sequence

from app.config import SEARCH_LIMIT
from app.services.normalize import words

MIN_QUERY_LETTERS = 2

HINT_TOO_SHORT = "Введите хотя бы 2 буквы"
HINT_NOT_FOUND = "Никого не найдено"
HINT_MORE_LETTERS = "Найдено больше {limit} — введите больше букв"


@dataclass(frozen=True)
class Candidate:
    id: int
    full_name: str
    exited: bool = False


@dataclass(frozen=True)
class SearchResult:
    items: list[Candidate]
    total: int
    hint: str | None


def _prefix_match(query: list[str], name: list[str]) -> bool:
    return all(any(w.startswith(q) for w in name) for q in query)


def _substring_match(query: list[str], name: list[str]) -> bool:
    return all(any(q in w for w in name) for q in query)


def _sort_key(c: Candidate) -> tuple:
    # Сначала не вышедшие, потом фамилия (первое слово), потом имя
    name = words(c.full_name)
    return (c.exited, name[:1], name[1:2], name[2:])


def search(query: str, students: Sequence[Candidate], limit: int = SEARCH_LIMIT) -> SearchResult:
    q = words(query)
    if sum(len(w) for w in q) < MIN_QUERY_LETTERS:
        return SearchResult([], 0, HINT_TOO_SHORT)

    indexed = [(s, words(s.full_name)) for s in students]
    found = [s for s, name in indexed if _prefix_match(q, name)]
    if not found:
        # По началу слов ничего — ищем по части слова (Ф-5)
        found = [s for s, name in indexed if _substring_match(q, name)]

    found.sort(key=_sort_key)
    if not found:
        hint = HINT_NOT_FOUND
    elif len(found) > limit:
        hint = HINT_MORE_LETTERS.format(limit=limit)
    else:
        hint = None
    return SearchResult(found[:limit], len(found), hint)
