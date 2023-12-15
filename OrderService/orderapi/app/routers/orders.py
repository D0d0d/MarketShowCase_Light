from datetime import datetime
from fastapi import HTTPException, status, APIRouter, Response
from pymongo.collection import ReturnDocument
from ..schemas import orders as schemas
from ..verifier import Verifier
from ..database import Orders, ProductItems
from ..serializers import orderEntity, orderListEntity, orderCreateEntity, orderCreateErrorEntity
from bson.objectid import ObjectId

router = APIRouter()

@router.get('/item/')
def check_item(amount: str):
    verifier = Verifier()
    res = verifier.check_item(verifier._item("2b2df997-ad8e-4392-8ceb-0cb6ce920109", amount))
    return {"the item": res["msg"], "res":res["res"]}

@router.get('/', response_model=schemas.ListOrdersResponse)
def get_orders(limit: int = 10, page: int = 1, search: str = datetime(1, 1, 1)):
    try:
        skip = (page - 1) * limit
        pipeline = [
            {'$match': {'date': {'$gte': search}}},
            {
                '$skip': skip
            }, {
                '$limit': limit
            }
        ]
        orders = orderListEntity(Orders.aggregate(pipeline))
        return {'status': 'success', 'results': len(orders),
                'orders': orders}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                        detail=str(e))


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.EmbedOrderResponse)
def create_order(payload: schemas.OrderCreateSchema):
    payload.date = payload.date if payload.date else datetime.utcnow()
    try:
        productItems = payload.productItems
        order = payload.dict()
        del order['productItems']

        new_ProductItems = []
        products = []
        for item in productItems:
            product = item.dict()
            
            verifier = Verifier()
            res = None
            try:
                res = verifier.check_item(verifier._item(product['uuid'], product['amount']))
            except Exception:
                new_order = {"productItems": [product]}
                return {"status": res, "order": orderCreateErrorEntity(new_order)}

            product['price'] = res['price']
            products.append(product)

                

            result = Orders.insert_one(order)
            new_order = Orders.find_one({'_id': result.inserted_id})  
            for p in products:
                p["order"] = ObjectId(result.inserted_id)
                product_res = ProductItems.insert_one(p)
                new_ProductItems.append(ProductItems.find_one({'_id': product_res.inserted_id}))
        new_order["productItems"] = new_ProductItems
        return {"status": "success", "order": orderCreateEntity(new_order)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))




@router.patch('/{orderId}', response_model=schemas.OrdersResponse)
def update_order(orderId: str, payload: schemas.UpdateOrdersSchema):
    if not ObjectId.is_valid(orderId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {orderId}")
    updated_order = Orders.find_one_and_update(
        {'_id': ObjectId(orderId)}, {'$set': payload.dict(exclude_none=True)}, return_document=ReturnDocument.AFTER)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No order with this id: {orderId} found')
    return {"status": "success", "order": orderEntity(updated_order)}


@router.get('/{orderId}', response_model=schemas.OrdersResponse)
def get_order(orderId: str):
    if not ObjectId.is_valid(orderId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {orderId}")

    order = Orders.find_one({'id': ObjectId(orderId)})
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No order with this id: {orderId} found")
    return {"status": "success", "order": orderEntity(order)}


@router.delete('/{orderId}')
def delete_order(orderId: str):
    if not ObjectId.is_valid(orderId):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid id: {orderId}")
    order = Orders.find_one_and_delete({'_id': ObjectId(orderId)})
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No order with this id: {orderId} found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)


