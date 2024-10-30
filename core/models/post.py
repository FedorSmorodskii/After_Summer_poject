from typing import TYPE_CHECKING

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base  # Информация о названии таблицы и параметров id

if TYPE_CHECKING:
    from .user import User

# Ограничили длину заголовка до 100 символов | Заголовки могут повторяться
class Post(Base):
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    # Связь с таблицей Users
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    user: Mapped["User"] = relationship(back_populates="posts")  # Ссылаемся на User
