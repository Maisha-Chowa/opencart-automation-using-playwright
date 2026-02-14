"""
SearchPage - Page Object for the OpenCart search results page.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class SearchPage(BasePage):
    """Page object for the OpenCart search results page."""

    # Locators
    SEARCH_INPUT = "#input-search"
    SEARCH_BUTTON = "#button-search"
    SEARCH_RESULTS = ".product-thumb"
    PRODUCT_NAME = ".product-thumb .description h4 a"
    PRODUCT_PRICE = ".product-thumb .description .price"
    PRODUCT_IMAGE = ".product-thumb .image img"
    NO_RESULTS_MESSAGE = "#content p"
    PAGE_HEADING = "#content h1"
    SEARCH_CRITERIA_CHECKBOX = "#input-description"
    CATEGORY_DROPDOWN = "select[name='category_id']"
    ADD_TO_CART_BUTTON = ".product-thumb .button-group button:first-child"

    def __init__(self, page: Page):
        super().__init__(page)

    def search(self, keyword: str):
        """Perform a search from the search page."""
        self.fill(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    def get_search_results_count(self) -> int:
        """Return the number of search results."""
        return self.page.locator(self.SEARCH_RESULTS).count()

    def get_result_names(self) -> list[str]:
        """Return a list of product names from search results."""
        elements = self.page.locator(self.PRODUCT_NAME).all()
        return [el.text_content() or "" for el in elements]

    def has_no_results(self) -> bool:
        """Check if the 'no results' message is displayed."""
        text = self.get_text(self.NO_RESULTS_MESSAGE)
        return "no product" in text.lower() if text else False

    def click_product(self, index: int = 0):
        """Click on a product from the search results by index."""
        products = self.page.locator(self.PRODUCT_NAME).all()
        if index < len(products):
            products[index].click()

    def add_to_cart(self, index: int = 0):
        """Add a product to cart from search results by index."""
        buttons = self.page.locator(self.ADD_TO_CART_BUTTON).all()
        if index < len(buttons):
            buttons[index].click()

    def get_result_prices(self) -> list[str]:
        """Return a list of product prices from search results."""
        elements = self.page.locator(self.PRODUCT_PRICE).all()
        return [el.text_content() or "" for el in elements]

    def get_result_images_count(self) -> int:
        """Return the number of product images in search results."""
        return self.page.locator(self.PRODUCT_IMAGE).count()
