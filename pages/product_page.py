"""
ProductPage - Page Object for the OpenCart product detail page.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class ProductPage(BasePage):
    """Page object for the OpenCart product detail page."""

    # Locators
    PRODUCT_NAME = "#content h1"
    PRODUCT_PRICE = ".price-new, #content .price"
    PRODUCT_DESCRIPTION = "#tab-description"
    PRODUCT_IMAGE = ".image-additional, .thumbnails"
    QUANTITY_INPUT = "#input-quantity"
    ADD_TO_CART_BUTTON = "#button-cart"
    WISHLIST_BUTTON = "button[data-original-title='Add to Wish List'], button[title='Add to Wish List']"
    COMPARE_BUTTON = "button[data-original-title='Compare this Product'], button[title='Compare this Product']"
    REVIEW_TAB = "a[href='#tab-review']"
    DESCRIPTION_TAB = "a[href='#tab-description']"
    SUCCESS_ALERT = ".alert-success"
    BREADCRUMB = ".breadcrumb"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_product_name(self) -> str:
        """Return the product name."""
        return self.get_text(self.PRODUCT_NAME).strip()

    def get_product_price(self) -> str:
        """Return the product price text."""
        return self.get_text(self.PRODUCT_PRICE).strip()

    def set_quantity(self, qty: int):
        """Set the product quantity."""
        self.fill(self.QUANTITY_INPUT, str(qty))

    def add_to_cart(self):
        """Click the Add to Cart button."""
        self.click(self.ADD_TO_CART_BUTTON)

    def add_to_wishlist(self):
        """Click the Add to Wishlist button."""
        self.click(self.WISHLIST_BUTTON)

    def add_to_compare(self):
        """Click the Compare button."""
        self.click(self.COMPARE_BUTTON)

    def click_review_tab(self):
        """Switch to the Review tab."""
        self.click(self.REVIEW_TAB)

    def click_description_tab(self):
        """Switch to the Description tab."""
        self.click(self.DESCRIPTION_TAB)

    def is_success_alert_visible(self) -> bool:
        """Check if the success alert is displayed after adding to cart."""
        return self.is_visible(self.SUCCESS_ALERT)

    def get_breadcrumb_text(self) -> str:
        """Return the breadcrumb navigation text."""
        return self.get_text(self.BREADCRUMB).strip()
