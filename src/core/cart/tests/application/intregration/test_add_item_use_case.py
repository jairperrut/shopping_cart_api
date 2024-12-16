
import pytest

from src.core.cart.application.use_cases.add_item import AddItemToCart
from src.core.cart.application.use_cases.remove_item import RemoveItemFromCart
from src.core.cart.domain.cart import Cart
from src.core.cart.domain.cart_item import CartItem
from src.core.cart.infrastructure.in_memory_cart_repository import InMemoryCartRepository
from src.core.product.application.exceptions import ProductNotFoundException
from src.core.product.domain.product import Product
from src.core.product.domain.product_repository import ProductRepository
from src.core.product.infrastructure.in_memory_product_repository import InMemoryProductRepository


@pytest.fixture
def mock_product_a() -> Product:
    return Product(name="Product A", price=10.0)

@pytest.fixture
def mock_product_b() -> Product:
    return Product(name="Product B", price=10.0)

@pytest.fixture
def mock_product_repository(mock_product_a: Product, mock_product_b: Product) -> ProductRepository:
    return InMemoryProductRepository(data=[mock_product_a, mock_product_b])


class TestAddCartItemUseCase:

    def test_add_item_to_empty_cart(self, mock_product_repository: ProductRepository, mock_product_a: Product):
        repository = InMemoryCartRepository(Cart(items=[]))
        use_case = AddItemToCart(
            repository=repository,
            product_repository=mock_product_repository
        )
        use_case.execute(mock_product_a.name)
        cart = repository.get_cart()
        assert cart.total_items == 1
        assert cart.items[0].product.name == mock_product_a.name
        assert cart.items[0].quantity == 1

    def test_add_same_item_to_cart(self, mock_product_repository: ProductRepository, mock_product_a: Product):
        repository = InMemoryCartRepository(Cart(items=[CartItem(product=mock_product_a, quantity=1)]))
        use_case = AddItemToCart(
            repository=repository,
            product_repository=mock_product_repository
        )
        use_case.execute(mock_product_a.name)
        cart = repository.get_cart()
        assert cart.total_items == 2
        assert cart.items[0].product.name == mock_product_a.name
        assert cart.items[0].quantity == 2

    def test_add_other_item_to_cart(self, mock_product_repository: ProductRepository, mock_product_a: Product, mock_product_b: Product):
        repository = InMemoryCartRepository(Cart(items=[CartItem(product=mock_product_a, quantity=2)]))
        use_case = AddItemToCart(
            repository=repository,
            product_repository=mock_product_repository
        )
        use_case.execute(mock_product_b.name)
        cart = repository.get_cart()
        assert cart.total_items == 3
        assert cart.items[0].product.name == mock_product_a.name
        assert cart.items[0].quantity == 2

        assert cart.items[1].product.name == mock_product_b.name
        assert cart.items[1].quantity == 1

    def test_add_invalid_item_to_cart(self, mock_product_repository: ProductRepository):
        repository = InMemoryCartRepository()
        with pytest.raises(ProductNotFoundException, match="Product 'Invalid Product' not found."):
            use_case = AddItemToCart(
                repository=repository,
                product_repository=mock_product_repository
            )
            use_case.execute("Invalid Product")
        

class TestRemoveCartItemUseCase:

    def test_remove_duplicated_item_from_cart(self, mock_product_a: Product):
        repository = InMemoryCartRepository(Cart(items=[CartItem(product=mock_product_a, quantity=2)]))
        RemoveItemFromCart(repository).execute(mock_product_a.name)
        cart = repository.get_cart()
        assert cart.total_items == 1
        assert cart.items[0].product.name == mock_product_a.name
        assert cart.items[0].quantity == 1

    def test_remove_item_turning_cart_empty(self, mock_product_a: Product):
        repository = InMemoryCartRepository(Cart(items=[CartItem(product=mock_product_a, quantity=1)]))
        RemoveItemFromCart(repository).execute(mock_product_a.name)
        cart = repository.get_cart()
        assert cart.total_items == 0
        
    def test_remove_product_not_in_cart(self, mock_product_a: Product):
        repository = InMemoryCartRepository()
        RemoveItemFromCart(repository).execute(mock_product_a.name)
        cart = repository.get_cart()
        assert cart.total_items == 0
