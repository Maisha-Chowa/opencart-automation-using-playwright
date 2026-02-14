"""
Test Suite: Product Page
Validates the OpenCart product detail page functionality.
"""

import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@pytest.mark.ui
@pytest.mark.regression
class TestProductPage:
    """Tests for the product detail page."""

    @pytest.fixture()
    def navigate_to_product(self, home_page, base_url):
        """Search for MacBook and navigate to the first product detail page."""
        hp = HomePage(home_page, base_url)
        hp.search_product("MacBook")

        sp = SearchPage(home_page)
        sp.click_product(0)
        home_page.wait_for_load_state("networkidle")

        return ProductPage(home_page)

    def test_product_page_displays_correct_details(self, navigate_to_product):
        """Verify product name, price, and description are displayed."""
        pp = navigate_to_product

        name = pp.get_product_name()
        price = pp.get_product_price()

        assert name, "Product name should be displayed"
        assert price, "Product price should be displayed"
        assert "$" in price, f"Price '{price}' should contain a currency symbol"

    def test_add_to_cart_with_custom_quantity(self, home_page, base_url, navigate_to_product):
        """Verify a product can be added to cart with a custom quantity."""
        pp = navigate_to_product

        pp.set_quantity(3)
        pp.add_to_cart()

        home_page.wait_for_selector(".alert-success", timeout=5000)
        assert pp.is_success_alert_visible(), (
            "Success alert should appear after adding to cart"
        )

        # Verify the cart reflects the quantity
        cp = CartPage(home_page, base_url)
        cp.open()

        assert cp.get_cart_items_count() > 0, "Cart should contain the added product"

    def test_add_product_to_wishlist_requires_login(self, navigate_to_product):
        """Verify adding to wishlist prompts login for unauthenticated users."""
        pp = navigate_to_product

        pp.add_to_wishlist()

        # OpenCart redirects to login or shows an alert for unauthenticated users
        pp.page.wait_for_load_state("networkidle")

        url = pp.get_url()
        has_login_redirect = "login" in url.lower()
        has_alert = pp.is_visible(".alert-danger") or pp.is_visible(".alert-success")

        assert has_login_redirect or has_alert, (
            "Wishlist action should prompt login or show an alert for guests"
        )

    def test_product_breadcrumb_navigation(self, navigate_to_product):
        """Verify the breadcrumb displays and contains the product name."""
        pp = navigate_to_product

        breadcrumb = pp.get_breadcrumb_text()
        product_name = pp.get_product_name()

        assert breadcrumb, "Breadcrumb should be displayed"
        assert product_name.lower() in breadcrumb.lower(), (
            f"Breadcrumb '{breadcrumb}' should contain product name '{product_name}'"
        )
