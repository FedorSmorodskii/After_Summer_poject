from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.parent  # Путь до базы данных

DB_PATH = BASE_DIR / "db.sqlite3"  # Путь к БД

class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"  # Путь по которому храниться БД
    echo: bool = False  # Типо для отладки


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"  # HTTP путь
    db: DbSettings = DbSettings()  # Настройки для БД


settings = Settings()
