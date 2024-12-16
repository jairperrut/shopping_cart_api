from src.core.cart.domain.cart import Cart
from src.core.cart.domain.customer import CustomerType
from src.core.cart.infrastructure.in_memory_cart_repository import InMemoryCartRepository


class TestInMemoryCartRepository:
    
    def test_get_cart_return_as_copy(self):
        repository = InMemoryCartRepository(Cart(customer_type=CustomerType.COMMON))
        data = repository.get_cart()
        data.customer_type = CustomerType.VIP
                       
        assert repository.get_cart().customer_type == CustomerType.COMMON
        
    def test_update_cart(self):
        repository = InMemoryCartRepository(Cart(customer_type=CustomerType.COMMON))
        repository.update_cart(Cart(customer_type=CustomerType.VIP))
                       
        assert repository.get_cart().customer_type == CustomerType.VIP