# Настройки Профиля каждого пользователя (Имя, Фамилия, Биография, ID)

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base  # Информация о названии таблицы и параметров id
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .user import User


class Profile(UserRelationMixin, Base):
    _user_id_unique = True  # Уникальный ID пользователя
    _user_id_nullable = 'profile'

    first_name: Mapped[str | None] = mapped_column(String(40))  # Ограничили макс имя до 40 символов | Каждое имя уникально
    last_name: Mapped[str | None] = mapped_column(String(40))  # Ограничили макс фамилию до 40 символов | Каждое имя уникально
    bio: Mapped[str | None]  # Биография
