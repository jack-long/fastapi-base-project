from fastapi import APIRouter

from .routers import (
    login,
    items,
    users
    )

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(login.router)
api_router.include_router(items.router)
api_router.include_router(users.router)
