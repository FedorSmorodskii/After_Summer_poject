from sqlalchemy.orm import Mapped

from .base import Base  # Информация о названии таблицы и параметров id


class Product(Base):
    __tablename__ = 'products'

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
