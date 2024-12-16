from abc import ABC, abstractmethod

from src.core.cart.domain.cart import Product

class ProductRepository(ABC):
    
    @abstractmethod
    def get_by_name(self) -> Product:
        pass
