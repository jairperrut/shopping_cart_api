from abc import ABC, abstractmethod
from dataclasses import dataclass
from inspect import isabstract, isclass
from typing import List

from src.core.cart.domain.cart import Cart


class CalculateStrategy(ABC):

    @dataclass(slots=True)
    class Output:
        strategy_name: str
        total: float

    @abstractmethod
    def execute(self, cart: Cart) -> "Output":
        pass

    @classmethod
    @abstractmethod
    def is_applicable(cls, cart: Cart) -> bool:
        pass


class CalculateStrategyFactory:

    @classmethod
    def get_strategies(cls, cart: "Cart") -> List[CalculateStrategy]:
        return [strategy() for strategy in CalculateStrategyFactory._get_classes() if strategy.is_applicable(cart)]
    
    @classmethod
    def _get_classes(cls) -> list[CalculateStrategy]:
        return [cls for cls in CalculateStrategy.__subclasses__() if isclass(cls) and not isabstract(cls)]