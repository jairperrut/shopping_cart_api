from typing import List
from dataclasses import dataclass, field

from src.core.cart.domain.cart_item import CartItem
from src.core.cart.domain.customer import CustomerType
from src.core.product.domain.product import Product


@dataclass(slots=True)
class Cart:
    customer_type: CustomerType = CustomerType.COMMON
    items: List[CartItem] = field(default_factory=lambda: [])

    def add_item(self, product: Product) -> None:
        for item in self.items:
            if item.product == product:
                item.quantity += 1
                return 
        self.items.append(CartItem(product=product, quantity=1))

    def remove_item(self, product_name: str) -> None:
        for item in self.items:
            if item.product.name == product_name:
                item.quantity -= 1
                if item.quantity == 0:
                    self.items.remove(item)

    @property
    def is_vip(self) -> bool:
        return self.customer_type == CustomerType.VIP
    
    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)
    
    @property
    def total_price(self) -> float:
        return sum(item.quantity * item.product.price for item in self.items)

    def to_list(self) -> List[Product]:
        return [item.product for item in self.items]