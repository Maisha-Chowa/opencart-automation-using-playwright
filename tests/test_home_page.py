"""
Test Suite: Home Page

Strategy: Test the *template* (structure & interactions), not every individual element.
Exception: Featured products section verifies the query that pulls them isn't broken.

Sections: Navbar (3), Slider (2), Featured (4) = 9 tests total.
"""

import pytest
from pages.home_page import HomePage, EXPECTED_FEATURED_PRODUCTS


# ================================================================
# Navbar — template structure & interaction
# ================================================================
@pytest.mark.smoke
@pytest.mark.ui
class TestHomePageNavbar:
    """Verify navbar template renders correctly and is interactive."""

    def test_all_navbar_elements_visible(self, page, base_url):
        """Aggregate: navbar container and all 8 category links should be visible."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_all_navbar_elements_visible()

    def test_navbar_dropdown_opens_on_hover(self, page, base_url):
        """Hovering a category with sub-items should open its dropdown."""
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


# ================================================================
# Slider — template structure & carousel control
# ================================================================
@pytest.mark.smoke
@pytest.mark.ui
class TestHomePageSlider:
    """Verify slider template renders and carousel controls work."""

    def test_all_slider_elements_visible(self, page, base_url):
        """Aggregate: carousel, images, controls, and indicators should be present."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_all_slider_elements_visible()

    def test_slider_controls_advance_slide(self, page, base_url):
        """Carousel should support slide transitions (template functionality)."""
        import re
        from playwright.sync_api import expect

        hp = HomePage(page, base_url)
        hp.open()

        # Use Bootstrap API: pause auto-rotation, go to slide 0, then advance
        page.evaluate("""(() => {
            const el = document.querySelector('#carousel-banner-0');
            const c = bootstrap.Carousel.getOrCreateInstance(el);
            c.pause();
            c.to(0);
        })()""")
        page.wait_for_timeout(1000)

        page.evaluate("""(() => {
            const el = document.querySelector('#carousel-banner-0');
            bootstrap.Carousel.getInstance(el).next();
        })()""")

        second_slide = page.locator(
            "#carousel-banner-0 .carousel-item:nth-child(2)"
        )
        expect(second_slide).to_have_class(
            re.compile(r"active"), timeout=5000
        )


# ================================================================
# Featured Section — the exception: verify the query & card template
# ================================================================
@pytest.mark.smoke
@pytest.mark.ui
class TestHomePageFeatured:
    """Featured section verifies the query that pulls the 4 products.

    This is the exception to 'test the template': we check that the
    correct products are returned and each card has the expected elements.
    """

    def test_featured_section_has_four_products(self, page, base_url):
        """There should be exactly 4 featured product cards."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_featured_products_visible()

    def test_featured_product_names_match_expected(self, page, base_url):
        """Featured product names should match the expected list (query integrity)."""
        hp = HomePage(page, base_url)
        hp.open()
        names = hp.get_featured_product_names()
        assert names == EXPECTED_FEATURED_PRODUCTS, (
            f"Expected products {EXPECTED_FEATURED_PRODUCTS}, got {names}"
        )

    def test_featured_card_template_has_all_elements(self, page, base_url):
        """Each card should have image, name, price, and action buttons."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.verify_featured_product_images_visible()
        hp.verify_featured_product_names_visible()
        hp.verify_featured_product_prices_visible()
        hp.verify_featured_add_to_cart_buttons_visible()

    def test_featured_product_link_navigates(self, page, base_url):
        """Clicking a featured product should navigate to its product page."""
        hp = HomePage(page, base_url)
        hp.open()
        hp.click_featured_product(0)
        assert "product/product" in hp.get_url(), (
            "URL should contain 'product/product' after clicking a featured product"
        )
