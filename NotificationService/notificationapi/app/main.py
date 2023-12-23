from .producers import router as producer
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio

loop = asyncio.get_event_loop()


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.loop = loop
    yield


app = FastAPI(lifespan=lifespan)

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
