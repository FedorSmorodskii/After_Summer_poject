from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from core.config import settings
from core.models import Base, db_helper  # Все что связано с SQL
from api_v1 import router as router_v1
from items_views import router as item_router
from users.views import router as users_router


@asynccontextmanager  # Все что нужно сделать перед запуском программы
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:  # Закроется после выполнения задачи | Запускаем "Движок"
        await conn.run_sync(Base.metadata.create_all)  # Пропускаем даленьнейшую программу к выполнению | Создаем таблицу SQL | create_all Не даст создать дубль таблицы

    yield  # Все что нужно сделать перед завершением работы программы


# Список наших приложений
app = FastAPI(lifespan=lifespan)  # Перед запуском основного приложения (main),
# он проверяет нет ли чего либо, что необходимо сделать перед запуском программы(lifespan)
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(item_router)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
