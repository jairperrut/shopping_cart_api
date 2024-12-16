from fastapi import APIRouter, Depends, HTTPException

from src.core.cart.application.calculate_strategies.base import CalculateStrategyFactory
from src.core.cart.application.use_cases.add_item import AddItemToCart
from src.core.cart.application.use_cases.calculate import CalculateCart
from src.core.cart.application.use_cases.remove_item import RemoveItemFromCart
from src.core.cart.domain.cart_repository import CartRepository
from src.core.product.domain.product_repository import ProductRepository
from src.fastapi.dependencies import get_cart_repository, get_product_repository
from src.fastapi.v1.cart_api.schemas import AddItemRequest, AddItemRespose, RemoveItemRequest, RemoveItemRespose

router = APIRouter()

@router.post("/items", response_model=AddItemRespose)
async def add_item_to_cart(
    request: AddItemRequest,
    cart_repository: CartRepository = Depends(get_cart_repository),
    product_repository: ProductRepository = Depends(get_product_repository)
):
    try:
        cart = AddItemToCart(cart_repository, product_repository).execute(request.product_name)
        result = CalculateCart(CalculateStrategyFactory).execute(cart)
        return AddItemRespose(
            cart,
            result.prices,
            result.best_deal
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/items")
async def remove_item_from_cart(
    request: RemoveItemRequest,
    cart_repository: CartRepository = Depends(get_cart_repository)
):
    try:
        cart = RemoveItemFromCart(cart_repository).execute(request.product_name)
        result = CalculateCart(CalculateStrategyFactory).execute(cart)
        return RemoveItemRespose(
            cart,
            result.prices,
            result.best_deal
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
