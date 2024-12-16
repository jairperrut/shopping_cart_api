from pydantic import BaseModel

from src.core.product.domain.product import Product

class CartItem(BaseModel):
    product: Product
    quantity: int = 0