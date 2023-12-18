from pydantic import BaseModel, StrictStr
from datetime import datetime


class MessageBaseMdoel(BaseModel):
    name: StrictStr
    message_id: StrictStr | None = " "
    topic: StrictStr    | None = None
    timestamp: datetime | None = None


class MessageResponse(BaseModel):
    status: StrictStr
    message: MessageBaseMdoel | None = None
