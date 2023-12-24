from pydantic import BaseModel, StrictStr
from datetime import datetime
from typing import List


class MessageBaseModel(BaseModel):
    text: StrictStr
    topic: StrictStr | None = None
    timestamp: datetime | None = None


class MessageResponse(BaseModel):
    status: StrictStr
    message: MessageBaseModel | None = None


class MessageResponseList(BaseModel):
    status: StrictStr
    messages: List[MessageBaseModel] | None = None
