from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base  # Информация о названии таблицы и параметров id

if TYPE_CHECKING:
    from .post import Post


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)  # Ограничили макс имя до 32 символов | Каждое имя уникально

    posts = Mapped[list["Post"]] = relationship(back_populates="user")  # Ссылаемся на список постов
