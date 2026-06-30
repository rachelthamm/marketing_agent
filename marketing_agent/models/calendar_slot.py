from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

SlotStatus = Literal["pending", "approved", "published", "rejected"]
Platform = Literal["instagram", "facebook", "tiktok", "twitter", "linkedin"]
PostFormat = Literal["carousel", "reel", "story", "static", "text"]


class CalendarSlot(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    strategy_id: UUID
    slot_date: datetime
    platform: Platform
    pillar: str
    format: PostFormat
    brief: str
    status: SlotStatus = "pending"
    created_at: datetime | None = None
