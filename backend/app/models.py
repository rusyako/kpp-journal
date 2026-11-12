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
