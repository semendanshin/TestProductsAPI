import uuid
from abc import ABC, abstractmethod


class CRUDUseCaseInterface[
    Model, CreateDTO, UpdateDTO
](ABC):
    @abstractmethod
    async def create(self, obj: CreateDTO) -> Model:
        pass

    @abstractmethod
    async def get(self, obj_id: uuid.UUID) -> Model:
        pass

    @abstractmethod
    async def update(self, obj_id: uuid.UUID, obj: UpdateDTO) -> None:
        pass

    @abstractmethod
    async def delete(self, obj_id: uuid.UUID) -> None:
        pass

    @abstractmethod
    async def get_all(self, limit: int = 100, offset: int = 0, **kwargs) -> list[Model]:
        pass
    