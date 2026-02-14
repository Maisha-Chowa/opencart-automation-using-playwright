"""
CartPage - Page Object for the OpenCart shopping cart page.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class CartPage(BasePage):
    """Page object for the OpenCart shopping cart page."""

    # Locators
    PAGE_HEADING = "#content h1"
    CART_TABLE = ".table-bordered"
    PRODUCT_NAME = ".table-bordered td:nth-child(2) a"
    PRODUCT_QUANTITY = ".table-bordered input[name^='quantity']"
    PRODUCT_UNIT_PRICE = ".table-bordered td:nth-child(5)"
    PRODUCT_TOTAL = ".table-bordered td:nth-child(6)"
    UPDATE_BUTTON = ".table-bordered button[data-original-title='Update'], .table-bordered button[title='Update']"
    REMOVE_BUTTON = ".table-bordered button[data-original-title='Remove'], .table-bordered button[title='Remove']"
    CONTINUE_SHOPPING_BUTTON = "a:has-text('Continue Shopping')"
    CHECKOUT_BUTTON = "a:has-text('Checkout')"
    EMPTY_CART_MESSAGE = "#content p"
    SUB_TOTAL = "#content .table-bordered tfoot td:last-child"
    COUPON_INPUT = "#input-coupon"
    COUPON_BUTTON = "#button-coupon"

    CART_URL_PATH = "/index.php?route=checkout/cart"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate directly to the cart page."""
        self.navigate(f"{self.base_url}{self.CART_URL_PATH}")

    def get_cart_items_count(self) -> int:
        """Return the number of items in the cart table."""
        return self.page.locator(self.PRODUCT_NAME).count()

    def get_product_names(self) -> list[str]:
        """Return a list of product names in the cart."""
        elements = self.page.locator(self.PRODUCT_NAME).all()
        return [el.text_content() or "" for el in elements]

    def update_quantity(self, index: int, qty: int):
        """Update the quantity of a cart item by index."""
        inputs = self.page.locator(self.PRODUCT_QUANTITY).all()
        if index < len(inputs):
            inputs[index].fill(str(qty))
            update_buttons = self.page.locator(self.UPDATE_BUTTON).all()
            if index < len(update_buttons):
                update_buttons[index].click()

    def remove_item(self, index: int = 0):
        """Remove an item from the cart by index."""
        buttons = self.page.locator(self.REMOVE_BUTTON).all()
        if index < len(buttons):
            buttons[index].click()

    def is_cart_empty(self) -> bool:
        """Check if the cart is empty."""
        text = self.get_text(self.EMPTY_CART_MESSAGE)
        return "your shopping cart is empty" in text.lower() if text else False

    def click_checkout(self):
        """Click the Checkout button."""
        self.click(self.CHECKOUT_BUTTON)

    def click_continue_shopping(self):
        """Click the Continue Shopping button."""
        self.click(self.CONTINUE_SHOPPING_BUTTON)
