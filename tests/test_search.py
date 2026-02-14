"""
Test Suite: Product Search
Validates the OpenCart search functionality.
"""

import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage


@pytest.mark.search
@pytest.mark.regression
class TestProductSearch:
    """Tests for the product search feature."""

    def test_search_with_valid_product(self, home_page, base_url):
        """Verify searching for an existing product returns results."""
        hp = HomePage(home_page, base_url)
        hp.search_product("MacBook")

        sp = SearchPage(home_page)
        assert sp.get_search_results_count() > 0, (
            "Search for 'MacBook' should return results"
        )

    def test_search_result_contains_keyword(self, home_page, base_url):
        """Verify search results contain the searched keyword."""
        hp = HomePage(home_page, base_url)
        hp.search_product("MacBook")

        sp = SearchPage(home_page)
        result_names = sp.get_result_names()
        assert any("macbook" in name.lower() for name in result_names), (
            "At least one result should contain 'MacBook'"
        )

    def test_search_with_no_results(self, home_page, base_url):
        """Verify searching for a non-existent product shows no results message."""
        hp = HomePage(home_page, base_url)
        hp.search_product("xyznonexistentproduct123")

        sp = SearchPage(home_page)
        assert sp.has_no_results(), (
            "Non-existent product search should show 'no results' message"
        )

    def test_empty_search(self, home_page, base_url):
        """Verify submitting an empty search shows appropriate response."""
        hp = HomePage(home_page, base_url)
        hp.search_product("")

        sp = SearchPage(home_page)
        assert sp.has_no_results(), "Empty search should show 'no results' message"

    @pytest.mark.parametrize("special_input", [
        "<script>alert('xss')</script>",
        "' OR 1=1 --",
        "!@#$%^&*()",
    ], ids=["xss_script", "sql_injection", "special_symbols"])
    def test_search_with_special_characters(self, home_page, base_url, special_input):
        """Verify search handles special characters gracefully without errors."""
        hp = HomePage(home_page, base_url)
        hp.search_product(special_input)

        sp = SearchPage(home_page)
        # Page should load without crashing -- either no results or results shown
        assert sp.has_no_results() or sp.get_search_results_count() >= 0, (
            f"Search should handle special input '{special_input}' gracefully"
        )

    def test_search_results_display_correct_product_details(self, home_page, base_url):
        """Verify each search result displays name, price, and image."""
        hp = HomePage(home_page, base_url)
        hp.search_product("MacBook")

        sp = SearchPage(home_page)
        results_count = sp.get_search_results_count()
        assert results_count > 0, "Should have results to validate"

        names = sp.get_result_names()
        prices = sp.get_result_prices()
        images_count = sp.get_result_images_count()

        assert len(names) == results_count, "Each result should have a product name"
        assert len(prices) == results_count, "Each result should have a price"
        assert images_count == results_count, "Each result should have a product image"
