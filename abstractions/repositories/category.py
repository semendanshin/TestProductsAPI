import uuid
from abc import ABC
from dataclasses import dataclass, field

from .abstract import CRUDRepositoryInterface
from domain import Category


@dataclass
class CreateCategoryDTO:
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    name: str

@dataclass
class UpdateCategoryDTO:
    name: str


class CategoryRepositoryInterface(
    CRUDRepositoryInterface[
        Category,
        CreateCategoryDTO,
        UpdateCategoryDTO
    ],
    ABC,
):
    ...
