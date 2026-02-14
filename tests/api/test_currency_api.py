"""
API Monitor: Currency Change
Monitors the API call triggered when the user changes the store currency
through the UI dropdown, then verifies prices update accordingly.
"""

import pytest
from pages.home_page import HomePage


@pytest.mark.ui
@pytest.mark.regression
class TestCurrencyApi:
    """Monitor currency-related API calls during UI interactions."""

    def test_currency_change_fires_api_call(self, home_page, base_url):
        """
        UI: Click the currency dropdown and switch to Euro.
        API: Intercept the POST to common/currency|save and verify response.
        UI: Verify the page reloads with Euro (EUR) symbol in prices.
        """
        hp = HomePage(home_page, base_url)

        # Capture original price symbol
        original_content = home_page.content()
        assert "$" in original_content, "Default currency should be USD ($)"

        # Click the currency dropdown and select Euro
        home_page.click("#form-currency .dropdown-toggle")
        home_page.wait_for_selector("#form-currency .dropdown-menu", state="visible")

        with home_page.expect_response(
            lambda r: "currency" in r.url
        ) as response_info:
            home_page.click("#form-currency a[href='EUR']")

        response = response_info.value

        # API assertions
        assert response.status in (200, 302), (
            f"Currency change API should return 200 or 302, got {response.status}"
        )

        # UI assertion -- wait for reload and check the symbol changed
        home_page.wait_for_load_state("networkidle")

        new_content = home_page.content()
        assert "€" in new_content, (
            "Page should display Euro symbol (€) after switching currency"
        )

    def test_currency_change_updates_product_prices(self, home_page, base_url):
        """
        UI: Record featured product prices in USD, switch to GBP.
        API: Verify the currency API call succeeds.
        UI: Verify prices now display the Pound (GBP) symbol.
        """
        hp = HomePage(home_page, base_url)

        # Get original prices in USD
        original_prices = home_page.locator(".product-thumb .price").all_text_contents()
        assert len(original_prices) > 0, "Should have product prices"
        assert any("$" in p for p in original_prices), "Prices should be in USD"

        # Switch to GBP
        home_page.click("#form-currency .dropdown-toggle")
        home_page.wait_for_selector("#form-currency .dropdown-menu", state="visible")

        with home_page.expect_response(
            lambda r: "currency" in r.url
        ) as response_info:
            home_page.click("#form-currency a[href='GBP']")

        response = response_info.value
        assert response.status in (200, 302), "Currency API should succeed"

        home_page.wait_for_load_state("networkidle")

        # UI assertion -- prices should now use pound symbol
        new_prices = home_page.locator(".product-thumb .price").all_text_contents()
        assert any("£" in p for p in new_prices), (
            f"Prices should display Pound (£) after currency change, got: {new_prices}"
        )
