from authx import AuthX, AuthXConfig
from fastapi import FastAPI
from api.routers.user import router
from config import JWT_SECRET_KEY


app = FastAPI()

app.include_router(router)

config = AuthXConfig()
config.JWT_ALGORITHM = "HS256"
config.JWT_SECRET_KEY = JWT_SECRET_KEY

security = AuthX(config=config)