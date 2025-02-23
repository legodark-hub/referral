from authx import TokenPayload
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import Token, UserCreate, UserListResponse, UserLogin, UserResponse
from api.services.user import UserService
from utils.security import security

router = APIRouter(prefix="/user")


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate, service: UserService = Depends(UserService)
):
    user = await service.create_user(user_data)
    return UserResponse(payload=user)


@router.post("/login")
async def login(user_data: UserLogin, service: UserService = Depends(UserService)):
    token = await service.authenticate_user(user_data)
    return Token(access_token=token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def get_me(
    service: UserService = Depends(UserService),
    payload: TokenPayload = Depends(security.access_token_required),
):
    return UserResponse(payload=await service.get_user_by_id(payload.sub))

@router.get("/referrals", response_model=UserListResponse)
async def get_referrals(
    service: UserService = Depends(UserService),
    payload: TokenPayload = Depends(security.access_token_required),
):
    return UserListResponse(payload=await service.get_user_referrals(payload.sub))
