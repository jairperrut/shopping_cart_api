from fastapi.testclient import TestClient

from src.core.cart.domain.cart import Cart
from src.core.cart.domain.cart_item import CartItem
from src.core.cart.domain.customer import CustomerType
from src.core.product.domain.product import Product

class TestAddItem:

    def test_add_item_to_cart(self, client: TestClient, mock_cart_repository, mock_product_repository, mock_product_a: Product):
        mock_cart_repository(Cart(CustomerType.COMMON))
        mock_product_repository()

        response = client.post(
            "/v1/cart/items",
            json={"product_name": mock_product_a.name}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["cart"]["items"][0]["product"]["name"] == mock_product_a.name
        assert data["cart"]["items"][0]["product"]["price"] == mock_product_a.price
        assert data["cart"]["items"][0]["quantity"] == 1
        assert data["best_deal"]["strategy_name"] == "Full price"
        assert data["best_deal"]["total"] == 10.0

    def test_add_same_item_to_cart(self, client: TestClient, mock_cart_repository, mock_product_repository, mock_product_a: Product):
        mock_cart_repository(Cart(items=[CartItem(product=mock_product_a, quantity=1)]))
        mock_product_repository()

        response = client.post(
            "/v1/cart/items",
            json={"product_name": mock_product_a.name}
        )
        assert response.status_code == 200
        data = response.json()

        assert data["cart"]["items"][0]["product"]["name"] == mock_product_a.name
        assert data["cart"]["items"][0]["product"]["price"] == mock_product_a.price
        assert data["cart"]["items"][0]["quantity"] == 2
        assert data["best_deal"]["strategy_name"] == "Full price"
        assert data["best_deal"]["total"] == 20.0


    def test_add_other_item_to_cart(self, client: TestClient, mock_cart_repository, mock_product_repository, mock_product_a: Product, mock_product_b: Product):
        mock_cart_repository(Cart(items=[CartItem(product=mock_product_a, quantity=1)]))
        mock_product_repository()

        response = client.post(
            "/v1/cart/items",
            json={"product_name": mock_product_b.name}
        )
        assert response.status_code == 200
        data = response.json()

        assert data["cart"]["items"][0]["product"]["name"] == mock_product_a.name
        assert data["cart"]["items"][0]["product"]["price"] == mock_product_a.price
        assert data["cart"]["items"][0]["quantity"] == 1
        assert data["cart"]["items"][1]["product"]["name"] == mock_product_b.name
        assert data["cart"]["items"][1]["product"]["price"] == mock_product_b.price
        assert data["cart"]["items"][1]["quantity"] == 1
        assert data["best_deal"]["strategy_name"] == "Full price"
        assert data["best_deal"]["total"] == 30.0

    def test_add_invalid_item_to_cart_return_400(self, client: TestClient, mock_product_repository):
        mock_product_repository()
        response = client.post(
            "/v1/cart/items",
            json={"product_name": "Invalid Product"}
        )
        assert response.status_code == 400
        assert response.json() == {'detail': "Product 'Invalid Product' not found."}

class TestScenarios:

    # Scenario 1
    def test_common_customer_Get_3_for_2_customer_pays_for_2_tshirts_and_1_is_free(
            self,
            client: TestClient,
            mock_cart_repository,
            mock_product_repository,
            mock_product_tshirt: Product
        ):
        mock_cart_repository(
            Cart(
                customer_type=CustomerType.COMMON,
                items=[
                    CartItem(product=mock_product_tshirt, quantity=2)
                ]
            )
        )
        mock_product_repository()

        response = client.post(
            "/v1/cart/items",
            json={"product_name": mock_product_tshirt.name}
        )
        assert response.status_code == 200
        data = response.json()

        assert data["cart"]["items"][0]["product"]["name"] == mock_product_tshirt.name
        assert data["cart"]["items"][0]["product"]["price"] == mock_product_tshirt.price
        assert data["cart"]["items"][0]["quantity"] == 3
        assert data["prices"][0]["strategy_name"] == "Full price"
        assert data["prices"][0]["total"] == 107.97
        assert data["prices"][1]["strategy_name"] == "Get 3 for 2"
        assert data["prices"][1]["total"] == 71.98
        assert data["best_deal"]["strategy_name"] == "Get 3 for 2"
        assert data["best_deal"]["total"] == 71.98

    # Scenario 2
    def test_common_customer_Get_3_for_2_customer_buys_2_tshirts_and_2_jeans__1_tshirt_is_free(
        self,
        client: TestClient,
        mock_cart_repository,
        mock_product_repository,
        mock_product_tshirt: Product,
        mock_product_jeans: Product
    ):
        mock_cart_repository(
            Cart(
                customer_type=CustomerType.COMMON,
                items=[
                    CartItem(product=mock_product_tshirt, quantity=2),
                    CartItem(product=mock_product_jeans, quantity=1)
                ]
            )
        )
        mock_product_repository()

        response = client.post(
            "/v1/cart/items",
            json={"product_name": mock_product_jeans.name}
        )
        assert response.status_code == 200
        data = response.json()

        assert data["cart"]["items"][0]["product"]["name"] == mock_product_tshirt.name
        assert data["cart"]["items"][0]["product"]["price"] == mock_product_tshirt.price
        assert data["cart"]["items"][0]["quantity"] == 2
        assert data["cart"]["items"][1]["product"]["name"] == mock_product_jeans.name
        assert data["cart"]["items"][1]["product"]["price"] == mock_product_jeans.price
        assert data["cart"]["items"][1]["quantity"] == 2
        assert data["prices"][0]["strategy_name"] == "Full price"
        assert data["prices"][0]["total"] == 202.98
        assert data["prices"][1]["strategy_name"] == "Get 3 for 2"
        assert data["prices"][1]["total"] == 166.99
        assert data["best_deal"]["strategy_name"] == "Get 3 for 2"
        assert data["best_deal"]["total"] == 166.99

    # Scenario 3
    def test_vip_customer_buys_3_dresses_and_Get_3_for_2_is_the_best_deal(self, client, mock_cart_repository, mock_product_repository, mock_product_dress):
        mock_cart_repository(
            Cart(
                customer_type=CustomerType.VIP,
                items=[
                    CartItem(product=mock_product_dress, quantity=2)
                ]
            )
        )
        mock_product_repository()

        response = client.post(
            "/v1/cart/items",
            json={"product_name": mock_product_dress.name}
        )
        assert response.status_code == 200
        data = response.json()

        assert data["cart"]["items"][0]["product"]["name"] == mock_product_dress.name
        assert data["cart"]["items"][0]["product"]["price"] == mock_product_dress.price
        assert data["cart"]["items"][0]["quantity"] == 3
        assert data["prices"][0]["strategy_name"] == "Full price"
        assert data["prices"][0]["total"] == 242.25
        assert data["prices"][1]["strategy_name"] == "Get 3 for 2"
        assert data["prices"][1]["total"] == 161.5
        assert data["prices"][2]["strategy_name"] == "VIP Discount"
        assert data["prices"][2]["total"] == 205.91
        assert data["best_deal"]["strategy_name"] == "Get 3 for 2"
        assert data["best_deal"]["total"] == 161.5

    # Scenario 4
    def test_vip_customer_buys_2_jeans_and_2_dresses_Get_3_for_2_is_the_best_deal(self, client, mock_cart_repository, mock_product_repository, mock_product_dress, mock_product_jeans):
        mock_cart_repository(
            Cart(
                customer_type=CustomerType.VIP,
                items=[
                    CartItem(product=mock_product_dress, quantity=1),
                    CartItem(product=mock_product_jeans, quantity=2)
                ]
            )
        )
        mock_product_repository()

        response = client.post(
            "/v1/cart/items",
            json={"product_name": mock_product_dress.name}
        )
        assert response.status_code == 200
        data = response.json()

        assert data["cart"]["items"][0]["product"]["name"] == mock_product_dress.name
        assert data["cart"]["items"][0]["product"]["price"] == mock_product_dress.price
        assert data["cart"]["items"][0]["quantity"] == 2
        assert data["cart"]["items"][1]["product"]["name"] == mock_product_jeans.name
        assert data["cart"]["items"][1]["product"]["price"] == mock_product_jeans.price
        assert data["cart"]["items"][1]["quantity"] == 2
        assert data["prices"][0]["strategy_name"] == "Full price"
        assert data["prices"][0]["total"] == 292.5
        assert data["prices"][1]["strategy_name"] == "Get 3 for 2"
        assert data["prices"][1]["total"] == 227
        assert data["prices"][2]["strategy_name"] == "VIP Discount"
        assert data["prices"][2]["total"] == 248.62
        assert data["best_deal"]["strategy_name"] == "Get 3 for 2"
        assert data["best_deal"]["total"] == 227

    # Scenario 5
    def test_vip_customer_buys_4_tshirts_and_1_jeans_VIP_Discount_is_the_best_deal(self, client, mock_cart_repository, mock_product_repository, mock_product_tshirt, mock_product_jeans):
        mock_cart_repository(
            Cart(
                customer_type=CustomerType.VIP,
                items=[
                    CartItem(product=mock_product_tshirt, quantity=4),
                ]
            )
        )
        mock_product_repository()

        response = client.post(
            "/v1/cart/items",
            json={"product_name": mock_product_jeans.name}
        )
        assert response.status_code == 200
        data = response.json()

        assert data["cart"]["items"][0]["product"]["name"] == mock_product_tshirt.name
        assert data["cart"]["items"][0]["product"]["price"] == mock_product_tshirt.price
        assert data["cart"]["items"][0]["quantity"] == 4
        assert data["cart"]["items"][1]["product"]["name"] == mock_product_jeans.name
        assert data["cart"]["items"][1]["product"]["price"] == mock_product_jeans.price
        assert data["cart"]["items"][1]["quantity"] == 1
        assert data["prices"][0]["strategy_name"] == "Full price"
        assert data["prices"][0]["total"] == 209.46
        assert data["prices"][1]["strategy_name"] == "Get 3 for 2"
        assert data["prices"][1]["total"] == 173.47
        assert data["prices"][2]["strategy_name"] == "VIP Discount"
        assert data["prices"][2]["total"] == 178.04
        assert data["best_deal"]["strategy_name"] == "Get 3 for 2"
        assert data["best_deal"]["total"] == 173.47
