# Этот блок нужен для создания сессии и создания SQL таблцы. Знчния передаем из settings
# Это необходимо для запуска "движка"

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from core.config import settings


class DatabaseHelper:  # Управление ассинхронностью базы данных
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(  # Обязательные переменные для функции ниже
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(  # Создает условия для работы ассинхронности
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db_helper = DatabaseHelper(url=settings.db_url, echo=settings.db_echo)  # Передаем из настроек путь и разрешение отладки
