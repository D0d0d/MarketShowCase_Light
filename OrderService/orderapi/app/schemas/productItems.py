from typing import List
from pydantic import BaseModel
from bson.objectid import ObjectId

#        ProductItems Schemas


class ProductItemsBaseSchema(BaseModel):
    uuid: str
    name: str
    amount: int
    price: float | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ProductItemsCreateSchema(ProductItemsBaseSchema):
    order: str
    pass


class ProductItemsResponseSchema(ProductItemsBaseSchema):
    id: str
    order: str
    pass

         
class ProductItemsResponse(BaseModel):
    status: str
    productItem: ProductItemsResponseSchema


class ProductItemsUpdate(BaseModel):
    uuid: str | None = None
    name: str | None = None
    amount: int | None = None
    price: float | None = None
    order: str | None = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ListProductItemsResponse(BaseModel):
    status: str
    results: int
    productItems: List[ProductItemsResponseSchema]

