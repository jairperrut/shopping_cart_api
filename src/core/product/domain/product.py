from dataclasses import dataclass


@dataclass(slots=True)
class Product:
    name: str
    price: float

    def __eq__(self, value: "Product") -> bool:
        return self.name == value.name