from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.schemas import ProductCreate
from core.models import Product


async def get_products(session: AsyncSession):  # Выдать список всех продуктов
    stmt = select(Product).order_by(Product.id)  # Команда для sql запроса
    result: Result = await session.execute(stmt)  # await - Пропускает другие программы пока это долго идет | .execute обращается к базу данных | Соединяем 2 части команды (БД и Команду sql)
    products = result.scalars().all()  # Собираем все данные
    return list(products)


async def get_product_by_id(session: AsyncSession, product_id: int):  # Выдать определенный продукт по id
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate):  # Создать новый продукт
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    # await session.refresh(product)
    return product
