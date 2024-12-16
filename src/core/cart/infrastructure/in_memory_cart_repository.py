import copy
from dataclasses import dataclass, field

from src.settings import settings
from src.core.cart.domain.cart import Cart
from src.core.cart.domain.cart_repository import CartRepository


@dataclass(slots=True)
class InMemoryCartRepository(CartRepository):
    
    cart: Cart = field(default_factory=lambda: Cart(customer_type=settings.customer_type))

    def get_cart(self) -> Cart:
        return Cart(
            customer_type=self.cart.customer_type,
            items=copy.deepcopy(self.cart.items)
        )

    def update_cart(self, cart: Cart) -> None:
        self.cart = cart
