from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base
from src.core.models.mixins import (
    CreatedTimestampMixin,
    IntIdPkMixin,
    UpdatedTimestampMixin,
)


class User(Base, IntIdPkMixin, CreatedTimestampMixin, UpdatedTimestampMixin):

    email: Mapped[str] = mapped_column(unique=True, index=True)
    nickname: Mapped[str] = mapped_column(nullable=False, index=True, unique=True)
    hash_password: Mapped[bytes] = mapped_column(nullable=False)
