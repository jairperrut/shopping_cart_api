from abc import ABC, abstractmethod

from src.core.cart.domain.cart import Cart

class CartRepository(ABC):

    @abstractmethod
    def get_cart(self) -> Cart:
        pass

    @abstractmethod
    def update_cart(self, item: Cart) -> None:
        pass
