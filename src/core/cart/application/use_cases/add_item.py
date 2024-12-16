from dataclasses import dataclass

from src.core.cart.domain.cart import Cart
from src.core.cart.domain.cart_repository import CartRepository
from src.core.product.application.exceptions import ProductNotFoundException
from src.core.product.domain.product_repository import ProductRepository


@dataclass(slots=True)
class AddItemToCart:

    repository: CartRepository
    product_repository: ProductRepository
    
    def execute(self, product_name: str) -> Cart:
        product = self.product_repository.get_by_name(product_name)
        if not product:
            raise ProductNotFoundException(product_name)

        cart = self.repository.get_cart()
        if not cart:
            cart = Cart(items=[])

        cart.add_item(product)
        self.repository.update_cart(cart)
        return cart
