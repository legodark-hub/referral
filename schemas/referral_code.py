from datetime import datetime
from pydantic import BaseModel, Field

from schemas.response import BaseResponse

class ReferralCodeBase(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)

class ReferralCodeCreate(BaseModel):
    expiry_period: int = Field(..., gt=0, le=90)

class ReferralCodeDB(ReferralCodeBase):
    id: int
    user_id: int
    expires_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
class ReferralCodeResponse(BaseResponse):
    payload: ReferralCodeDB

class ReferralCodeUpdate(BaseModel):
    expires_at: datetime | None = None
