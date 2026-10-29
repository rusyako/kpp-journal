"""Нормализация ФИО для поиска (Ф-6).

Регистр, ё/е, апострофы и казахские буквы не важны: «Актилек» находит «Ақтілекқызы».
Та же функция должна быть повторена во frontend/src/lib/normalize.ts —
общие примеры лежат в shared/search_cases.json.
"""

import re

_LETTERS = str.maketrans(
    {
        "ә": "а",
        "ғ": "г",
        "қ": "к",
        "ң": "н",
        "ө": "о",
        "ұ": "у",
        "ү": "у",
        "һ": "х",
        "і": "и",
        "ё": "е",
    }
)

# Апострофы и кавычки удаляются, а не заменяются пробелом: «Ғали'ев» → «галиев»
_APOSTROPHES = re.compile(r"[’'`ʼ‘\"«»]")
# Всё, что не буква и не цифра (дефис, точка, пробелы), разделяет слова
_SEPARATORS = re.compile(r"[^\w]+|_")


def normalize(text: str) -> str:
    """Строка в нижнем регистре без казахских букв, слова через один пробел."""
    text = text.lower().translate(_LETTERS)
    text = _APOSTROPHES.sub("", text)
    return _SEPARATORS.sub(" ", text).strip()


def words(text: str) -> list[str]:
    return normalize(text).split()
