# Этот блок нужен для создания "Неочевидных" настроек SQL таблицы. Таких как назвазвание, столбец id и тп
# Используется при создании любой таблицы, т к все от него наследуются
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):  # Базовый от которого все наследуются
    __abstract__ = True  #  Данный класс не должен быть напрямую отображен в таблицу базы данных. Вместо этого он должен использоваться как базовый класс для других классов.

    @declared_attr  # Создаем имя для таблицы
    def __tablename__(cls) -> str: # Определяет как будет генерироваться имя таблицы
        return f"{cls.__name__.lower()}s" #  Берет имя класса и сокращает его до суффикса "s"

    id: Mapped[int] = mapped_column(primary_key=True)  # Определение столбца id в SQL таблице
