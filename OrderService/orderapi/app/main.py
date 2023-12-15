from .routers import orders, productItems
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(orders.router, tags=['Orders'], prefix='/api/orders')
app.include_router(productItems.router, tags=['Orders'], prefix='/api/productItems')

@app.get("/api/orderService")
def root():
    return {"message": "That is OrderService!"}