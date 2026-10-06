from fastapi import APIRouter

from .endpoints import product, user

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(user.router)
api_router.include_router(product.router)
