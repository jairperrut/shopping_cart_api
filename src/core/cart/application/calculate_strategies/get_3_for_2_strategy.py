from dataclasses import dataclass

from src.core.cart.application.calculate_strategies.base import CalculateStrategy
from src.core.cart.domain.cart import Cart


@dataclass(slots=True)
class Get3For2CalculateStrategy(CalculateStrategy):
    
    name: str = "Get 3 for 2"
    
    def execute(self, cart: Cart) -> CalculateStrategy.Output:
        total_price = 0
        items = sorted(cart.items, key=lambda item: item.product.price)
        free_items = cart.total_items // 3
        for item in items:
            for _ in range(item.quantity):
                if free_items > 0:
                    free_items -= 1
                else:
                    total_price += item.product.price
        return self.Output(strategy_name=self.name, total=round(total_price, ndigits=2))

    @classmethod
    def is_applicable(cls, cart: Cart) -> bool:
        return cart.total_items >= 3
