"""
Test Suite: Home Page
Validates the OpenCart storefront home page functionality.
"""

import pytest
from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.ui
class TestHomePage:
    """Tests for the OpenCart home page."""

    def test_home_page_loads_successfully(self, home_page, base_url):
        """Verify the home page loads and displays the store logo."""
        hp = HomePage(home_page, base_url)
        assert hp.is_logo_visible(), "Store logo should be visible on home page"

    def test_page_title_contains_store_name(self, home_page, base_url):
        """Verify the page title contains the store name."""
        hp = HomePage(home_page, base_url)
        title = hp.get_title()
        assert "store" in title.lower() or "opencart" in title.lower(), (
            f"Page title '{title}' should contain the store name"
        )

    def test_featured_products_are_displayed(self, home_page, base_url):
        """Verify featured products are displayed on the home page."""
        hp = HomePage(home_page, base_url)
        products = hp.get_featured_products()
        assert len(products) > 0, "At least one featured product should be displayed"

    def test_search_functionality_from_home(self, home_page, base_url):
        """Verify the search bar works from the home page."""
        hp = HomePage(home_page, base_url)
        hp.search_product("mac")
        assert "search" in hp.get_url().lower(), (
            "URL should navigate to search results page"
        )

    def test_navigation_to_register_page(self, home_page, base_url):
        """Verify navigation to the registration page from My Account dropdown."""
        hp = HomePage(home_page, base_url)
        hp.click_register()
        assert "register" in hp.get_url().lower(), (
            "URL should navigate to register page"
        )

    def test_navigation_to_login_page(self, home_page, base_url):
        """Verify navigation to the login page from My Account dropdown."""
        hp = HomePage(home_page, base_url)
        hp.click_login()
        assert "login" in hp.get_url().lower(), "URL should navigate to login page"
