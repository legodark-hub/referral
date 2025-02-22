from fastapi import FastAPI
from api.routers.user import router as user_router
from api.routers.referral_code import router as referral_code_router


app = FastAPI()

app.include_router(user_router)
app.include_router(referral_code_router)

