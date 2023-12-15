from datetime import datetime
from fastapi import HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from ..schemas import productItems as schemas
from ..database import Orders, ProductItems
from ..serializers import productItemsListEntity, productItemsEntity
from bson.objectid import ObjectId

router = APIRouter()


@router.get('/', response_model=schemas.ListProductItemsResponse)
def get_products(limit: int = 10, page: int = 1, search: str = ''):
    try:
        skip = (page - 1) * limit
        pipeline = [
            {
                '$skip': skip
            }, {
                '$limit': limit
            }
        ]
        pipeline.append(
            {'$match': {"order":ObjectId(search)}} if ObjectId.is_valid(search)
            else {'$match': {'name':{'$regex': search, '$options': 'i'}}})
        productItems = productItemsListEntity(ProductItems.aggregate(pipeline))
        return {'status': 'success', 'results': len(productItems),
                'productItems': productItems}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=str(e)+"1")


@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schemas.ProductItemsResponse)
def create_product(payload: schemas.ProductItemsCreateSchema):

    try:
        payload.order = ObjectId(payload.order)
        result = ProductItems.insert_one(payload.dict())
        new_ProductItem = ProductItems.find_one({'_id': result.inserted_id})
        return {"status": "success",
                "productItem": productItemsEntity(new_ProductItem)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e)+"1")


@router.patch('/{productItemsId}',
              response_model=schemas.ProductItemsResponse)
def update_product(productItemsId: str, payload: schemas.ProductItemsUpdate):
    if not ObjectId.is_valid(productItemsId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {productItemsId}")
    updated_productItem = ProductItems.find_one_and_update(
        {'id': ObjectId(productItemsId)}, 
        {'$set': payload.dict(exclude_none=True)}, 
        return_document=ReturnDocument.AFTER)
    if not updated_productItem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No productItems with this id: {productItemsId} found')
    return {"status": "success",
            "productItem": productItemsEntity(updated_productItem)}


@router.get('/{productItemsId}', response_model=schemas.ProductItemsResponse)
def get_product(productItemsId: str):
    if not ObjectId.is_valid(productItemsId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {productItemsId}")

    productItem = ProductItems.find_one({'_id': ObjectId(productItemsId)})
    if not productItem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No ProductItems with this id: {productItemsId} found")
    return {"status": "success", "note": productItemsEntity(productItem)}


@router.delete('/{productItemsId}')
def delete_product(productItemsId: str):
    if not ObjectId.is_valid(productItemsId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {productItemsId}")
    note = ProductItems.find_one_and_delete({'id': ObjectId(productItemsId)})
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No ProductItems with this id: {productItemsId} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)