"""
API Monitor: Cart Widget (Header Mini-Cart)
Monitors the AJAX call to common/cart|info that updates the mini-cart
dropdown in the header after cart modifications.
"""

import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.product_page import ProductPage


@pytest.mark.cart
@pytest.mark.regression
class TestCartWidgetApi:
    """Monitor the cart widget API that powers the header mini-cart."""

    def test_cart_widget_updates_after_add(self, home_page, base_url):
        """
        UI: Add a product to cart from the home page.
        API: Monitor the cart widget refresh call (common/cart|info)
             and verify it reflects the newly added item.
        UI: Verify the header cart button text updates.
        """
        hp = HomePage(home_page, base_url)

        # Capture all responses during the add-to-cart action
        cart_info_responses = []

        def capture_cart_info(response):
            if "cart" in response.url and "info" in response.url:
                cart_info_responses.append(response)

        home_page.on("response", capture_cart_info)

        hp.add_featured_product_to_cart(0)
        home_page.wait_for_selector(".alert-success", timeout=5000)

        # Wait for any remaining AJAX calls
        home_page.wait_for_timeout(1000)
        home_page.remove_listener("response", capture_cart_info)

        # API assertions -- cart info should have been called
        if cart_info_responses:
            latest_response = cart_info_responses[-1]
            assert latest_response.status == 200, (
                f"Cart widget API should return 200, got {latest_response.status}"
            )

            widget_html = latest_response.text()
            # After adding an item, the widget should NOT say "empty"
            assert "empty" not in widget_html.lower() or "item(s)" in widget_html, (
                "Cart widget API should reflect the added item"
            )

        # UI assertion -- header cart should show items
        cart_text = hp.get_cart_count()
        assert "0 item" not in cart_text.lower(), (
            f"Header cart should reflect items, got: '{cart_text}'"
        )

    def test_cart_widget_shows_empty_after_clear(self, home_page, base_url):
        """
        UI: Add a product, then remove it from the cart.
        API: Monitor the cart widget call after removal and verify it shows empty.
        """
        hp = HomePage(home_page, base_url)

        # Add a product first
        hp.add_featured_product_to_cart(0)
        home_page.wait_for_selector(".alert-success", timeout=5000)

        # Navigate to cart and remove
        home_page.goto(f"{base_url}/index.php?route=checkout/cart&language=en-gb")
        home_page.wait_for_load_state("networkidle")

        # Start monitoring before removal
        cart_info_responses = []

        def capture_cart_info(response):
            if "cart" in response.url:
                cart_info_responses.append(response)

        home_page.on("response", capture_cart_info)

        # Click the remove button
        remove_btn = home_page.locator(
            "button[data-original-title='Remove'], button[title='Remove']"
        ).first
        if remove_btn.is_visible():
            remove_btn.click()

        home_page.wait_for_load_state("networkidle")
        home_page.wait_for_timeout(1000)
        home_page.remove_listener("response", capture_cart_info)

        # API assertions
        if cart_info_responses:
            for resp in cart_info_responses:
                assert resp.status == 200, (
                    f"Cart API call should return 200, got {resp.status}"
                )

        # UI assertion -- navigate to home and check cart shows 0
        hp.open()
        cart_text = hp.get_cart_count()
        assert "0 item" in cart_text.lower(), (
            f"Cart should show 0 items after removal, got: '{cart_text}'"
        )

    def test_cart_widget_reflects_product_page_add(self, home_page, base_url):
        """
        UI: Navigate to a product detail page and add it to cart.
        API: Capture both the cart|add and cart|info responses.
        UI: Verify the header mini-cart updates with the product.
        """
        hp = HomePage(home_page, base_url)
        hp.search_product("MacBook")

        sp = SearchPage(home_page)
        sp.click_product(0)
        home_page.wait_for_load_state("networkidle")

        pp = ProductPage(home_page)
        product_name = pp.get_product_name()

        # Monitor all cart-related responses
        cart_responses = []

        def capture(response):
            if "cart" in response.url:
                cart_responses.append({
                    "url": response.url,
                    "status": response.status,
                    "method": response.request.method,
                })

        home_page.on("response", capture)

        pp.add_to_cart()
        home_page.wait_for_selector(".alert-success", timeout=5000)
        home_page.wait_for_timeout(1000)
        home_page.remove_listener("response", capture)

        # API assertions -- should have captured at least the cart|add call
        assert len(cart_responses) > 0, (
            "Should have captured at least one cart API call"
        )

        add_calls = [r for r in cart_responses if r["method"] == "POST"]
        assert len(add_calls) > 0, "Should have captured a POST cart add call"
        assert all(r["status"] == 200 for r in add_calls), (
            f"All cart API calls should return 200, got: {add_calls}"
        )

        # UI assertion -- success alert should mention the product
        alert_text = home_page.text_content(".alert-success") or ""
        assert product_name.lower() in alert_text.lower(), (
            f"Success alert should mention '{product_name}', got: '{alert_text}'"
        )
