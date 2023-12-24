from .producers import router as producer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from .config import settings
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import json

loop = asyncio.get_event_loop()
aioconsumer = AIOKafkaConsumer(
        "cons1",
        bootstrap_servers=settings.KAFKA_INSTANCE,
        enable_auto_commit=True,
        auto_commit_interval_ms=1000,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        loop=loop)
aioproducer = AIOKafkaProducer(
        loop=loop,
        bootstrap_servers=settings.KAFKA_INSTANCE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.loop = loop
    app.state.producer = aioproducer
    app.state.consumer = aioconsumer
    await app.state.producer.start()
    await app.state.consumer.start()
    yield
    await app.state.producer.stop()
    await app.state.consumer.stop()

app = FastAPI(lifespan=lifespan)
origins = ["http://localhost:3000",]
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
