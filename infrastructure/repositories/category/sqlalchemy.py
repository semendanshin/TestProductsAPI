from abstractions.repositories.category import UpdateCategoryDTO, CreateCategoryDTO, CategoryRepositoryInterface
from domain import Category as CategoryModel
from infrastructure.repositories.sqlalchemy import AbstractSQLAlchemyRepository
from infrastructure.repositories.sqlalchemy.entities import Category


class SqlAlchemyCategoryRepository(
    AbstractSQLAlchemyRepository[
        Category, CategoryModel, CreateCategoryDTO, UpdateCategoryDTO
    ],
    CategoryRepositoryInterface,
):
    def entity_to_model(self, entity: Category) -> CategoryModel:
        return CategoryModel(
            id=entity.id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def model_to_entity(self, model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def create_dto_to_entity(self, create_dto: CreateCategoryDTO) -> Category:
        return Category(
            id=create_dto.id,
            name=create_dto.name,
        )

    def update_dto_to_entity(self, update_dto: UpdateCategoryDTO) -> Category:
        return Category(
            name=update_dto.name,
        )
