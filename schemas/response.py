from pydantic import BaseModel
from starlette.status import HTTP_200_OK


class BaseResponse(BaseModel):
    status_code: int = HTTP_200_OK
    error: bool = False
