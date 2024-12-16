import pytest

from src.core.cart.application.calculate_strategies.get_3_for_2_strategy import Get3For2CalculateStrategy
from src.core.cart.domain.cart import Cart, CartItem
from src.core.product.domain.product import Product

@pytest.fixture
def mock_products() -> list[Product]:
    return [
        Product(name="T-shirt", price=35.99),
        Product(name="Jeans", price=65.50),
        Product(name="Dress", price=80.75),
    ]

class TestGet3For2CalculateStrategy:
    
    def test_is_applicable_for_cart_with_fewer_than_three_items(self):
        cart = Cart(items=[
            CartItem(product=Product(name="T-shirt", price=35.99), quantity=2),
        ])
        assert not Get3For2CalculateStrategy.is_applicable(cart)

    def test_is_applicable_for_cart_with_three_or_more_items(self):
        cart = Cart(items=[
            CartItem(product=Product(name="T-shirt", price=35.99), quantity=3),
        ])
        assert Get3For2CalculateStrategy.is_applicable(cart)

    def test_calculate_cart_with_no_items(self):
        cart = Cart(items=[])
        strategy = Get3For2CalculateStrategy()
        result = strategy.execute(cart)
        assert result.strategy_name == "Get 3 for 2"
        assert result.total == 0.0

    def test_calculate_cart_with_exactly_three_items(self, mock_products: list[Product]):
        cart = Cart(items=[
            CartItem(product=mock_products[0], quantity=1),
            CartItem(product=mock_products[1], quantity=1),
            CartItem(product=mock_products[2], quantity=1),
        ])
        strategy = Get3For2CalculateStrategy()
        result = strategy.execute(cart)

        assert result.strategy_name == "Get 3 for 2"
        assert result.total == 146.25

    def test_calculate_cart_with_six_items(self, mock_products: list[Product]):
        cart = Cart(items=[
            CartItem(product=mock_products[0], quantity=2), 
            CartItem(product=mock_products[1], quantity=2), 
            CartItem(product=mock_products[2], quantity=2), 
        ])
        strategy = Get3For2CalculateStrategy()
        result = strategy.execute(cart)
        
        assert result.strategy_name == "Get 3 for 2"
        assert result.total == 292.5
