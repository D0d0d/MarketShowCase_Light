#       Product Serialize


def productItemsEntity(product) -> dict:
    return {
        "id": str(product["_id"]),
        "uuid": product["uuid"],
        "order": str(product["order"]),
        "name": product["name"],
        "amount": product["amount"],
        "price": product["price"],
    }


def productItemsErrorEntity(product) -> dict:
    return {
        "uuid": product["uuid"],
        "name": product["name"],
        "amount": product["amount"],
    }


def productItemsListEntity(products) -> list:
    return [productItemsEntity(product) for product in products]


def productItemsListErrorEntity(products) -> list:
    return [productItemsErrorEntity(product) for product in products]
#       Order Serialize


def orderCreateEntity(order) -> dict:
    return {
        "id": str(order["_id"]),
        "date": order["date"],
        "productItems":productItemsListEntity(order["productItems"])
    }


def orderCreateErrorEntity(order) -> dict:
    return {
        "error":"Item not available",
        "productItems":productItemsListErrorEntity(order["productItems"])
    }


def orderEntity(order) -> dict:
    return {
        "id": str(order["_id"]),
        "date": order["date"]
    }


def orderListEntity(orders) -> list:
    return [orderEntity(order) for order in orders]
