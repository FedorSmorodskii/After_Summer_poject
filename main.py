from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from core.models import Base, db_helper
from items_views import router as item_router
from users.views import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)
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
