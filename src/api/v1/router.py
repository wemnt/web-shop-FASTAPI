from fastapi import APIRouter

from .endpoints import products, users

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(users.router)
api_router.include_router(products.router)
