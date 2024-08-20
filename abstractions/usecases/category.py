from abc import ABC

from abstractions.repositories.category import CreateCategoryDTO, UpdateCategoryDTO
from abstractions.usecases.abstract import CRUDUseCaseInterface
from domain import Category


class CategoryUseCaseInterface(
    CRUDUseCaseInterface[
        Category, CreateCategoryDTO, UpdateCategoryDTO
    ],
    ABC,
):
    pass
