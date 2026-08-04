from datetime import datetime

from pydantic import BaseModel


class CallCreate(BaseModel):
    customer_id: int


class CallResponse(BaseModel):
    id: int
    customer_id: int
    started_at: datetime
    ended_at: datetime | None
    created_at: datetime
    status: str
    transcript: str | None
    summary: str | None
    sentiment: str | None = None
    intent: str | None = None
    embedding_id: str | None = None

    model_config = {
        "from_attributes": True
    }


class CallEnd(BaseModel):
    transcript: str