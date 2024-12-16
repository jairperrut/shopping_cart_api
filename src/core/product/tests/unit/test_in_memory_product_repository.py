from src.core.product.domain.product import Product
from src.core.product.infrastructure.in_memory_product_repository import InMemoryProductRepository


class TestInMemoryProductRepository:
    
    def test_get_by_name_return_none_when_not_found(self):
        repository = InMemoryProductRepository()
        data = repository.get_by_name("Test")
        
        assert data is None
    
    def test_get_by_name_return_as_copy(self):
        repository = InMemoryProductRepository([Product("Test", 10)])
        data = repository.get_by_name("Test")
        data.price = 50
                       
        assert repository.get_by_name("Test").price == 10
        
    def test_list_return_as_copy(self):
        repository = InMemoryProductRepository()
        data = repository.list()
        data.append(Product("Test", 10))
        
        assert len(repository.list()) == 0
        
