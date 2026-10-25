from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field


class PlanBase(BaseModel):
    name: str = Field(..., max_length=50)
    code: str = Field(..., max_length=30)
    description: str | None = None
    max_branches: int = Field(..., ge=1)
    has_ai_access: bool = False
    price_monthly: Decimal = Field(..., ge=0)
    is_active: bool = True


class PlanCreate(PlanBase):
    pass


class PlanRead(PlanBase):
    id: UUID

    model_config = {"from_attributes": True}
