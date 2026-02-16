"""
HomePage - Page Object for the OpenCart storefront home page.

Covers three main sections:
  1. Navbar   – top-level category links with dropdown sub-menus
  2. Slider   – Bootstrap carousel with 2 banner images
  3. Featured – four product cards with images, names, prices, and action buttons
"""

from pages.base_page import BasePage
from playwright.sync_api import Page, expect


# ── Expected data (used for assertion helpers) ────────────────────
EXPECTED_NAV_CATEGORIES = [
    "Desktops",
    "Laptops & Notebooks",
    "Components",
    "Tablets",
    "Software",
    "Phones & PDAs",
    "Cameras",
    "MP3 Players",
]

EXPECTED_FEATURED_PRODUCTS = [
    "MacBook",
    "iPhone",
    "Apple Cinema 30\"",
    "Canon EOS 5D",
]


class HomePage(BasePage):
    """Page object for the OpenCart home page."""

    HOME_URL_PATH = "index.php?route=common/home&language=en-gb"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the home page."""
        self.navigate(self.base_url)

    def open_direct(self):
        """Navigate directly to the home page URL."""
        self.navigate(f"{self.base_url}{self.HOME_URL_PATH}")

    # ================================================================
    # Navbar – Visibility Checks
    # ================================================================

    def verify_navbar_visible(self):
        """Assert that the main navigation bar is visible."""
        expect(self.page.locator("nav#menu")).to_be_visible()

    def verify_navbar_categories_visible(self):
        """Assert that all 8 top-level category links are visible."""
        nav_links = self.page.locator(
            "nav#menu ul.nav.navbar-nav > li > a.nav-link"
        )
        expect(nav_links).to_have_count(len(EXPECTED_NAV_CATEGORIES))
        for category in EXPECTED_NAV_CATEGORIES:
            expect(
                self.page.locator(
                    "nav#menu ul.nav.navbar-nav > li > a.nav-link",
                    has_text=category,
                ).first
            ).to_be_visible()

    def verify_navbar_dropdown_opens(self, category: str = "Desktops"):
        """Assert that hovering a category opens its dropdown sub-menu."""
        parent_link = self.page.locator(
            "nav#menu a.nav-link.dropdown-toggle", has_text=category
        ).first
        parent_link.hover()
        dropdown = parent_link.locator("..").locator(".dropdown-menu")
        expect(dropdown).to_be_visible()

    def verify_all_navbar_elements_visible(self):
        """Assert that all navbar elements are visible (aggregate check)."""
        self.verify_navbar_visible()
        self.verify_navbar_categories_visible()

    # ── Navbar – Actions ──────────────────────────────────────────────

    def get_navbar_category_names(self) -> list[str]:
        """Return the text of all top-level navbar category links."""
        links = self.page.locator(
            "nav#menu ul.nav.navbar-nav > li > a.nav-link"
        ).all()
        return [(el.text_content() or "").strip() for el in links]

    def click_navbar_category(self, category: str):
        """Click a top-level navbar category link."""
        self.page.locator(
            "nav#menu a.nav-link", has_text=category
        ).first.click()
        self.page.wait_for_load_state("networkidle")

    def hover_navbar_category(self, category: str):
        """Hover over a top-level navbar category to open its dropdown."""
        self.page.locator(
            "nav#menu a.nav-link.dropdown-toggle", has_text=category
        ).first.hover()

    def get_navbar_dropdown_items(self, category: str) -> list[str]:
        """Hover a category and return its dropdown sub-menu link texts."""
        self.hover_navbar_category(category)
        parent = self.page.locator(
            "nav#menu a.nav-link.dropdown-toggle", has_text=category
        ).first.locator("..")
        items = parent.locator(".dropdown-menu a.nav-link").all()
        return [(el.text_content() or "").strip() for el in items]

    # ================================================================
    # Slider / Carousel – Visibility Checks
    # ================================================================

    def verify_slider_visible(self):
        """Assert that the carousel banner container is visible."""
        expect(self.page.locator("#carousel-banner-0")).to_be_visible()

    def verify_slider_images_visible(self):
        """Assert that the carousel contains exactly 2 slide images.

        Only the active slide is visible at any moment; the inactive slide is
        hidden by Bootstrap.  We verify the count and that the active image
        is visible.
        """
        images = self.page.locator("#carousel-banner-0 .carousel-item img")
        expect(images).to_have_count(2)
        # The currently active slide image must be visible
        active_img = self.page.locator(
            "#carousel-banner-0 .carousel-item.active img"
        )
        expect(active_img).to_be_visible()

    def verify_slider_controls_visible(self):
        """Assert that the Previous and Next carousel controls are visible."""
        expect(
            self.page.locator("#carousel-banner-0 .carousel-control-prev")
        ).to_be_visible()
        expect(
            self.page.locator("#carousel-banner-0 .carousel-control-next")
        ).to_be_visible()

    def verify_slider_indicators_visible(self):
        """Assert that the 2 carousel indicator buttons are visible."""
        indicators = self.page.locator(
            "#carousel-banner-0 .carousel-indicators button"
        )
        expect(indicators).to_have_count(2)

    def verify_all_slider_elements_visible(self):
        """Assert that all slider elements are visible (aggregate check)."""
        self.verify_slider_visible()
        self.verify_slider_images_visible()
        self.verify_slider_controls_visible()
        self.verify_slider_indicators_visible()

    # ── Slider – Actions ──────────────────────────────────────────────

    def click_slider_next(self):
        """Click the Next carousel control button."""
        self.page.locator(
            "#carousel-banner-0 .carousel-control-next"
        ).click()

    def click_slider_prev(self):
        """Click the Previous carousel control button."""
        self.page.locator(
            "#carousel-banner-0 .carousel-control-prev"
        ).click()

    def click_slider_indicator(self, index: int):
        """Click a specific carousel indicator button (0-based)."""
        self.page.locator(
            "#carousel-banner-0 .carousel-indicators button"
        ).nth(index).click()

    def get_active_slide_index(self) -> int:
        """Return the 0-based index of the currently active carousel slide."""
        items = self.page.locator("#carousel-banner-0 .carousel-item").all()
        for i, item in enumerate(items):
            if "active" in (item.get_attribute("class") or ""):
                return i
        return -1

    # ================================================================
    # Featured Section – Visibility Checks
    # ================================================================

    def verify_featured_heading_visible(self):
        """Assert that the 'Featured' heading is visible."""
        expect(
            self.page.locator("#content h3", has_text="Featured")
        ).to_be_visible()

    def verify_featured_products_visible(self):
        """Assert that exactly 4 featured product cards are visible."""
        cards = self.page.locator("#content .product-thumb")
        expect(cards).to_have_count(4)

    def verify_featured_product_images_visible(self):
        """Assert that all 4 featured product images are visible."""
        images = self.page.locator("#content .product-thumb .image img")
        expect(images).to_have_count(4)
        for i in range(4):
            expect(images.nth(i)).to_be_visible()

    def verify_featured_product_names_visible(self):
        """Assert that all 4 featured product name links are visible."""
        names = self.page.locator(
            "#content .product-thumb .description h4 a"
        )
        expect(names).to_have_count(4)
        for i in range(4):
            expect(names.nth(i)).to_be_visible()

    def verify_featured_product_prices_visible(self):
        """Assert that all 4 featured product prices are visible."""
        prices = self.page.locator(
            "#content .product-thumb .price"
        )
        expect(prices).to_have_count(4)
        for i in range(4):
            expect(prices.nth(i)).to_be_visible()

    def verify_featured_add_to_cart_buttons_visible(self):
        """Assert that all 4 'Add to Cart' buttons are visible.

        Note: Bootstrap 5 tooltips move the ``title`` attribute to
        ``data-bs-original-title`` at runtime, so we match on ``aria-label``.
        """
        buttons = self.page.locator(
            "#content .product-thumb .button-group button[aria-label='Add to Cart']"
        )
        expect(buttons).to_have_count(4)

    def verify_featured_wishlist_buttons_visible(self):
        """Assert that all 4 'Add to Wish List' buttons are visible."""
        buttons = self.page.locator(
            "#content .product-thumb .button-group button[aria-label='Add to Wish List']"
        )
        expect(buttons).to_have_count(4)

    def verify_featured_compare_buttons_visible(self):
        """Assert that all 4 'Compare this Product' buttons are visible."""
        buttons = self.page.locator(
            "#content .product-thumb .button-group button[aria-label='Compare this Product']"
        )
        expect(buttons).to_have_count(4)

    def verify_all_featured_elements_visible(self):
        """Assert that all featured section elements are visible (aggregate)."""
        self.verify_featured_heading_visible()
        self.verify_featured_products_visible()
        self.verify_featured_product_images_visible()
        self.verify_featured_product_names_visible()
        self.verify_featured_product_prices_visible()
        self.verify_featured_add_to_cart_buttons_visible()
        self.verify_featured_wishlist_buttons_visible()
        self.verify_featured_compare_buttons_visible()

    # ── Featured – Actions ────────────────────────────────────────────

    def get_featured_product_names(self) -> list[str]:
        """Return a list of featured product names."""
        self.wait_for_element("#content .product-thumb .description h4 a")
        elements = self.page.locator(
            "#content .product-thumb .description h4 a"
        ).all()
        return [(el.text_content() or "").strip() for el in elements]

    def get_featured_product_prices(self) -> list[str]:
        """Return a list of featured product prices (the 'new' or main price)."""
        self.wait_for_element("#content .product-thumb .price")
        prices = self.page.locator(
            "#content .product-thumb .price .price-new"
        ).all()
        if not prices:
            # Fallback: some products may not have price-new class
            prices = self.page.locator(
                "#content .product-thumb .price"
            ).all()
        return [(el.text_content() or "").strip().split("\n")[0] for el in prices]

    def click_featured_product(self, index: int = 0):
        """Click a featured product name link by index (0-based)."""
        self.page.locator(
            "#content .product-thumb .description h4 a"
        ).nth(index).click()
        self.page.wait_for_load_state("networkidle")

    def click_add_to_cart(self, index: int = 0):
        """Click the 'Add to Cart' button for a featured product by index."""
        self.page.locator(
            "#content .product-thumb .button-group button[aria-label='Add to Cart']"
        ).nth(index).click()

    def click_add_to_wishlist(self, index: int = 0):
        """Click the 'Add to Wish List' button for a featured product by index."""
        self.page.locator(
            "#content .product-thumb .button-group button[aria-label='Add to Wish List']"
        ).nth(index).click()

    def click_compare_product(self, index: int = 0):
        """Click the 'Compare this Product' button for a featured product by index."""
        self.page.locator(
            "#content .product-thumb .button-group button[aria-label='Compare this Product']"
        ).nth(index).click()

    # ================================================================
    # Existing helpers (retained for backward compatibility)
    # ================================================================

    def add_featured_product_to_cart(self, index: int = 0):
        """Alias for ``click_add_to_cart`` (backward compatibility)."""
        self.click_add_to_cart(index)

    def get_featured_products(self) -> list[str]:
        """Alias for ``get_featured_product_names`` (backward compatibility)."""
        return self.get_featured_product_names()

    def search_product(self, product_name: str):
        """Search for a product using the search bar."""
        self.fill("input[name='search']", product_name)
        self.click("#search button")

    def click_my_account(self):
        """Open the My Account dropdown."""
        self.page.locator("a.dropdown-toggle", has_text="My Account").first.click()

    def click_register(self):
        """Navigate to the registration page."""
        self.click_my_account()
        self.page.get_by_role("link", name="Register").click()
        self.page.wait_for_load_state("networkidle")

    def click_login(self):
        """Navigate to the login page."""
        self.click_my_account()
        self.page.get_by_role("link", name="Login").click()
        self.page.wait_for_load_state("networkidle")

    def is_logo_visible(self) -> bool:
        """Check if the store logo is displayed."""
        return self.is_visible("#logo")

    def get_cart_count(self) -> str:
        """Get the cart item count text."""
        return self.get_text("#header-cart button")
