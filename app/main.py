from fastapi import FastAPI
from app.api.customers import router as customer_router
from app.api.root import router as root_router
from app.core.config import settings
from app.api.auth import router as auth_router
from app.api.users import router as users_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.include_router(root_router)
app.include_router(customer_router)
app.include_router(auth_router)
app.include_router(users_router)