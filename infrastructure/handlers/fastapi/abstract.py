import logging
import traceback
import uuid
from abc import ABC
from typing import Type, Optional

from fastapi import APIRouter, HTTPException
from fastapi.params import Param
from pydantic import BaseModel

from abstractions.repositories.abstract import NotFoundException
from abstractions.usecases import CRUDUseCaseInterface

logger = logging.getLogger(__name__)


class CRUDFastApiHandler:
    def __init__(self, use_case: CRUDUseCaseInterface):
        self.use_case = use_case
        self.router = APIRouter(
            tags=[],
        )
        self.register()

    def register(self):
        self.router.get("/")(self.get_all)
        self.router.get("/{id}")(self.get)
        self.router.post("/")(self.create)
        self.router.put("/{id}")(self.update)
        self.router.delete("/{id}")(self.delete)

    async def get_all(
            self,
            offset: int = 0,
            limit: int = 100,
    ) -> list[Model]:
        try:
            return await self.use_case.get_all(offset=offset, limit=limit)
        except NotFoundException as e:
            logger.error(f"Product not found: {e}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Internal error: {e}\n", traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

    async def get(
            self,
            obj_id: str = Param(alias="id"),
    ) -> Model:
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
            dto: HandlerCreateDTO,
    ) -> Model:
        try:
            return await self.use_case.create(**dto.model_dump())
        except Exception as e:
            logger.error(f"Internal error: {e}\n", traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))

    async def update(
            self,
            dto: HandlerUpdateDTO,
            obj_id: str = Param(alias="id"),
    ) -> None:
        try:
            uuid_id = uuid.UUID(obj_id)
        except ValueError as e:
            logger.error(f"Invalid UUID: {e}")
            raise HTTPException(status_code=400, detail="Invalid UUID")
        try:
            return await self.use_case.update(uuid_id, **dto.model_dump())
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
