# Этот блок нужен для создания сессии и создания SQL таблцы. Знчния передаем из settings
# Это необходимо для запуска "движка"
# Здесь описано подключение к базу данных
from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
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

    def get_scoped_session(self):  # Вспомогательная функция для подключения к БД
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self):  # Открываем сессию для подключения к БД, закрывая ее после использования
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self):  # Открываем сессию для подключения к БД, закрывая ее после использования
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DatabaseHelper(url=settings.db_url, echo=settings.db_echo)  # Передаем из настроек путь и разрешение отладки
