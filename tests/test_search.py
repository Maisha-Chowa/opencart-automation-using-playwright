"""
Test Suite: Product Search
Covers visibility checks and fully data-driven tests from search_data.csv.
"""

import time

import pytest
from pages.search_page import SearchPage
from utilities.csv_reader import read_csv

# ── Load CSV data once ──────────────────────────────────────────
SEARCH_CSV_DATA = read_csv("search_data.csv")

# Delay (seconds) after each search submission so you can visually inspect the result.
# Set to 0 when you no longer need visual debugging.
VISUAL_DELAY = 2


# ================================================================
# Visibility Tests (no CSV data needed)
# ================================================================
@pytest.mark.search
@pytest.mark.regression
class TestSearchPageVisibility:
    """Verify all search page elements are visible."""

    def test_all_search_form_elements_visible(self, page, base_url):
        """All search form elements should be visible."""
        sp = SearchPage(page, base_url)
        sp.open()
        sp.verify_all_search_form_elements_visible()

    def test_result_controls_visible_when_results_exist(self, page, base_url):
        """Sort, Limit, Grid, and List controls should be visible when results exist."""
        sp = SearchPage(page, base_url)
        sp.open_with_query("macbook")
        sp.verify_all_result_controls_visible()


# ================================================================
# Data-Driven Tests (all values from search_data.csv)
# ================================================================
@pytest.mark.search
@pytest.mark.regression
class TestSearchDataDriven:
    """Data-driven search tests — every scenario is defined in search_data.csv."""

    @pytest.mark.parametrize(
        "row",
        SEARCH_CSV_DATA,
        ids=[row["test_id"] for row in SEARCH_CSV_DATA],
    )
    def test_search_from_csv(self, page, base_url, row):
        """Run a single search test case from CSV."""
        sp = SearchPage(page, base_url)
        test_id = row["test_id"]
        keyword = row["search_keyword"]

        # ── Search from the home page header bar ──────────────
        sp.search_from_home(keyword)
        time.sleep(VISUAL_DELAY)

        # ── Assert ────────────────────────────────────────────
        if row["expected_result"] == "found":
            min_results = int(row["min_results"])
            actual_count = sp.get_search_results_count()
            assert actual_count >= min_results, (
                f"[{test_id}] Expected at least {min_results} results "
                f"for '{keyword}', got {actual_count}"
            )

            # Verify that expected product name appears in results
            expected_contains = row["expected_contains"]
            if expected_contains:
                result_names = sp.get_result_names()
                assert any(
                    expected_contains.lower() in name.lower()
                    for name in result_names
                ), (
                    f"[{test_id}] Expected a result containing "
                    f"'{expected_contains}', got: {result_names}"
                )

        else:
            # expected_result == "not_found"
            assert sp.has_no_results(), (
                f"[{test_id}] Search for '{keyword}' should show "
                f"'no product' message"
            )

            expected_message = row["expected_message"]
            if expected_message:
                actual_message = sp.get_no_results_message()
                assert expected_message.lower() in actual_message.lower(), (
                    f"[{test_id}] Expected message containing "
                    f"'{expected_message}', got: '{actual_message}'"
                )


# ================================================================
# Search Result Interaction Tests
# ================================================================
@pytest.mark.search
@pytest.mark.regression
class TestSearchResultInteraction:
    """Verify interactions with search results."""

    def test_search_result_product_link_navigates(self, page, base_url):
        """Clicking a product name in results should navigate to the product page."""
        sp = SearchPage(page, base_url)
        sp.search_from_home("macbook")
        sp.click_product(0)
        assert "product/product" in sp.get_url(), (
            "URL should contain 'product/product' after clicking a result"
        )

    def test_search_results_display_correct_product_details(self, page, base_url):
        """Each search result should display name, price, and image."""
        sp = SearchPage(page, base_url)
        sp.search_from_home("macbook")
        results_count = sp.get_search_results_count()
        assert results_count > 0, "Should have results to validate"

        names = sp.get_result_names()
        prices = sp.get_result_prices()
        images_count = sp.get_result_images_count()

        assert len(names) == results_count, "Each result should have a product name"
        assert len(prices) == results_count, "Each result should have a price"
        assert images_count == results_count, "Each result should have a product image"

    def test_search_heading_reflects_keyword(self, page, base_url):
        """The search page heading should reflect the searched keyword."""
        sp = SearchPage(page, base_url)
        sp.search_from_home("iphone")
        heading = sp.get_heading_text()
        assert "iphone" in heading.lower(), (
            f"Heading '{heading}' should contain the searched keyword 'iphone'"
        )

    def test_search_page_re_search(self, page, base_url):
        """Searching again from the search page should update results."""
        sp = SearchPage(page, base_url)
        sp.search_from_home("macbook")
        first_count = sp.get_search_results_count()
        assert first_count > 0, "Initial search should return results"

        # Re-search from the search page itself
        sp.search("iphone")
        second_names = sp.get_result_names()
        assert any("iphone" in n.lower() for n in second_names), (
            "Re-searching for 'iphone' should show iPhone in results"
        )
