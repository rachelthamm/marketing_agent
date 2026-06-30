from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class Post(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: UUID = Field(default_factory=uuid4)
    slot_id: UUID
    caption: str = Field(alias="copy")
    hashtags: list[str]
    media_prompt: str
    approved: bool = False
    postiz_post_id: str | None = None
    published_at: datetime | None = None
    created_at: datetime | None = None
