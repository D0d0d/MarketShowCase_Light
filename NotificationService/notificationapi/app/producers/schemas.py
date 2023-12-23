from pydantic import BaseModel, StrictStr
from datetime import datetime


class MessageBaseMdoel(BaseModel):
    text: StrictStr
    message_id: StrictStr | None = " "
    topic: StrictStr | None = None
    timestamp: datetime | None = None


class MessageResponse(BaseModel):
    status: StrictStr
    message: MessageBaseMdoel | None = None


class MessageResponseList(BaseModel):
    status: StrictStr
    message: StrictStr | None = None
