import uuid
from abc import ABC
from dataclasses import dataclass, field
from typing import Optional

from .abstract import CRUDRepositoryInterface
from domain import Product


@dataclass
class CreateProductDTO:
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    sku: str
    name: str
    description: str
    price: int
    category_id: uuid.UUID


@dataclass
class UpdateProductDTO:
    sku: Optional[str]
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    category_id: Optional[uuid.UUID]


class ProductRepositoryInterface(
    CRUDRepositoryInterface[
        Product,
        CreateProductDTO,
        UpdateProductDTO
    ],
    ABC,
):
    ...
