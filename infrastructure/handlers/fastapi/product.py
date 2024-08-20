import logging
import traceback
import uuid
from typing import Optional

from fastapi import APIRouter
from fastapi.params import Param
from pydantic import BaseModel

from starlette.exceptions import HTTPException

from abstractions.repositories.abstract import NotFoundException
from abstractions.repositories.product import CreateProductDTO, UpdateProductDTO
from domain import Product
from usecases import ProductUseCase

logger = logging.getLogger(__name__)



class HandlerCreateProductDTO(BaseModel):
    sku: str
    name: str
    description: str
    price: float

class HandlerUpdateProductDTO(BaseModel):
    sku: Optional[str]
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]

class FastApiProductHandler:
    def __init__(self, product_use_case: ProductUseCase):
        self.product_use_case = product_use_case
        self.router = APIRouter(
            prefix="/products",
            tags=["products"],
        )
        self.register()

    def register(self):
        self.router.get("/",)(self.get_all)
        self.router.get("/{id}")(self.get)
        self.router.post("/")(self.create)
        self.router.put("/{id}")(self.update)
        self.router.delete("/{id}")(self.delete)

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
            sku: str = None,
            name: str = None,
    ) -> list[Product]:
        try:
            return await self.product_use_case.get_all(offset=offset, limit=limit, sku=sku, name=name)
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
            return await self.product_use_case.get(uuid_id)
        except NotFoundException as e:
            logger.error(f"Product not found: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Internal error: {e}\n", traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))


    async def create(
            self,
            dto: HandlerCreateProductDTO,
    ) -> None:
        try:
            return await self.product_use_case.create(CreateProductDTO(**dto.model_dump()))
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
            return await self.product_use_case.update(uuid_id, UpdateProductDTO(**dto.model_dump()))
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
            return await self.product_use_case.delete(uuid_id)
        except NotFoundException as e:
            logger.error(f"Product not found: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Internal error: {e}\n", traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))
