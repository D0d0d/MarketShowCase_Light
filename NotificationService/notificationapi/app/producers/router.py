from fastapi import APIRouter, HTTPException
from datetime import datetime
import json
from . import schemas
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from ..config import settings
from fastapi import Request
router = APIRouter()


@router.post("/{topicname}", response_model=schemas.MessageResponse)
async def kafka_produce(request: Request, msg: schemas.MessageBaseMdoel,
                        topicname: str):
    msg.timestamp = msg.timestamp if msg.timestamp else datetime.utcnow()
    msg.topic = topicname
    aioproducer = AIOKafkaProducer(
        loop=request.app.state.loop,
        bootstrap_servers=settings.KAFKA_INSTANCE)
    await aioproducer.start()
    try:
        await aioproducer.send(topicname, json.dumps(msg.dict(), default=str
                                                     ).encode("ascii"))
        await aioproducer.flush()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await aioproducer.stop()
    return {'status': 'success', 'message': msg}


def kafka_json_deserializer(serialized):
    return json.loads(serialized)


@router.get("/{topicname}", response_model=schemas.MessageResponseList)
async def kafka_consume(request: Request,
                        topicname: str,
                        timeout_ms: int = 1000, limit: int = 50):
    aioconsumer = AIOKafkaConsumer(
        "cons1",
        bootstrap_servers=settings.KAFKA_INSTANCE,
        value_deserializer=kafka_json_deserializer,
        loop=request.app.state.loop)
    await aioconsumer.start()
    msgs = []
    try:
        result = await aioconsumer.getmany()
        msgs = result.items()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await aioconsumer.stop()
    return {'status': 'success', 'message': str(msgs)}
