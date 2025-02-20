from datetime import datetime
from pydantic import BaseModel, Field

class ReferralCodeBase(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)
    expires_at: datetime

class ReferralCodeCreate(ReferralCodeBase):
    user_id: int

class ReferralCodeResponse(ReferralCodeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ReferralCodeUpdate(BaseModel):
    expires_at: datetime | None = None
