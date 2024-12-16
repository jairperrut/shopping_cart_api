import pytest

from src.core.cart.application.calculate_strategies.vip_strategy import VIPCalculateStrategy
from src.core.product.domain.product import Product
from src.core.cart.domain.cart import Cart, CartItem
from src.core.cart.domain.customer import CustomerType

@pytest.fixture
def mock_products() -> list[Product]:
    return [
        Product(name="T-shirt", price=35.99),
        Product(name="Jeans", price=65.50),
        Product(name="Dress", price=80.75),
    ]

class TesteVIPCalculateStrategy:

    def test_is_applicable_for_vip_customer(self):
        cart = Cart(items=[], customer_type=CustomerType.VIP)
        assert VIPCalculateStrategy.is_applicable(cart)

    def test_is_not_applicable_for_common_customer(self):
        cart = Cart(items=[], customer_type=CustomerType.COMMON)
        assert not VIPCalculateStrategy.is_applicable(cart)

    def test_calculate_cart_with_vip_discount(self, mock_products: list[Product]):
        cart = Cart(
            customer_type=CustomerType.VIP,
            items=[
                CartItem(product=mock_products[0], quantity=1),
                CartItem(product=mock_products[1], quantity=1),
            ]
        )
        strategy = VIPCalculateStrategy(discount=0.15)
        result = strategy.execute(cart)
        assert result.strategy_name == "VIP Discount"
        assert result.total == 86.27

    def test_calculate_cart_without_items_for_vip_customer(self):
        cart = Cart(items=[], customer_type=CustomerType.VIP)
        strategy = VIPCalculateStrategy()
        result = strategy.execute(cart)
        assert result.strategy_name == "VIP Discount"
        assert result.total == 0.0
