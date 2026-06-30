from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BrandBrief(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    company_name: str
    industry: str = "food_and_beverage"
    products: list[str]
    target_audience: str
    tone: str
    goals: list[str]
    constraints: list[str]
    competitors: list[str]
    created_at: datetime | None = None
    updated_at: datetime | None = None
