from typing import List

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from auth.core.models.base import Base
from auth.core.models.mixins import (
    CreatedTimestampMixin,
    IntIdPkMixin,
    UpdatedTimestampMixin,
)

role_rights_association = Table(
    "role_rights_association",
    Base.metadata,
    Column(
        "role_id",
        Integer,
        ForeignKey("roles.role_id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "right_id",
        Integer,
        ForeignKey("role_rights.role_right_id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base, IntIdPkMixin, CreatedTimestampMixin, UpdatedTimestampMixin):
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hash_password: Mapped[bytes] = mapped_column(nullable=False)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.role_id", ondelete="SET DEFAULT"),
        nullable=False,
        default=1,
    )

    role: Mapped["Role"] = relationship(back_populates="users")


class Role(Base):
    role_id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[str] = mapped_column(unique=True, nullable=False)

    users: Mapped[List["User"]] = relationship(
        back_populates="role", cascade="all, delete"
    )

    rights: Mapped[List["RoleRight"]] = relationship(
        secondary=role_rights_association, back_populates="roles"
    )


class RoleRight(Base):
    role_right_id: Mapped[int] = mapped_column(primary_key=True)
    right: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)

    roles: Mapped[List["Role"]] = relationship(
        secondary=role_rights_association, back_populates="rights"
    )
