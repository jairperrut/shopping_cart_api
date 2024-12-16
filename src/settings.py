from pydantic_settings import BaseSettings

from src.core.cart.domain.customer import CustomerType

class Settings(BaseSettings):
    vip_discount: float = 0.15
    customer_type: CustomerType = CustomerType.COMMON

settings = Settings()
