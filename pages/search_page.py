"""
SearchPage - Page Object for the OpenCart search results page.

Covers:
  1. Search form elements (input, button, description checkbox, category dropdown)
  2. Search results (product cards with images, names, prices, action buttons)
  3. No-results messaging
  4. Sort / limit / view controls
"""

from pages.base_page import BasePage
from playwright.sync_api import Page, expect, TimeoutError as PwTimeout


class SearchPage(BasePage):
    """Page object for the OpenCart search results page."""

    SEARCH_URL_PATH = "index.php?route=product/search&language=en-gb"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the search page directly (no search term)."""
        self.navigate(f"{self.base_url}{self.SEARCH_URL_PATH}")

    def open_with_query(self, keyword: str):
        """Navigate directly to the search results page for a keyword."""
        self.navigate(
            f"{self.base_url}{self.SEARCH_URL_PATH}&search={keyword}"
        )

    def search_from_home(self, keyword: str):
        """Search for a product via the header search bar on the home page.

        This mimics the real user flow: go to home → type in the header
        search bar → click the search button → land on search results.
        """
        self.navigate(self.base_url)
        self.page.locator("input[name='search']").fill(keyword)
        self.page.locator("#search button").click()
        self.page.wait_for_load_state("networkidle")

    # ================================================================
    # Visibility checks: Search Form
    # ================================================================

    def verify_search_heading_visible(self):
        """Assert that the 'Search' heading is visible."""
        expect(
            self.page.locator("#content h1", has_text="Search")
        ).to_be_visible()

    def verify_search_input_visible(self):
        """Assert that the search keyword input is visible."""
        expect(self.page.locator("#input-search")).to_be_visible()

    def verify_search_button_visible(self):
        """Assert that the Search button is visible."""
        expect(self.page.locator("#button-search")).to_be_visible()

    def verify_search_criteria_label_visible(self):
        """Assert that the 'Search Criteria' label is visible."""
        expect(
            self.page.locator("label[for='input-search']")
        ).to_be_visible()

    def verify_description_checkbox_visible(self):
        """Assert that the 'Search in product descriptions' checkbox is visible."""
        expect(self.page.locator("#input-description")).to_be_visible()

    def verify_category_dropdown_visible(self):
        """Assert that the category dropdown is visible."""
        expect(
            self.page.locator("select[name='category_id']")
        ).to_be_visible()

    def verify_subcategory_checkbox_visible(self):
        """Assert that the 'Search in subcategories' checkbox is visible."""
        expect(self.page.locator("#input-sub-category")).to_be_visible()

    def verify_all_search_form_elements_visible(self):
        """Assert that all search form elements are visible (aggregate)."""
        self.verify_search_heading_visible()
        self.verify_search_input_visible()
        self.verify_search_button_visible()
        self.verify_search_criteria_label_visible()
        self.verify_description_checkbox_visible()
        self.verify_category_dropdown_visible()
        self.verify_subcategory_checkbox_visible()

    # ================================================================
    # Visibility checks: Results Controls (only visible when results exist)
    # ================================================================

    def verify_sort_dropdown_visible(self):
        """Assert that the Sort By dropdown is visible."""
        expect(self.page.locator("#input-sort")).to_be_visible()

    def verify_limit_dropdown_visible(self):
        """Assert that the Show (limit) dropdown is visible."""
        expect(self.page.locator("#input-limit")).to_be_visible()

    def verify_grid_view_button_visible(self):
        """Assert that the Grid view button is visible."""
        expect(self.page.locator("#button-grid")).to_be_visible()

    def verify_list_view_button_visible(self):
        """Assert that the List view button is visible."""
        expect(self.page.locator("#button-list")).to_be_visible()

    def verify_all_result_controls_visible(self):
        """Assert that all result display controls are visible (aggregate)."""
        self.verify_sort_dropdown_visible()
        self.verify_limit_dropdown_visible()
        self.verify_grid_view_button_visible()
        self.verify_list_view_button_visible()

    # ================================================================
    # Search form actions
    # ================================================================

    def search(self, keyword: str):
        """Perform a search from the search page itself."""
        self.page.locator("#input-search").fill(keyword)
        self.page.locator("#button-search").click()
        self.page.wait_for_load_state("networkidle")

    def toggle_description_search(self):
        """Toggle the 'Search in product descriptions' checkbox."""
        self.page.locator("#input-description").click()

    def select_category(self, category_text: str):
        """Select a category from the dropdown by visible text."""
        self.page.locator("select[name='category_id']").select_option(
            label=category_text
        )

    # ================================================================
    # Result inspection
    # ================================================================

    def get_search_results_count(self) -> int:
        """Return the number of product cards in the search results."""
        return self.page.locator("#content .product-thumb").count()

    def get_result_names(self) -> list[str]:
        """Return a list of product names from search results."""
        elements = self.page.locator(
            "#content .product-thumb .description h4 a"
        ).all()
        return [(el.text_content() or "").strip() for el in elements]

    def get_result_prices(self) -> list[str]:
        """Return a list of product prices from search results."""
        elements = self.page.locator(
            "#content .product-thumb .price"
        ).all()
        return [(el.text_content() or "").strip().split("\n")[0] for el in elements]

    def get_result_images_count(self) -> int:
        """Return the number of product images in search results."""
        return self.page.locator(
            "#content .product-thumb .image img"
        ).count()

    def get_heading_text(self) -> str:
        """Return the search page heading text (e.g. 'Search - macbook')."""
        return (
            self.page.locator("#content h1").text_content() or ""
        ).strip()

    # ── No-results helpers ────────────────────────────────────────────

    def has_no_results(self) -> bool:
        """Check if the 'no product' message is displayed."""
        paragraphs = self.page.locator("#content p").all()
        for p in paragraphs:
            text = (p.text_content() or "").lower()
            if "no product" in text:
                return True
        return False

    def get_no_results_message(self) -> str:
        """Return the no-results message text, if any."""
        paragraphs = self.page.locator("#content p").all()
        for p in paragraphs:
            text = (p.text_content() or "").strip()
            if "no product" in text.lower():
                return text
        return ""

    # ── Result interaction ────────────────────────────────────────────

    def click_product(self, index: int = 0):
        """Click on a product name link from the search results by index."""
        self.page.locator(
            "#content .product-thumb .description h4 a"
        ).nth(index).click()
        self.page.wait_for_load_state("networkidle")

    def click_add_to_cart(self, index: int = 0):
        """Click the 'Add to Cart' button for a result product by index.

        Bootstrap tooltips move ``title`` to ``aria-label`` at runtime.
        """
        self.page.locator(
            "#content .product-thumb .button-group button[aria-label='Add to Cart']"
        ).nth(index).click()

    def click_add_to_wishlist(self, index: int = 0):
        """Click the 'Add to Wish List' button for a result product by index."""
        self.page.locator(
            "#content .product-thumb .button-group button[aria-label='Add to Wish List']"
        ).nth(index).click()

    def click_compare_product(self, index: int = 0):
        """Click the 'Compare this Product' button for a result product by index."""
        self.page.locator(
            "#content .product-thumb .button-group button[aria-label='Compare this Product']"
        ).nth(index).click()
