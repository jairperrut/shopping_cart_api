from dataclasses import dataclass
from typing import List

from src.core.cart.application.calculate_strategies.base import CalculateStrategy
from src.core.cart.domain.cart import Cart


@dataclass(slots=True)
class AddItemRequest:
    product_name: str

@dataclass(slots=True)
class AddItemRespose:
    cart: Cart
    prices: List[CalculateStrategy.Output]
    best_deal: CalculateStrategy.Output

@dataclass(slots=True)
class RemoveItemRequest:
    product_name: str
    
@dataclass(slots=True)
class RemoveItemRespose:
    cart: Cart
    prices: List[CalculateStrategy.Output]
    best_deal: CalculateStrategy.Output
