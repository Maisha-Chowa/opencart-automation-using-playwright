"""
API Monitor: Wishlist Operations
Monitors the API call triggered when a user tries to add a product to the
wishlist, verifying authentication requirements and success responses.
"""

import time

import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utilities.test_data import generate_unique_email


@pytest.mark.account
@pytest.mark.regression
class TestWishlistApi:
    """Monitor wishlist-related API calls during UI interactions."""

    def test_wishlist_add_requires_login(self, home_page, base_url):
        """
        UI: As a guest, navigate to a product and click 'Add to Wishlist'.
        API: Intercept the response and verify it indicates login is required.
        """
        hp = HomePage(home_page, base_url)
        hp.search_product("MacBook")

        sp = SearchPage(home_page)
        sp.click_product(0)
        home_page.wait_for_load_state("networkidle")

        pp = ProductPage(home_page)

        # Collect responses triggered by the wishlist click
        captured_responses = []

        def capture(response):
            if "wishlist" in response.url:
                captured_responses.append(response)

        home_page.on("response", capture)
        pp.add_to_wishlist()

        # Give the AJAX call time to complete
        home_page.wait_for_timeout(2000)
        home_page.remove_listener("response", capture)

        # Check: either we got an API response requiring login, or the UI redirected
        url = pp.get_url()
        if captured_responses:
            resp_text = captured_responses[0].text()
            assert (
                "login" in resp_text.lower()
                or captured_responses[0].status in (302, 403)
            ), "Wishlist API should require login for guest users"
        else:
            # If no AJAX response, the page likely redirected to login
            assert "login" in url.lower(), (
                "Should redirect to login page when guest adds to wishlist"
            )

    def test_wishlist_add_succeeds_for_logged_in_user(self, page, base_url):
        """
        UI: Register a user, log in, navigate to a product, click 'Add to Wishlist'.
        API: Intercept the response and verify it returns success.
        """
        # Register a fresh user
        rp = RegisterPage(page, base_url)
        rp.open()

        email = generate_unique_email("wishlist_test")
        password = "Test@1234"

        rp.register(
            first_name="Wishlist",
            last_name="Tester",
            email=email,
            password=password,
            agree_privacy=True,
        )
        page.wait_for_load_state("networkidle")

        # Navigate to a product
        hp = HomePage(page, base_url)
        hp.open()
        hp.search_product("MacBook")

        sp = SearchPage(page)
        sp.click_product(0)
        page.wait_for_load_state("networkidle")

        pp = ProductPage(page)

        # Click wishlist and monitor response
        captured_responses = []

        def capture(response):
            if "wishlist" in response.url:
                captured_responses.append(response)

        page.on("response", capture)
        pp.add_to_wishlist()

        page.wait_for_timeout(2000)
        page.remove_listener("response", capture)

        # API assertion -- should succeed for authenticated user
        if captured_responses:
            resp = captured_responses[0]
            assert resp.status == 200, (
                f"Wishlist API should return 200 for logged-in user, got {resp.status}"
            )
            resp_text = resp.text()
            assert "success" in resp_text.lower() or "login" not in resp_text.lower(), (
                "Wishlist API should return success for authenticated user"
            )

        # UI assertion -- check for success alert or wishlist count update
        has_success = pp.is_visible(".alert-success")
        wishlist_text = page.text_content("a#wishlist-total") or ""
        assert has_success or "1" in wishlist_text, (
            "UI should show success alert or update wishlist count"
        )
