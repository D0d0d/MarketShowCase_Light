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


@app.on_event("startup")
async def startup_event():
    prods = []
    cons = []
    try:
        for aioproducer in env.aioproducers:
            await aioproducer.start()
            prods.append[aioproducer]
        for consumer in env.consumers:
            env.loop.create_task(consumer["consume"](consumer["consumer"]))
            cons.append[consumer["consumer"]]
    except Exception:
        await shutdown_event()


@app.on_event("shutdown")
async def shutdown_event():
    for aioproducer in env.aioproducers:
        await aioproducer.stop()
    for consumer in env.consumers:
        await consumer["consumer"].stop()


app.include_router(producer.router, tags=['producer'], prefix='/api/produce')


@app.get("/api/notificationService")
def root():
    return {"message": "That is NotificationService!"}
