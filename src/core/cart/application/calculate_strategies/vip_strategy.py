from dataclasses import dataclass

from src.settings import settings
from src.core.cart.domain.customer import CustomerType
from src.core.cart.application.calculate_strategies.base import CalculateStrategy
from src.core.cart.domain.cart import Cart

@dataclass(slots=True)
class VIPCalculateStrategy(CalculateStrategy):
    
    name: str = "VIP Discount"
    discount: float = settings.vip_discount
    
    def execute(self, cart: Cart) -> CalculateStrategy.Output:
        total_price = sum(item.product.price * item.quantity for item in cart.items)
        total_price *= 1 - self.discount # 100% - VIP_DISCOUNT
        return self.Output(self.name, round(total_price, ndigits=2))

    @classmethod
    def is_applicable(cls, cart: Cart) -> bool:
        return cart.customer_type == CustomerType.VIP