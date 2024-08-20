import logging
import traceback
import uuid
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Param, Depends
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from abstractions.repositories.abstract import NotFoundException
from abstractions.repositories.product import CreateProductDTO, UpdateProductDTO
from abstractions.usecases import ProductUseCaseInterface
from domain import Product

logger = logging.getLogger(__name__)


class HandlerCreateProductDTO(BaseModel):
    sku: str
    name: str
    description: str
    price: float
    category_id: uuid.UUID


class HandlerUpdateProductDTO(BaseModel):
    sku: str
    name: str
    description: str
    price: float
    category_id: uuid.UUID


class FastApiProductHandler:
    def __init__(self, use_case: ProductUseCaseInterface):
        self.use_case = use_case
        self.router = APIRouter(
            tags=["Product"]
        )
        self.register()

    def register(self):
        self.router.get("")(self.get_all)
        self.router.get("/{id}")(self.get)
        self.router.post("")(self.create)
        self.router.put("/{id}")(self.update)
        self.router.delete("/{id}")(self.delete)

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
            sku: str = None,
            name: str = None,
            category_id: str = None,
    ) -> list[Product]:
        try:
            return await self.use_case.get_all(offset=offset, limit=limit, sku=sku, name=name, category_id=category_id)
        except NotFoundException as e:
            logger.error(f"Product not found: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Internal error: {e}\n", traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

    async def get(
            self,
            obj_id: str = Param(alias="id"),
    ) -> Product:
        try:
            uuid_id = uuid.UUID(obj_id)
        except ValueError as e:
            logger.error(f"Invalid UUID: {e}")
            raise HTTPException(status_code=400, detail="Invalid UUID")
        try:
            return await self.use_case.get(uuid_id)
        except NotFoundException as e:
            logger.error(f"Product not found: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Internal error: {e}\n", traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

    async def create(
            self,
            dto: HandlerCreateProductDTO
    ) -> Product:
        try:
            return await self.use_case.create(CreateProductDTO(**dto.model_dump()))
        except Exception as e:
            logger.error(f"Internal error: {e}\n", traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

    async def update(
            self,
            dto: HandlerUpdateProductDTO,
            obj_id: str = Param(alias="id"),
    ) -> None:
        try:
            uuid_id = uuid.UUID(obj_id)
        except ValueError as e:
            logger.error(f"Invalid UUID: {e}")
            raise HTTPException(status_code=400, detail="Invalid UUID")
        try:
            return await self.use_case.update(uuid_id, UpdateProductDTO(**dto.model_dump()))
        except NotFoundException as e:
            logger.error(f"Product not found: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Internal error: {e}\n", traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

    async def delete(
            self,
            obj_id: str = Param(alias="id"),
    ) -> None:
        try:
            uuid_id = uuid.UUID(obj_id)
        except ValueError as e:
            logger.error(f"Invalid UUID: {e}")
            raise HTTPException(status_code=400, detail="Invalid UUID")
        try:
            return await self.use_case.delete(uuid_id)
        except NotFoundException as e:
            logger.error(f"Product not found: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Internal error: {e}\n", traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

