"""Временный пароль от администратора и постоянный, который пользователь задаёт сам.

Новому пользователю (и после сброса) ставится общий временный пароль TEMP_PASSWORD.
С ним можно только войти и сразу придумать свой — до этого сервер ничего другого не отдаёт.
Временный пароль действует TEMP_PASSWORD_HOURS часов: он у всех одинаковый,
поэтому окно, когда чужой может войти под новым логином первым, должно быть коротким.
"""

from datetime import datetime, timedelta

from app import clock
from app.config import SCHOOL_TZ, TEMP_PASSWORD
from app.models import User
from app.services.auth import hash_password

TEMP_PASSWORD_HOURS = 72
MIN_LENGTH = 10
MAX_LENGTH = 128

# Пароли, которые подбирают первыми. Сравнение без учёта регистра.
_COMMON = {
    "qwerty123!", "qwerty1234", "qwerty12345", "qwertyuiop", "1234567890", "12345678910", "0123456789",
    "password1!", "password123", "password12", "passw0rd!!", "1q2w3e4r5t", "1qaz2wsx3edc", "qazwsxedc1",
    "aaaaaaaaaa", "1111111111", "abc1234567", "iloveyou12", "admin12345", "administrator", "kpp1234567",
    "parol12345", "йцукен1234", "пароль1234",
}


class PasswordError(Exception):
    pass


def issue_temp_password(user: User) -> tuple[str, datetime]:
    """Поставить временный пароль. Все сеансы пользователя завершаются."""
    password = TEMP_PASSWORD
    expires = clock.now() + timedelta(hours=TEMP_PASSWORD_HOURS)
    user.password_hash = hash_password(password)
    user.must_change_password = True
    user.temp_password_expires_at = expires
    user.revoke_sessions()
    return password, expires


def temp_password_expired(user: User) -> bool:
    expires = user.temp_password_expires_at
    if not user.must_change_password or expires is None:
        return False
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=SCHOOL_TZ)
    return expires < clock.now()


def check_new_password(user: User, new: str, current: str) -> None:
    """Требования к постоянному паролю. Ошибка — текстом для пользователя."""
    if len(new) < MIN_LENGTH:
        raise PasswordError(f"Пароль должен быть не короче {MIN_LENGTH} символов")
    if len(new) > MAX_LENGTH:
        raise PasswordError(f"Пароль должен быть не длиннее {MAX_LENGTH} символов")
    if new == current or new.lower() == TEMP_PASSWORD.lower():
        raise PasswordError("Новый пароль должен отличаться от временного")
    if user.username and user.username.lower() in new.lower():
        raise PasswordError("Пароль не должен содержать логин")
    if new.lower() in _COMMON or len(set(new)) < 4:
        raise PasswordError("Этот пароль слишком простой — его подберут первым. Придумайте другой")


def set_own_password(user: User, new: str) -> None:
    user.password_hash = hash_password(new)
    user.must_change_password = False
    user.temp_password_expires_at = None
    user.revoke_sessions()  # старый пароль мог знать кто-то ещё
