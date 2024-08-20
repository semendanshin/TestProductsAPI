from abc import abstractmethod
from dataclasses import dataclass
from typing import Type

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker

from abstractions.repositories.abstract import CRUDRepositoryInterface, AlreadyExistsException, NotFoundException


@dataclass
class AbstractSQLAlchemyRepository[Entity, Model, CreateDTO, UpdateDTO](
    CRUDRepositoryInterface[Model, CreateDTO, UpdateDTO]
):
    session_maker: async_sessionmaker

    def __post_init__(self):
        self.entity: Type[Entity] = self.__orig_bases__[0].__args__[0] # noqa

    async def create(self, obj: CreateDTO) -> Model:
        entity = self.create_dto_to_entity(obj)
        async with self.session_maker() as session:
            try:
                async with session.begin():
                    session.add(entity)
                    await session.flush()
                    return self.entity_to_model(entity)
            except IntegrityError as e:
                raise AlreadyExistsException("Unique constraint violation") from e

    async def get(self, obj_id: str) -> Model:
        async with self.session_maker() as session:
            res = await session.execute(
                select(self.entity).where(self.entity.id == obj_id)
            )
            try:
                obj = res.scalars().one()
            except NoResultFound as e:
                raise NotFoundException(f"Entity with id {obj_id} not found") from e
            return self.entity_to_model(obj)

    async def update(self, obj_id: str, obj: UpdateDTO) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                stm = (
                    select(self.entity).where(self.entity.id == obj_id).with_for_update()
                )
                entity = (await session.execute(stm)).scalars().one()
                for key, value in obj.__dict__.items():
                    setattr(entity, key, value)
                await session.flush()

    async def delete(self, obj_id: str) -> None:
        async with self.session_maker() as session:
            async with session.begin():
                stm = delete(self.entity).where(self.entity.id == obj_id)
                await session.execute(stm)

    async def get_all(self, limit: int = 100, offset: int = 0, **kwargs) -> list[Model]:
        async with self.session_maker() as session:
            stm = select(self.entity).order_by(self.entity.created_at.desc())
            for key, value in kwargs.items():
                stm = stm.where(getattr(self.entity, key) == value) # noqa
            stm = stm.limit(limit).offset(offset)
            return [
                self.entity_to_model(entity)
                for entity in (await session.execute(stm)).scalars().all()
            ]

    @abstractmethod
    def entity_to_model(self, entity: Entity) -> Model:
        pass

    @abstractmethod
    def model_to_entity(self, model: Model) -> Entity:
        pass

    @abstractmethod
    def create_dto_to_entity(self, create_dto: CreateDTO) -> Entity:
        pass

    @abstractmethod
    def update_dto_to_entity(self, update_dto: UpdateDTO) -> Entity:
        pass
