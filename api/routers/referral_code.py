from datetime import datetime, timedelta
from authx import TokenPayload
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from schemas.referral_code import ReferralCodeCreate, ReferralCodeResponse
from api.services.referral_code import ReferralCodeService
from utils.security import security


router = APIRouter(prefix="/referral_code")


@router.post(
    "/create", response_model=ReferralCodeResponse, status_code=status.HTTP_201_CREATED
)
async def create_referral_code(
    referral_data: ReferralCodeCreate,
    service: ReferralCodeService = Depends(ReferralCodeService),
    payload: TokenPayload = Depends(security.access_token_required),
):
    referral_code = await service.create(referral_data, payload.sub)
    return ReferralCodeResponse(payload=referral_code)

@router.get(
    "/my", response_model=ReferralCodeResponse
)
async def get_my_referral_code(
    service: ReferralCodeService = Depends(ReferralCodeService),
    payload: TokenPayload = Depends(security.access_token_required),
):
    referral_code = await service.get_by_user_id(payload.sub)
    return ReferralCodeResponse(payload=referral_code)


@router.delete(
    "/delete", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_referral_code(
    service: ReferralCodeService = Depends(ReferralCodeService),
    payload: TokenPayload = Depends(security.access_token_required),
):
    return await service.delete(payload.sub)
