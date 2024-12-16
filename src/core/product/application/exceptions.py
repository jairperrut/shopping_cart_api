class ProductNotFoundException(Exception):
    
    def __init__(self, product_name: str):
        super().__init__(f"Product '{product_name}' not found.")