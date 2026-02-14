"""
Test Suite: Shopping Cart
Validates the OpenCart shopping cart functionality.
"""

import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@pytest.mark.cart
@pytest.mark.regression
class TestShoppingCart:
    """Tests for the shopping cart feature."""

    @pytest.mark.smoke
    def test_add_product_to_cart_from_home(self, home_page, base_url):
        """Verify a product can be added to cart from the home page."""
        hp = HomePage(home_page, base_url)
        hp.add_featured_product_to_cart(0)

        # Wait for success alert
        home_page.wait_for_selector(".alert-success", timeout=5000)
        assert hp.is_visible(".alert-success"), (
            "Success alert should appear after adding to cart"
        )

    def test_add_product_to_cart_from_product_page(self, home_page, base_url):
        """Verify a product can be added to cart from its detail page."""
        hp = HomePage(home_page, base_url)
        hp.search_product("MacBook")

        sp = SearchPage(home_page)
        sp.click_product(0)

        pp = ProductPage(home_page)
        pp.add_to_cart()

        home_page.wait_for_selector(".alert-success", timeout=5000)
        assert pp.is_success_alert_visible(), (
            "Success alert should appear after adding to cart"
        )

    def test_cart_displays_added_product(self, home_page, base_url):
        """Verify the cart page shows a product after it's added."""
        hp = HomePage(home_page, base_url)
        hp.search_product("MacBook")

        sp = SearchPage(home_page)
        sp.click_product(0)

        pp = ProductPage(home_page)
        product_name = pp.get_product_name()
        pp.add_to_cart()

        home_page.wait_for_selector(".alert-success", timeout=5000)

        cp = CartPage(home_page, base_url)
        cp.open()

        cart_products = cp.get_product_names()
        assert any(product_name.lower() in p.lower() for p in cart_products), (
            f"Cart should contain '{product_name}'"
        )

    def test_remove_product_from_cart(self, home_page, base_url):
        """Verify a product can be removed from the cart."""
        # Add a product first
        hp = HomePage(home_page, base_url)
        hp.add_featured_product_to_cart(0)
        home_page.wait_for_selector(".alert-success", timeout=5000)

        # Go to cart and remove
        cp = CartPage(home_page, base_url)
        cp.open()
        cp.remove_item(0)

        # Wait for page to reload
        home_page.wait_for_load_state("networkidle")

        assert cp.is_cart_empty(), "Cart should be empty after removing the item"

    def test_empty_cart_message(self, home_page, base_url):
        """Verify the empty cart shows appropriate message."""
        cp = CartPage(home_page, base_url)
        cp.open()

        assert cp.is_cart_empty(), "Cart should show empty message when no items"
