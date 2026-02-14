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
