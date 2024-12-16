from dataclasses import dataclass

from src.core.cart.application.calculate_strategies.base import CalculateStrategy
from src.core.cart.domain.cart import Cart


@dataclass(slots=True)
class FullPriceCalculateStrategy(CalculateStrategy):
    
    name: str = "Full price"
    
    def execute(self, cart: Cart) -> CalculateStrategy.Output:
        total_price = 0
        for item in cart.items:
            total_price += item.product.price * item.quantity
        return self.Output(strategy_name=self.name, total=round(total_price, ndigits=2))

    @classmethod
    def is_applicable(cls, cart: Cart) -> bool:
        return True