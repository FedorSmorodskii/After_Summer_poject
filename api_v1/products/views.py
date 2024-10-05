from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.models import db_helper
from . import crud
from .schemas import Product, ProductCreate

router = APIRouter(tags=["Products"])


@router.get("/", response_model=list[Product])  # .get для получения инофрмации из БД | response_model для проверки типа
async def get_products(session: AsyncSession = Depends(db_helper.scoped_session_dependency),
                       ):
    return await crud.get_products(session=session)


@router.post("/", response_model=Product)  # .post для создания нового товара в БД | response_model для проверки типа
async def create_product(
        product_in: ProductCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get("/{product_id}/", response_model=Product)
async def get_product(product_id: int,
                      session: AsyncSession = Depends(db_helper.session_dependency)
                      ):
    product = await crud.get_product_by_id(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!",
    )
