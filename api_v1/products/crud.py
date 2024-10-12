"""
Передаем команду SQL и возвращаем ответ
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.schemas import ProductCreate, ProductUpdate, ProductUpdatePartial
from core.models import Product

"""
select() - выбрать все | .order_by() - отсортировать по
.get() - выбрать определенный продукт
.add() - добавить в таблицу
.commit() - сохранить изменения
.refresh() - актуализировать данные в сессии
.delete() - удалить из таблицы
"""


async def get_products(session: AsyncSession):  # Выдать список всех продуктов
    stmt = select(Product).order_by(Product.id)  # Команда для sql запроса
    result: Result = await session.execute(
        stmt)  # await - Пропускает другие программы пока это долго идет | .execute обращается к базу данных | Соединяем 2 части команды (БД и Команду sql)
    products = result.scalars().all()  # Собираем все данные
    return list(products)


async def get_product_by_id(session: AsyncSession, product_id: int):  # Выдать определенный продукт по id
    return await session.get(Product, product_id)


async def get_product_by_id(session: AsyncSession, product_id: int):
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate):  # Создать новый продукт
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    # await session.refresh(product)
    return product


async def update_product(
        session: AsyncSession,
        product: Product,
        product_update: ProductUpdate | ProductUpdatePartial,
        partial: bool = False,
) -> Product:  # Обновить продукт по id
    for name, value in product_update.model_dump(exclude_unset=partial).items():  # Получаем словарь и идем по всем элементам
        setattr(product, name, value)
    await session.commit()
    return product

async def delete_product(
        session: AsyncSession,
        product: Product
) -> None:
    await session.delete(product)
    await session.commit()