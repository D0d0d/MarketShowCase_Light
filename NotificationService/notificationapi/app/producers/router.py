from fastapi import APIRouter, HTTPException
from datetime import datetime
import json
from .. import schemas
from fastapi import Request
router = APIRouter()


@router.post("/{topicname}", response_model=schemas.MessageResponse)
async def kafka_produce(request: Request, msg: schemas.MessageBaseModel,
                        topicname: str):
    msg.timestamp = msg.timestamp if msg.timestamp else datetime.utcnow()
    msg.topic = topicname
    aioproducer = request.app.state.producer
    try:
        await aioproducer.send_and_wait(topicname, 
                                        json.dumps(
                                            msg.dict(), default=str
                                            ).encode("ascii"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'status': 'success', 'message': msg}


@router.get("/cons1", response_model=schemas.MessageResponseList)
async def kafka_consume(request: Request,
                        timeout_ms: int = 1000, limit: int = 10):
    aioconsumer = request.app.state.consumer
    msgs = []
    try:
        data = await aioconsumer.getmany(timeout_ms=timeout_ms,
                                         max_records=limit)
        for tp, messages in data.items():
            for msg in messages:
                msgs.append(msg.value)
                # await consumer.commit({tp: messages[-1].offset + 1})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {'status': 'success', 'messages': msgs}
