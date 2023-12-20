import json
from fastapi import APIRouter
from datetime import datetime

from . import schemas
from ..env import aioproducers

router = APIRouter()
aioproducer = aioproducers[0]


@router.post("/{topicname}", response_model=schemas.MessageResponse)
async def kafka_produce(msg: schemas.MessageBaseMdoel, topicname: str):
    msg.timestamp = msg.timestamp if msg.timestamp else datetime.utcnow()
    msg.topic = topicname
    await aioproducer.send(topicname, json.dumps(msg.dict(), default=str).encode("ascii"))
    return {'status': 'success', 'message': msg}


@router.on_event("startup")
async def startup_event():
    await aioproducer.start()


@router.on_event("shutdown")
async def shutdown_event():
    await aioproducer.stop()