from fastapi import APIRouter
from app.api.v1.routes.auth_routes import router as auth_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="", tags=["Auth"])
api_router.include_router(product_router, prefix="/product", tags=["Products"])
