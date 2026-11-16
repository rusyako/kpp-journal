"""Временные пароли: пользователь сам задаёт постоянный пароль при первом входе

Всем пользователям с логином ставится временный пароль (TEMP_PASSWORD, по умолчанию Qwerty123!)
сроком на 72 часа. Старые пароли, в том числе демо-пароли из README, больше не действуют.
При первом входе каждый придумывает свой пароль.

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-13 12:00:00
"""
from datetime import datetime, timedelta, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.config import TEMP_PASSWORD
from app.services.auth import hash_password

revision: str = '0003'
down_revision: Union[str, None] = '0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TEMP_PASSWORD_HOURS = 72


def upgrade() -> None:
    with op.batch_alter_table('users') as batch:
        batch.add_column(sa.Column('must_change_password', sa.Boolean(), nullable=False, server_default=sa.false()))
        batch.add_column(sa.Column('temp_password_expires_at', sa.DateTime(timezone=True), nullable=True))

    conn = op.get_bind()
    users = sa.table(
        'users',
        sa.column('id', sa.Integer()),
        sa.column('username', sa.String()),
        sa.column('password_hash', sa.String()),
        sa.column('session_version', sa.Integer()),
        sa.column('must_change_password', sa.Boolean()),
        sa.column('temp_password_expires_at', sa.DateTime(timezone=True)),
    )
    expires = datetime.now(timezone.utc) + timedelta(hours=TEMP_PASSWORD_HOURS)
    for uid, version in conn.execute(sa.select(users.c.id, users.c.session_version).where(users.c.username.is_not(None))):
        conn.execute(
            users.update()
            .where(users.c.id == uid)
            .values(
                password_hash=hash_password(TEMP_PASSWORD),  # у каждого своя соль
                must_change_password=True,
                temp_password_expires_at=expires,
                session_version=(version or 0) + 1,  # вошедшие по старым паролям выходят
            )
        )


def downgrade() -> None:
    with op.batch_alter_table('users') as batch:
        batch.drop_column('temp_password_expires_at')
        batch.drop_column('must_change_password')
