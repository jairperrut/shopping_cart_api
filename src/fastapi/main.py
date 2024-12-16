from fastapi import FastAPI

from src.fastapi.v1.urls import router as v1_router

app = FastAPI(
    title="Shopping Cart API",
    description="API for managing a shopping cart with promotions and discounts",
    version="1.0.0",
    contact={
        "name": "Jair Perrut",
        "email": "jairperrut@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },)

app.include_router(v1_router)
