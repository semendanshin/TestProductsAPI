import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Base:
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


@dataclass
class Product(Base):
    sku: str
    name: str
    description: str
    price: int
