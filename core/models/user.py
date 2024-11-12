"""
К User привязаны Post и Profile
User имеет много постов и один профиль
User - главный класс для работы с пользователями
"""

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base  # Информация о названии таблицы и параметров id

if TYPE_CHECKING: # Создает import для проверки типов данных через Mapped | Используем для избежания параллельного импорта
    from .post import Post
    from .profile import Profile

class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)  # Ограничили макс имя до 32 символов | Каждое имя уникально

    """
    Связываем User с Post и Profile 
    """

    posts : Mapped[list["Post"]] = relationship(back_populates="user")  # Это означает, что один пользователь может иметь много постов
    profile : Mapped["Profile"] = relationship(back_populates="user")  # Это означает, что у каждого пользователя есть один профиль.
