"""
API Monitor: Cart Operations
Monitors the AJAX calls fired when adding, updating, and removing cart items
through the UI, then asserts on both the API response and the UI state.
"""

import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@pytest.mark.regression
class TestCartApi:
    """Monitor cart-related API calls during UI interactions."""

    @pytest.mark.smoke
    def test_add_to_cart_api_response(self, home_page, base_url):
        """
        UI: Click 'Add to Cart' on a featured product.
        API: Intercept the POST to checkout/cart|add and verify JSON success.
        """
        hp = HomePage(home_page, base_url)

        with home_page.expect_response(
            lambda r: "cart" in r.url and r.request.method == "POST"
        ) as response_info:
            hp.add_featured_product_to_cart(0)

        response = response_info.value

        # API assertions
        assert response.status == 200, (
            f"Cart add API should return 200, got {response.status}"
        )
        body = response.json()
        assert "success" in body, (
            f"Cart add API response should contain 'success' key, got: {body}"
        )
        assert "shopping cart" in body["success"].lower(), (
            "Success message should reference shopping cart"
        )

        # UI assertion
        home_page.wait_for_selector(".alert-success", timeout=5000)
        assert hp.is_visible(".alert-success"), (
            "Success alert should be visible in the UI after adding to cart"
        )

    def test_add_to_cart_from_product_page_api(self, home_page, base_url):
        """
        UI: Navigate to a product page and click 'Add to Cart'.
        API: Intercept the POST and verify the correct product was added.
        """
        hp = HomePage(home_page, base_url)
        hp.search_product("MacBook")

        sp = SearchPage(home_page)
        sp.click_product(0)
        home_page.wait_for_load_state("networkidle")

        pp = ProductPage(home_page)
        product_name = pp.get_product_name()

        with home_page.expect_response(
            lambda r: "cart" in r.url and r.request.method == "POST"
        ) as response_info:
            pp.add_to_cart()

        response = response_info.value

        # API assertions
        assert response.status == 200, (
            f"Cart add API should return 200, got {response.status}"
        )
        body = response.json()
        assert "success" in body, "API should return success after adding product"

        # Verify the product name appears in the success message
        assert product_name.lower() in body["success"].lower(), (
            f"API success message should mention '{product_name}'"
        )

        # UI assertion
        home_page.wait_for_selector(".alert-success", timeout=5000)
        assert pp.is_success_alert_visible(), "UI should show success alert"

    def test_remove_from_cart_api_response(self, home_page, base_url):
        """
        UI: Add a product, navigate to cart, click 'Remove'.
        API: Intercept the remove POST and verify the response.
        """
        hp = HomePage(home_page, base_url)
        hp.add_featured_product_to_cart(0)
        home_page.wait_for_selector(".alert-success", timeout=5000)

        cp = CartPage(home_page, base_url)
        cp.open()

        assert cp.get_cart_items_count() > 0, "Cart should have items before removal"

        # Click remove and monitor the API call
        with home_page.expect_response(
            lambda r: "cart" in r.url and r.request.method == "POST"
        ) as response_info:
            cp.remove_item(0)

        response = response_info.value

        # API assertion
        assert response.status == 200, (
            f"Cart remove API should return 200, got {response.status}"
        )

        # UI assertion -- cart should be empty after reload
        home_page.wait_for_load_state("networkidle")
        cp.open()
        assert cp.is_cart_empty(), "Cart should be empty in the UI after removal"
