from fastapi import FastAPI
from app.api.customers import router as customer_router
from app.api.root import router as root_router
from app.core.config import settings
from fastapi import HTTPException
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.core.middleware import log_requests
from app.api.calls import router as call_router
from app.api.ai import router as ai_router
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.exceptions import (
    http_exception_handler,
    general_exception_handler,
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    Exception,
    general_exception_handler,
)
app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=log_requests,
)

app.include_router(root_router)
app.include_router(customer_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(call_router)
app.include_router(ai_router)