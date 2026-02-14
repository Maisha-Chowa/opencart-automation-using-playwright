"""
API Monitor: Product Search
Monitors the HTTP request/response when performing a search through the UI,
then validates both the network response and the displayed results.
"""

import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage


@pytest.mark.search
@pytest.mark.regression
class TestSearchApi:
    """Monitor search-related API calls during UI interactions."""

    def test_search_request_returns_200(self, home_page, base_url):
        """
        UI: Search for 'MacBook' using the search bar.
        API: Intercept the navigation request and verify status 200.
        """
        hp = HomePage(home_page, base_url)

        with home_page.expect_response(
            lambda r: "search" in r.url and r.status == 200
        ) as response_info:
            hp.search_product("MacBook")

        response = response_info.value

        # API assertions
        assert response.status == 200, (
            f"Search page should return 200, got {response.status}"
        )
        assert "text/html" in response.headers.get("content-type", ""), (
            "Search response should be HTML content"
        )

        # UI assertions
        sp = SearchPage(home_page)
        assert sp.get_search_results_count() > 0, "UI should display search results"

    def test_search_response_contains_product_data(self, home_page, base_url):
        """
        UI: Search for 'MacBook'.
        API: Verify the HTML response body contains product markup.
        UI: Verify the result count matches what's in the response.
        """
        hp = HomePage(home_page, base_url)

        with home_page.expect_response(
            lambda r: "search" in r.url and r.status == 200
        ) as response_info:
            hp.search_product("MacBook")

        response = response_info.value
        response_html = response.text()

        # API assertion -- response HTML should contain product-thumb elements
        api_product_count = response_html.count("product-thumb")
        assert api_product_count > 0, (
            "Search API response HTML should contain product-thumb elements"
        )

        # UI assertion -- browser display should match the response
        sp = SearchPage(home_page)
        ui_product_count = sp.get_search_results_count()

        assert api_product_count == ui_product_count, (
            f"API response has {api_product_count} products "
            f"but UI displays {ui_product_count}"
        )

    def test_empty_search_returns_no_products(self, home_page, base_url):
        """
        UI: Search for a non-existent product.
        API: Verify the response does not contain product-thumb elements.
        UI: Verify the 'no results' message is displayed.
        """
        hp = HomePage(home_page, base_url)

        with home_page.expect_response(
            lambda r: "search" in r.url and r.status == 200
        ) as response_info:
            hp.search_product("xyznonexistentproduct999")

        response = response_info.value
        response_html = response.text()

        # API assertion
        assert "product-thumb" not in response_html, (
            "API response should not contain products for non-existent search"
        )

        # UI assertion
        sp = SearchPage(home_page)
        assert sp.has_no_results(), "UI should display 'no results' message"
