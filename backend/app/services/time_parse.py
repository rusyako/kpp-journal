"""Разбор времени, которое пишет эдвайзер (Ф-13): 15:05, 15.05, 1505, 9:30."""

import re
from datetime import time

# «15:05», «15.05», «15,05», «15-05», «15 05», «9:30»
_SEPARATED = re.compile(r"^(\d{1,2})\s*[:.,\-\s]\s*(\d{2})$")
# «1505», «930»
_COMPACT = re.compile(r"^(\d{3,4})$")
# «15» — целый час
_HOUR = re.compile(r"^(\d{1,2})$")


def parse_time(text: str) -> time | None:
    """Время из строки или None, если не распознано.

    Пустую строку вызывающий код трактует как отмену разрешения, а не как ошибку.
    """
    s = text.strip()
    if m := _SEPARATED.match(s):
        hour, minute = int(m[1]), int(m[2])
    elif m := _COMPACT.match(s):
        hour, minute = int(m[1][:-2]), int(m[1][-2:])
    elif m := _HOUR.match(s):
        hour, minute = int(m[1]), 0
    else:
        return None
    if hour > 23 or minute > 59:
        return None
    return time(hour, minute)


def format_time(t: time) -> str:
    return t.strftime("%H:%M")
