from authx import TokenPayload
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import Token, UserCreate, UserLogin, UserResponse
from api.services.user import UserService
from utils.security import security

router = APIRouter(prefix="/user")


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(
    user_data: UserCreate, service: UserService = Depends(UserService)
):
    if await service.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )
    if await service.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

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


@router.get("/protected", dependencies=[Depends(security.access_token_required)])
def get_protected():
    return {"message": "Hello World"}