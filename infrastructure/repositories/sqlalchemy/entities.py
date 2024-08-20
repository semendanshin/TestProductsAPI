import uuid
from datetime import datetime

from sqlalchemy import UUID, TIMESTAMP, func, String, Integer
from sqlalchemy.orm import declarative_base, mapped_column, Mapped

Base = declarative_base()


class BaseEntity(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(),
                                                 onupdate=func.current_timestamp())


class Product(BaseEntity):
    __tablename__ = 'products'

    sku: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
