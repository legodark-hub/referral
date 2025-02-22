from fastapi import FastAPI
from api.routers.user import router


app = FastAPI()

app.include_router(router)

