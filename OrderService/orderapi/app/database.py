from pymongo import mongo_client, ASCENDING
from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)

db = client[settings.MONGO_INITDB_DATABASE]
Orders = db.orders
ProductItems = db.productItems
