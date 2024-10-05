from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):  # Класс по которому строятся другие классы и проверяется каждый товар
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):  # Класс с которым сравнивается товар при создании (нужен, т к могут быть доп условия при создании)
    pass


class Product(ProductBase):  # Вспомогательный класс для продуктов
    model_config = ConfigDict(from_attributes=True)

    id: int
