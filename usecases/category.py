from abstractions.repositories.category import CreateCategoryDTO, UpdateCategoryDTO
from abstractions.usecases import CategoryUseCaseInterface
from domain import Category
from usecases.abstract import AbstractCRUDUseCase


class CategoryUseCase(
    AbstractCRUDUseCase[
        Category, CreateCategoryDTO, UpdateCategoryDTO
    ],
    CategoryUseCaseInterface,
):
    pass
