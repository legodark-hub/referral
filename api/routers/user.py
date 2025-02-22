from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import UserCreate, UserLogin, UserResponse
from api.services.user import UserService

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
    return await service.authenticate_user(user_data)
