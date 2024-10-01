# Этот блок нужен для создания "Неочевидных" настроек SQL таблицы. Таких как назвазвание, столбец id и тп
# Используется при создании любой таблицы, т к все от него наследуются
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):  # Базовый от которого все наследуются
    __abstract__ = True

    @declared_attr  # Создаем имя для таблицы
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)  # Определение столбца id в SQL таблице
