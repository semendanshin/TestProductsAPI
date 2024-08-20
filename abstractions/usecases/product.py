import uuid
from abc import ABC

from abstractions.repositories.product import CreateProductDTO, UpdateProductDTO
from abstractions.usecases.abstract import CRUDUseCaseInterface
from domain import Product


class ProductUseCaseInterface(
    CRUDUseCaseInterface[
        Product, CreateProductDTO, UpdateProductDTO
    ],
    ABC,
):
    async def get_all(self, limit: int = 100, offset: int = 0, sku: str = None, name: str = None,
                      category_id: uuid.UUID = None) -> list[Product]:
        pass
