from datetime import datetime
from typing import Annotated, Any, Awaitable, Callable
from sqlalchemy import DateTime, text
from sqlalchemy.orm import mapped_column

AsyncFunc = Callable[..., Awaitable[Any]]

dt_now_utc_sql = text("TIMEZONE('utc', now())")
created_at = Annotated[datetime, mapped_column(DateTime, server_default=dt_now_utc_sql)]
updated_at = Annotated[
    datetime,
    mapped_column(
        DateTime,
        server_default=dt_now_utc_sql,
        onupdate=dt_now_utc_sql,
    ),
]
