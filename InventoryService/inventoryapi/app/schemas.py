import uuid
from pydantic import BaseModel
from typing import List


class InventoryBase(BaseModel):
    name: str
    amount: int
    price: float
    reserved: int | None = 0

    class Config:
        orm_mode = True


class InventoryResponse(InventoryBase):
    id: uuid.UUID


class CreateInventory(InventoryBase):
    pass


class UpdateInventory(BaseModel):
    name: str
    amount: int
    price: float
    reserved: int | None = 0


class ListInventory(BaseModel):
    status: str
    results: int
    Inventory: List[InventoryResponse]
