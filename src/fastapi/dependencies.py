from src.core.product.domain.product import Product
from src.core.product.infrastructure.in_memory_product_repository import InMemoryProductRepository
from src.core.cart.infrastructure.in_memory_cart_repository import InMemoryCartRepository


cart_repository = InMemoryCartRepository()
product_repository = InMemoryProductRepository(data=[
        Product(name="T-shirt", price=35.99),
        Product(name="Jeans", price=65.50),
        Product(name="Dress", price=80.75),
])

async def get_cart_repository():
    return cart_repository

async def get_product_repository():
    return product_repository
