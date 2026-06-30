from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Strategy(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    brand_brief_id: UUID
    positioning: str
    content_pillars: list[str]
    channels: list[str]
    cadence: str
    kpis: list[str]
    created_at: datetime | None = None
