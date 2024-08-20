from abstractions.repositories import ProductRepositoryInterface
from abstractions.repositories.product import UpdateProductDTO, CreateProductDTO
from domain import Product as ProductModel
from infrastructure.repositories.sqlalchemy import AbstractSQLAlchemyRepository

from infrastructure.repositories.sqlalchemy.entities import Product


class SqlAlchemyProductRepository(
    AbstractSQLAlchemyRepository[
        Product, ProductModel, CreateProductDTO, UpdateProductDTO
    ],
    ProductRepositoryInterface,
):
    def entity_to_model(self, entity: Product) -> ProductModel:
        return ProductModel(
            id=entity.id,
            sku=entity.sku,
            name=entity.name,
            price=entity.price,
            description=entity.description,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def model_to_entity(self, model: ProductModel) -> Product:
        return Product(
            id=model.id,
            sku=model.sku,
            name=model.name,
            price=model.price,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def create_dto_to_entity(self, create_dto: CreateProductDTO) -> Product:
        return Product(
            id=create_dto.id,
            sku=create_dto.sku,
            name=create_dto.name,
            price=create_dto.price,
            description=create_dto.description,
        )

    def update_dto_to_entity(self, update_dto: UpdateProductDTO) -> Product:
        return Product(
            sku=update_dto.sku,
            name=update_dto.name,
            price=update_dto.price,
            description=update_dto.description,
        )
