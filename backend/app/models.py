"""Модель данных. «Лист дня» — это не копия листа, а выборка по дате."""

import enum
from datetime import date, datetime, time

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    String,
    Text,
    Time,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app import clock


class Base(DeclarativeBase):
    # Имена ограничений нужны миграциям, чтобы их можно было потом менять и удалять
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class AdvisoryKind(enum.StrEnum):
    PRIMARY = "primary"  # 1A … 5B: эдвайзери равна классу
    ALPHA = "alpha"
    CDC = "cdc"
    GROUP = "group"  # 6–12 классы: именованная группа


class Role(enum.StrEnum):
    ADMIN = "admin"
    GUARD = "guard"
    ADVISOR = "advisor"
    VIEWER = "viewer"


class Advisory(Base):
    __tablename__ = "advisories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    kind: Mapped[AdvisoryKind] = mapped_column(Enum(AdvisoryKind, native_enum=False))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    students: Mapped[list["Student"]] = relationship(back_populates="advisory")


class Student(Base):
    __tablename__ = "students"
    # Ученик определяется парой «ФИО + класс» (раздел 4)
    __table_args__ = (UniqueConstraint("full_name", "class_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(200))
    full_name_norm: Mapped[str] = mapped_column(String(200), index=True)
    class_name: Mapped[str] = mapped_column(String(20))
    advisory_id: Mapped[int] = mapped_column(ForeignKey("advisories.id"))
    # Выбывших не удаляем, чтобы история выходов осталась целой
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    advisory: Mapped[Advisory] = relationship(back_populates="students")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=False))
    display_name: Mapped[str] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(200), unique=True)
    # Вход по логину и паролю (охрана, админ; эдвайзер — запасной вход без Telegram)
    username: Mapped[str | None] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(300))
    telegram_id: Mapped[int | None] = mapped_column(BigInteger, unique=True)
    # Получает отчёт за день в Telegram (руководство)
    receives_report: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    # Номер в cookie сессии. Увеличение номера (смена пароля, «завершить сеансы») выкидывает все входы
    session_version: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    def revoke_sessions(self) -> None:
        self.session_version = (self.session_version or 0) + 1

    advisories: Mapped[list[Advisory]] = relationship(secondary="user_advisories")


class Invite(Base):
    """Одноразовый код для привязки Telegram: t.me/<бот>?start=<code>."""

    __tablename__ = "invites"

    code: Mapped[str] = mapped_column(String(64), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class UserAdvisory(Base):
    """Эдвайзер правит только свои группы — закрывает риск «чужая вкладка»."""

    __tablename__ = "user_advisories"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    advisory_id: Mapped[int] = mapped_column(ForeignKey("advisories.id"), primary_key=True)


class SchoolDay(Base):
    """Исключения из календаря пн–сб: каникулы, праздники, перенесённые дни."""

    __tablename__ = "school_days"

    date: Mapped[date] = mapped_column(Date, primary_key=True)
    is_working: Mapped[bool] = mapped_column(Boolean)
    note: Mapped[str | None] = mapped_column(String(200))


class Permission(Base):
    """Разовое разрешение эдвайзера на выход в этот день (Ф-13)."""

    __tablename__ = "permissions"
    __table_args__ = (UniqueConstraint("date", "student_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    allowed_time: Mapped[time | None] = mapped_column(Time)
    # Что эдвайзер ввёл как есть — нужно для статуса «⚠️ время не распознано»
    raw_time: Mapped[str] = mapped_column(String(50), default="")
    reason: Mapped[str] = mapped_column(Text, default="")
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: clock.now(), onupdate=lambda: clock.now()
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    student: Mapped[Student] = relationship()


class Exit(Base):
    """Отметка «Вышел» на КПП. Ошибочная отметка не удаляется, а отменяется (Ф-10)."""

    __tablename__ = "exits"
    # Одна действующая отметка на ученика в день, даже если два охранника нажали одновременно
    __table_args__ = (
        Index(
            "uq_exits_active",
            "date",
            "student_id",
            unique=True,
            postgresql_where=text("cancelled_at IS NULL"),
            sqlite_where=text("cancelled_at IS NULL"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    exit_time: Mapped[time] = mapped_column(Time)
    guard_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    # Отметка сделана без связи и отправлена позже (PWA-очередь на КПП)
    offline: Mapped[bool] = mapped_column(Boolean, default=False)
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    student: Mapped[Student] = relationship()


class AuditLog(Base):
    """Журнал действий (Ф-21)."""

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: clock.now(), index=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(50))
    student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id"))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)


# ---------------------------------------------------------------------------
# Hikvision: пилот предварительной авторизации выхода (docs/hikvision/MVP_IMPLEMENTATION.md)
#
# Терминал только опознаёт человека (employeeNo), решение о выходе принимает kpp-journal.
# Решение (release_decisions), ответ устройству (hik_commands) и фактический проход
# (hik_passages) — разные записи: ALLOW ещё не значит, что турникет открылся и человек прошёл.
# ---------------------------------------------------------------------------


class HikDirection(enum.StrEnum):
    EXIT = "exit"
    ENTRY = "entry"


class HikDevice(Base):
    """Терминал. Пароль в БД не храним: credentials_env — префикс переменных HIK_<X>_USER / HIK_<X>_PASSWORD."""

    __tablename__ = "hik_devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Часть URL приёмника: /hikvision/listen/<key>
    key: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    host: Mapped[str] = mapped_column(String(100), default="")
    port: Mapped[int] = mapped_column(Integer, default=80)
    scheme: Mapped[str] = mapped_column(String(5), default="http")
    # Направление задаётся конфигурацией: в событии Hikvision его нет (EVENTS.md §5)
    direction: Mapped[HikDirection] = mapped_column(Enum(HikDirection, native_enum=False))
    door_no: Mapped[int] = mapped_column(Integer, default=1)
    # Виртуальный терминал симулятора: в сеть не ходит, запросы принимает только изнутри приложения
    simulated: Mapped[bool] = mapped_column(Boolean, default=False)
    # sync — решение в теле ответа на POST устройства; async — отдельным PUT /ISAPI/AccessControl/remoteCheck
    response_mode: Mapped[str] = mapped_column(String(10), default="sync")
    # С каких адресов принимать события. Пусто у реального терминала = не доверять никому
    allowed_ips: Mapped[list] = mapped_column(JSON, default=list)
    credentials_env: Mapped[str | None] = mapped_column(String(50))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    model: Mapped[str | None] = mapped_column(String(100))
    firmware: Mapped[str | None] = mapped_column(String(100))
    serial_number: Mapped[str | None] = mapped_column(String(100))
    last_event_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_health_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_health_ok: Mapped[bool | None] = mapped_column(Boolean)
    last_error: Mapped[str | None] = mapped_column(String(300))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: clock.now())


class HikPerson(Base):
    """Связь employeeNo терминала с профилем kpp-journal. employeeNo — всегда строка."""

    __tablename__ = "hik_persons"

    id: Mapped[int] = mapped_column(primary_key=True)
    employee_no: Mapped[str] = mapped_column(String(32), unique=True)
    # Подпись для экрана пилота; ФИО учеников из терминала сюда не копируем
    label: Mapped[str] = mapped_column(String(200))
    kind: Mapped[str] = mapped_column(String(20), default="test")  # test | student | staff
    student_id: Mapped[int | None] = mapped_column(ForeignKey("students.id"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    # Участвует в пилоте. Дополнительно сверяется со списком HIKVISION_PILOT_EMPLOYEE_NOS
    pilot: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: clock.now())
    # userType, прочитанный с терминала (UserInfo/Search) — только после проверенного чтения
    terminal_user_type: Mapped[str | None] = mapped_column(String(20))
    terminal_checked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    terminal_device_key: Mapped[str | None] = mapped_column(String(50))

    student: Mapped[Student | None] = relationship()
    user: Mapped[User | None] = relationship()


class ReleasePermission(Base):
    """Разрешение на автоматический выход через турникет.

    source="pilot" — тестовое разрешение пилота. Это НЕ согласие родителей; для него позже появится свой source.
    """

    __tablename__ = "release_permissions"
    __table_args__ = (Index("ix_release_permissions_person_window", "person_id", "valid_from", "valid_until"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    person_id: Mapped[int] = mapped_column(ForeignKey("hik_persons.id"))
    source: Mapped[str] = mapped_column(String(20), default="pilot")
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    single_use: Mapped[bool] = mapped_column(Boolean, default=True)
    note: Mapped[str] = mapped_column(Text, default="")
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: clock.now())
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Без внешнего ключа, чтобы не было цикла permission ↔ decision
    used_by_decision_id: Mapped[int | None] = mapped_column(Integer)

    person: Mapped[HikPerson] = relationship()


class HikEvent(Base):
    """Событие терминала без фото и ФИО. dedup_key уникален; у повтора он пустой, а duplicate_of_id указывает оригинал."""

    __tablename__ = "hik_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("hik_devices.id"), index=True)
    device_key: Mapped[str] = mapped_column(String(50))
    source_ip: Mapped[str] = mapped_column(String(64), default="")
    dedup_key: Mapped[str | None] = mapped_column(String(200), unique=True)
    duplicate_of_id: Mapped[int | None] = mapped_column(ForeignKey("hik_events.id"))
    serial_no: Mapped[int | None] = mapped_column(Integer)
    front_serial_no: Mapped[int | None] = mapped_column(Integer)
    event_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    event_time_raw: Mapped[str] = mapped_column(String(40), default="")
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: clock.now(), index=True)
    event_type: Mapped[str] = mapped_column(String(50), default="")
    major: Mapped[int | None] = mapped_column(Integer)
    minor: Mapped[int | None] = mapped_column(Integer)
    employee_no: Mapped[str | None] = mapped_column(String(32), index=True)
    user_type: Mapped[str | None] = mapped_column(String(20))
    remote_check: Mapped[bool] = mapped_column(Boolean, default=False)
    current_event: Mapped[bool | None] = mapped_column(Boolean)
    # remote_check | passage | passage_timeout | reverse_passage | door | auth_ok | auth_failed | remote_check_result | other
    category: Mapped[str] = mapped_column(String(30), default="other")
    simulated: Mapped[bool] = mapped_column(Boolean, default=False)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)


class ReleaseDecision(Base):
    """Решение kpp-journal по одному запросу удалённой проверки. Одно событие — одно решение."""

    __tablename__ = "release_decisions"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("hik_events.id"), unique=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("hik_devices.id"))
    person_id: Mapped[int | None] = mapped_column(ForeignKey("hik_persons.id"))
    permission_id: Mapped[int | None] = mapped_column(ForeignKey("release_permissions.id"))
    employee_no: Mapped[str | None] = mapped_column(String(32))
    direction: Mapped[str] = mapped_column(String(10), default="")
    result: Mapped[str] = mapped_column(String(5))  # ALLOW | DENY
    reason: Mapped[str] = mapped_column(String(40))
    detail: Mapped[str] = mapped_column(String(300), default="")
    mode: Mapped[str] = mapped_column(String(20))
    decided_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: clock.now(), index=True)
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)


class HikCommand(Base):
    """Что ушло на терминал (или было заблокировано режимом) и чем закончилось."""

    __tablename__ = "hik_commands"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int | None] = mapped_column(ForeignKey("hik_devices.id"))
    decision_id: Mapped[int | None] = mapped_column(ForeignKey("release_decisions.id"), index=True)
    event_id: Mapped[int | None] = mapped_column(ForeignKey("hik_events.id"))
    # remote_check_sync_response | remote_check_put | isapi_read | parse_error
    kind: Mapped[str] = mapped_column(String(40))
    method: Mapped[str] = mapped_column(String(6), default="")
    path: Mapped[str] = mapped_column(String(200), default="")
    check_result: Mapped[str | None] = mapped_column(String(10))  # success | failed
    # sent | simulated | blocked | error | timeout
    status: Mapped[str] = mapped_column(String(20))
    http_status: Mapped[int | None] = mapped_column(Integer)
    error: Mapped[str | None] = mapped_column(String(300))
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: clock.now(), index=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    payload: Mapped[dict] = mapped_column(JSON, default=dict)


class HikPassage(Base):
    """Фактический результат после ALLOW: прошёл / не прошёл. Хранится отдельно от решения."""

    __tablename__ = "hik_passages"

    id: Mapped[int] = mapped_column(primary_key=True)
    decision_id: Mapped[int] = mapped_column(ForeignKey("release_decisions.id"), unique=True)
    event_id: Mapped[int | None] = mapped_column(ForeignKey("hik_events.id"), unique=True)
    person_id: Mapped[int | None] = mapped_column(ForeignKey("hik_persons.id"))
    device_id: Mapped[int | None] = mapped_column(ForeignKey("hik_devices.id"))
    # passed | timed_out | reverse | not_passed
    outcome: Mapped[str] = mapped_column(String(20))
    source: Mapped[str] = mapped_column(String(20))  # device_event | manual
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: clock.now())
    confirmed_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    exit_id: Mapped[int | None] = mapped_column(ForeignKey("exits.id"))


class HikPilotState(Base):
    """Выключатель пилота (одна строка, id=1). По умолчанию выключен: все запросы — DENY."""

    __tablename__ = "hik_pilot_state"

    id: Mapped[int] = mapped_column(primary_key=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))


class HikConfigSnapshot(Base):
    """Снимок настроек терминала «до» (read-only GET) — основа для отката. Пароли вырезаны."""

    __tablename__ = "hik_config_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(ForeignKey("hik_devices.id"), index=True)
    taken_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: clock.now())
    # acs_cfg | acs_cfg_caps | http_hosts | user_before | user_after | user_type_change | …
    kind: Mapped[str] = mapped_column(String(30), default="")
    path: Mapped[str] = mapped_column(String(200))
    http_status: Mapped[int | None] = mapped_column(Integer)
    content: Mapped[dict] = mapped_column(JSON, default=dict)
