from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from schemas.response import BaseResponse

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=50)

class UserCreate(UserBase):
    password: str = Field(min_length=6)
    referral_code: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserDB(UserBase):
    id: int
    created_at: datetime
    referred_by: Optional[str] = None

    class Config:
        from_attributes = True
        
class UserResponse(BaseResponse):
    payload: UserDB

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None