from fastapi.testclient import TestClient

from src.core.cart.domain.customer import CustomerType
from src.core.cart.domain.cart import Cart
from src.core.cart.domain.cart_item import CartItem
from src.core.product.domain.product import Product


class TestRemoveItem:

    def test_delete_item_from_empty_cart(self, client: TestClient, mock_product_a: Product):
        response = client.request(
            method="DELETE",
            url="/v1/cart/items",
            json={"product_name": mock_product_a.name}
        )
        assert response.status_code == 200


    def test_delete_duplicated_item_from_cart(self, client: TestClient, mock_cart_repository, mock_product_a: Product):
        mock_cart_repository(Cart(items=[CartItem(product=mock_product_a, quantity=2)]))
        response = client.request(
            method="DELETE",
            url="/v1/cart/items",
            json={"product_name": mock_product_a.name}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["cart"]["items"][0]["product"]["name"] == mock_product_a.name
        assert data["cart"]["items"][0]["product"]["price"] == mock_product_a.price
        assert data["cart"]["items"][0]["quantity"] == 1
        assert data["best_deal"]["strategy_name"] == "Full price"
        assert data["best_deal"]["total"] == 10.0


    def test_remove_item_from_cart(self, client: TestClient, mock_cart_repository, mock_product_a: Product, mock_product_b: Product):
        mock_cart_repository(
            Cart(
                customer_type=CustomerType.COMMON,
                items=[
                    CartItem(product=mock_product_a, quantity=2),
                    CartItem(product=mock_product_b, quantity=1)
                ]
            )
        )
        response = client.request(
            method="DELETE",
            url="/v1/cart/items",
            json={"product_name": mock_product_b.name}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["cart"]["items"]) == 1
        assert data["cart"]["items"][0]["product"]["name"] == mock_product_a.name
        assert data["cart"]["items"][0]["product"]["price"] == mock_product_a.price
        assert data["cart"]["items"][0]["quantity"] == 2
        assert data["best_deal"]["strategy_name"] == "Full price"
        assert data["best_deal"]["total"] == 20.0

    def test_add_invalid_item_to_cart_return_400(self, client: TestClient):
        response = client.post(
            "/v1/cart/items",
            json={"product_name": "Invalid Product"}
        )
        assert response.status_code == 400
        assert response.json() == {'detail': "Product 'Invalid Product' not found."}
