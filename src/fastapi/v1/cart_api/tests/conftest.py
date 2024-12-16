from typing import Any, Callable, Generator, List

import pytest
from fastapi.testclient import TestClient

from src.core.cart.domain.cart import Cart
from src.core.cart.infrastructure.in_memory_cart_repository import InMemoryCartRepository
from src.core.product.domain.product import Product
from src.core.product.infrastructure.in_memory_product_repository import InMemoryProductRepository
from src.fastapi.dependencies import get_cart_repository, get_product_repository
from src.fastapi.main import app

@pytest.fixture
def mock_product_a() -> Product:
    return Product(name="Product A", price=10.0)

@pytest.fixture
def mock_product_b() -> Product:
    return Product(name="Product B", price=20.0)

@pytest.fixture
def mock_product_tshirt() -> Product:
    return Product(name="T-shirt", price=35.99)

@pytest.fixture
def mock_product_jeans() -> Product:
    return Product(name="Jeans", price=65.5)

@pytest.fixture
def mock_product_dress() -> Product:
    return Product(name="Dress", price=80.75)

@pytest.fixture
def mock_product_repository(client: TestClient, mock_product_a: Product, mock_product_b: Product, mock_product_tshirt: Product, mock_product_jeans: Product, mock_product_dress: Product) -> Callable[[List[Product]], None]:
    def create_repo(products: List[Product] = [mock_product_a, mock_product_b, mock_product_tshirt, mock_product_jeans, mock_product_dress]):
        client.app.dependency_overrides[get_product_repository] = lambda: InMemoryProductRepository(data=products)
    return create_repo

@pytest.fixture
def client() -> Generator[TestClient, Any, None]:
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_cart_repository(client: TestClient) -> Callable[[Cart], None]:
    def create_repo(cart: Cart) -> None:
        client.app.dependency_overrides[get_cart_repository] = lambda: InMemoryCartRepository(cart)
    return create_repo