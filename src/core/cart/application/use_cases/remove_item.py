from dataclasses import dataclass

from src.core.cart.domain.cart import Cart
from src.core.cart.domain.cart_repository import CartRepository


@dataclass(slots=True)
class RemoveItemFromCart:
    
    repository: CartRepository

    def execute(self, product_name: str) -> Cart:
        cart = self.repository.get_cart()
        cart.remove_item(product_name)
        self.repository.update_cart(cart)
        return cart
