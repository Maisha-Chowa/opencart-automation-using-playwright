"""
Test Suite: Home Page
Validates the OpenCart storefront home page — navbar, slider, and featured section.
"""

import time

import pytest
from pages.home_page import HomePage, EXPECTED_NAV_CATEGORIES, EXPECTED_FEATURED_PRODUCTS

# Delay (seconds) after carousel transitions so the animation completes.
SLIDE_TRANSITION_DELAY = 1


# ================================================================
# Navbar Visibility & Interaction Tests
# ================================================================
@pytest.mark.smoke
@pytest.mark.ui
class TestHomePageNavbar:
    """Verify navbar elements are visible and interactive."""

    def test_navbar_visible(self, page, base_url):
        """Navbar container should be visible on the home page."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_navbar_visible()

    def test_navbar_categories_visible(self, page, base_url):
        """All 8 top-level category links should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_navbar_categories_visible()

    def test_navbar_desktop_dropdown_opens(self, page, base_url):
        """Hovering 'Desktops' should open its dropdown with sub-categories."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_navbar_dropdown_opens("Desktops")

    def test_navbar_category_link_navigates(self, page, base_url):
        """Clicking a category link should navigate to the category page."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.click_navbar_category("Tablets")
        assert "product/category" in hp.get_url(), (
            "URL should contain 'product/category' after clicking a navbar link"
        )

    def test_all_navbar_elements_visible(self, page, base_url):
        """Aggregate: all navbar elements should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_all_navbar_elements_visible()


# ================================================================
# Slider / Carousel Visibility & Interaction Tests
# ================================================================
@pytest.mark.smoke
@pytest.mark.ui
class TestHomePageSlider:
    """Verify slider/carousel elements are visible and interactive."""

    def test_slider_visible(self, page, base_url):
        """Carousel banner container should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_slider_visible()

    def test_slider_has_two_images(self, page, base_url):
        """Carousel should contain exactly 2 banner images."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_slider_images_visible()

    def test_slider_controls_visible(self, page, base_url):
        """Previous and Next carousel controls should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_slider_controls_visible()

    def test_slider_indicators_visible(self, page, base_url):
        """Carousel should have exactly 2 indicator dots."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_slider_indicators_visible()

    def test_slider_next_button_changes_slide(self, page, base_url):
        """Clicking the Next button should advance to the second slide."""
        hp = HomePage(page, base_url)
        hp.open()
        initial = hp.get_active_slide_index()
        hp.click_slider_next()
        time.sleep(SLIDE_TRANSITION_DELAY)
        after = hp.get_active_slide_index()
        assert after != initial, (
            f"Active slide should change after clicking Next "
            f"(was {initial}, still {after})"
        )

    def test_slider_prev_button_changes_slide(self, page, base_url):
        """Clicking the Previous button should go back to the first slide."""
        hp = HomePage(page, base_url)
        hp.open()
        # Move to second slide first
        hp.click_slider_next()
        time.sleep(SLIDE_TRANSITION_DELAY)
        hp.click_slider_prev()
        time.sleep(SLIDE_TRANSITION_DELAY)
        assert hp.get_active_slide_index() == 0, (
            "Active slide should return to the first slide after clicking Prev"
        )

    def test_slider_indicator_changes_slide(self, page, base_url):
        """Clicking the second indicator dot should activate the second slide."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.click_slider_indicator(1)
        time.sleep(SLIDE_TRANSITION_DELAY)
        assert hp.get_active_slide_index() == 1, (
            "Clicking indicator 1 should activate the second slide"
        )

    def test_all_slider_elements_visible(self, page, base_url):
        """Aggregate: all slider elements should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_all_slider_elements_visible()


# ================================================================
# Featured Section Visibility & Interaction Tests
# ================================================================
@pytest.mark.smoke
@pytest.mark.ui
class TestHomePageFeatured:
    """Verify featured product section elements are visible and correct."""

    def test_featured_heading_visible(self, page, base_url):
        """'Featured' heading should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_featured_heading_visible()

    def test_featured_products_count(self, page, base_url):
        """There should be exactly 4 featured product cards."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_featured_products_visible()

    def test_featured_product_images_visible(self, page, base_url):
        """All 4 featured product images should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_featured_product_images_visible()

    def test_featured_product_names_visible(self, page, base_url):
        """All 4 featured product name links should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_featured_product_names_visible()

    def test_featured_product_names_correct(self, page, base_url):
        """Featured product names should match the expected product list."""
        hp = HomePage(page, base_url)
        hp.open()
        names = hp.get_featured_product_names()
        assert names == EXPECTED_FEATURED_PRODUCTS, (
            f"Expected products {EXPECTED_FEATURED_PRODUCTS}, got {names}"
        )

    def test_featured_product_prices_visible(self, page, base_url):
        """All 4 featured product prices should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_featured_product_prices_visible()

    def test_featured_add_to_cart_buttons_visible(self, page, base_url):
        """All 4 'Add to Cart' buttons should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_featured_add_to_cart_buttons_visible()

    def test_featured_wishlist_buttons_visible(self, page, base_url):
        """All 4 'Add to Wish List' buttons should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_featured_wishlist_buttons_visible()

    def test_featured_compare_buttons_visible(self, page, base_url):
        """All 4 'Compare this Product' buttons should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_featured_compare_buttons_visible()

    def test_featured_product_link_navigates(self, page, base_url):
        """Clicking a featured product name should navigate to the product page."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.click_featured_product(0)
        assert "product/product" in hp.get_url(), (
            "URL should contain 'product/product' after clicking a featured product"
        )


# ================================================================
# Aggregate Smoke Tests – All Sections
# ================================================================
@pytest.mark.smoke
@pytest.mark.ui
class TestHomePageAllElements:
    """Quick aggregate smoke tests for the entire home page."""

    def test_all_navbar_elements_visible(self, page, base_url):
        """All navbar elements should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_all_navbar_elements_visible()

    def test_all_slider_elements_visible(self, page, base_url):
        """All slider elements should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_all_slider_elements_visible()

    def test_all_featured_elements_visible(self, page, base_url):
        """All featured section elements should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_all_featured_elements_visible()
