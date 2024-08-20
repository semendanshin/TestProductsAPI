import uuid
from abc import ABC
from dataclasses import dataclass

from abstractions.repositories import CRUDRepositoryInterface
from abstractions.usecases.abstract import CRUDUseCaseInterface


@dataclass
class AbstractCRUDUseCase[
    Model, CreateDTO, UpdateDTO
](
    CRUDUseCaseInterface[Model, CreateDTO, UpdateDTO],
    ABC,
):
    repository: CRUDRepositoryInterface[Model, CreateDTO, UpdateDTO]

    async def create(self, obj: CreateDTO) -> Model:
        return await self.repository.create(obj)

    async def get(self, obj_id: uuid.UUID) -> Model:
        return await self.repository.get(obj_id)

    async def update(self, obj_id: uuid.UUID, obj: UpdateDTO) -> None:
        await self.repository.update(obj_id, obj)

    async def delete(self, obj_id: uuid.UUID) -> None:
        await self.repository.delete(obj_id)

    async def get_all(self, limit: int = 100, offset: int = 0, **kwargs) -> list[Model]:
        return await self.repository.get_all(limit, offset, **kwargs)
