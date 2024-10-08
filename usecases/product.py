import uuid

from abstractions.repositories.product import UpdateProductDTO, CreateProductDTO
from abstractions.usecases.product import ProductUseCaseInterface
from domain import Product
from usecases.abstract import AbstractCRUDUseCase


class ProductUseCase(
    AbstractCRUDUseCase[
        Product, CreateProductDTO, UpdateProductDTO
    ],
    ProductUseCaseInterface,
):
    async def get_all(self, limit: int = 100, offset: int = 0, sku: str = None, name: str = None, category_id: uuid.UUID = None) -> list[Product]:
        filters = {}
        if sku is not None:
            filters["sku"] = sku
        if name is not None:
            filters["name"] = name
        if category_id is not None:
            filters["category_id"] = category_id
        return await self.repository.get_all(limit, offset, **filters)
