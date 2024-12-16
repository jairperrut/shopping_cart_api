import pytest

from src.core.cart.domain.cart import Cart
from src.core.cart.domain.cart_item import CartItem
from src.core.product.domain.product import Product

@pytest.fixture
def mock_product() -> Product:
    return Product(name="Test Product", price=10.0)


class TestAddCartItem:

    def test_add_item_to_empty_cart(self, mock_product: Product):
        cart = Cart(items=[])
        cart.add_item(mock_product)
        assert len(cart.items) == 1
        assert cart.items[0].product.name == mock_product.name
        assert cart.items[0].quantity == 1

    def test_add_same_item_to_cart(self, mock_product: Product):
        cart = Cart(items=[CartItem(product=mock_product, quantity=1)])
        cart.add_item(mock_product)
        assert len(cart.items) == 1
        assert cart.items[0].product.name == mock_product.name
        assert cart.items[0].quantity == 2
    
    def test_add_other_item_to_cart(self, mock_product: Product):
        cart = Cart(items=[CartItem(product=mock_product, quantity=1)])
        new_product = Product("Other product", price=20.5)
        cart.add_item(new_product)
        assert len(cart.items) == 2
        
        assert cart.items[0].product.name == mock_product.name
        assert cart.items[0].quantity == 1
        
        assert cart.items[1].product.name == new_product.name
        assert cart.items[1].quantity == 1


class TestRemoveCartItem:
    
    def test_remove_duplicated_item_from_cart(self, mock_product: Product):
        cart = Cart(items=[CartItem(product=mock_product, quantity=2)])
        cart.remove_item(mock_product.name)
        assert len(cart.items) == 1
        assert cart.items[0].product.name == mock_product.name
        assert cart.items[0].quantity == 1

    def test_remove_item_turning_cart_empty(self, mock_product: Product):
        cart = Cart(items=[CartItem(product=mock_product, quantity=1)])
        cart.remove_item(mock_product.name)
        assert len(cart.items) == 0

    def test_remove_product_not_in_cart(self, mock_product: Product):
        cart = Cart(items=[])
        cart.remove_item(mock_product.name)
        assert len(cart.items) == 0
