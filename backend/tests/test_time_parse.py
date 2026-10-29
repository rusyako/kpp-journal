from datetime import time

import pytest

from app.services.time_parse import format_time, parse_time


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("15:05", time(15, 5)),
        ("15.05", time(15, 5)),
        ("1505", time(15, 5)),
        ("9:30", time(9, 30)),
        ("930", time(9, 30)),
        ("09:30", time(9, 30)),
        (" 15 05 ", time(15, 5)),
        ("15,05", time(15, 5)),
        ("15", time(15, 0)),
        ("0:00", time(0, 0)),
    ],
)
def test_recognized(raw, expected):
    assert parse_time(raw) == expected


@pytest.mark.parametrize("raw", ["абв", "", "25:00", "15:60", "15:5", "12345", "15:05:00", "после обеда"])
def test_not_recognized(raw):
    assert parse_time(raw) is None


def test_format():
    assert format_time(time(9, 5)) == "09:05"
