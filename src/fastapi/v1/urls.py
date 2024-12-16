from fastapi import APIRouter

from src.fastapi.v1.cart_api.views import router as cart_router


router = APIRouter(prefix="/v1")

router.include_router(cart_router, prefix="/cart")
