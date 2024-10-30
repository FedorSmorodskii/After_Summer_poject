# Добавляем сюда, что бы BaseMetaData знал
__all__ = (
    "Base",
    "DatabaseHelper",
    "db_helper",
    "Product",
    "User",
    "Post",
    # Add more models here..."
)

from .base import Base
from .db_helper import DatabaseHelper, db_helper
from .product import Product
from .user import User
from .post import Post
