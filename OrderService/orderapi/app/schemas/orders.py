from datetime import datetime
from typing import List
from pydantic import BaseModel
from bson.objectid import ObjectId
from .productItems import ProductItemsBaseSchema

#        OrderSchemas


class OrdersBaseSchema(BaseModel):
    date: datetime | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateOrdersSchema(OrdersBaseSchema):
    id: str | None = None
    pass


class OrdersResponseSchema(OrdersBaseSchema):
    id: str | None = None
    pass


class OrdersResponse(BaseModel):
    status: str
    order: OrdersResponseSchema


class OrderCreateSchema(OrdersBaseSchema):
    productItems: List[ProductItemsBaseSchema]
    pass


class EmbedOrder(OrdersResponseSchema):
    productItems: List[ProductItemsBaseSchema]
    pass


class EmbedOrderResponse(BaseModel):
    status: str
    order: EmbedOrder


class ListOrdersResponse(BaseModel):
    status: str
    results: int
    orders: List[OrdersResponseSchema]