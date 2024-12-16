from dataclasses import dataclass, field

from src.core.product.domain.product import Product
from src.core.product.domain.product_repository import ProductRepository


@dataclass(slots=True)
class InMemoryProductRepository(ProductRepository):
    data: list[Product] = field(default_factory=lambda: [])

    def get_by_name(self, name: str) -> Product | None:
        for product in self.data:
            if product.name == name:
                return Product(
                    name=product.name,
                    price=product.price
                )
        return None

    def list(self) -> list[Product]:
        return self.data[:]