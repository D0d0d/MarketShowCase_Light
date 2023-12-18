from .producers import router as producer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import env

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


app.include_router(producer.router, tags=['producer'], prefix='/api/produce')


@app.get("/api/notificationService")
def root():
    return {"message": "That is NotificationService!"}


@app.on_event("startup")
async def startup_event():
    for aioproducer in env.aioproducers:
        await aioproducer.start()
    for consumer in env.consumers:
        env.loop.create_task(consumer["consume"](consumer["consumer"]))


@app.on_event("shutdown")
async def shutdown_event():
    for aioproducer in env.aioproducers:
        await aioproducer.stop()
    for consumer in env.consumers:
        await consumer["consumer"]
