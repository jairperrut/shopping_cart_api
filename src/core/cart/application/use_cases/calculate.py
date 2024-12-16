from dataclasses import dataclass

from src.core.cart.application.calculate_strategies.base import CalculateStrategy, CalculateStrategyFactory
from src.core.cart.domain.cart import Cart


@dataclass(slots=True)
class CalculateCart:
    
    strategy_factory: CalculateStrategyFactory
    
    @dataclass(slots=True)
    class Output:
        prices: list[CalculateStrategy.Output]
        best_deal: CalculateStrategy.Output

    def execute(self, cart: Cart) -> "Output":
        strategies = self.strategy_factory.get_strategies(cart)
        results = []
        for strategy in strategies:
            results.append(strategy.execute(cart))
        
        best_deal = min(results, key=lambda x: x.total)
        return self.Output(
            prices=results,
            best_deal=best_deal
        )
