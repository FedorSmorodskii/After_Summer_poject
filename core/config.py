from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent  # Путь до базы данных


class Settings(BaseSettings):
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"  # Путь по которому храниться БД
    db_echo: bool = True  # Типо для отладки


settings = Settings()
