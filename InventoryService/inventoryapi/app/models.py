import uuid
from .database import Base
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID


class Inventory(Base):
    __tablename__ = 'Inventory'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False,
                default=uuid.uuid4)
    name = Column(String,  nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    reserved = Column(Integer, nullable=False)

