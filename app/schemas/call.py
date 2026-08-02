from datetime import datetime

from pydantic import BaseModel


class CallCreate(BaseModel):
    customer_id: int


class CallResponse(BaseModel):
    id: int
    customer_id: int
    started_at: datetime
    ended_at: datetime | None
    status: str
    transcript: str | None
    summary: str | None

    model_config = {
        "from_attributes": True
    }


class CallEnd(BaseModel):
    transcript: str
    summary: str