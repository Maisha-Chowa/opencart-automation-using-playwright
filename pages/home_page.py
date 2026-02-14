"""
HomePage - Page Object for the OpenCart storefront home page.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class HomePage(BasePage):
    """Page object for the OpenCart home page."""

    # Locators
    SEARCH_INPUT = "input[name='search']"
    SEARCH_BUTTON = "#search button"
    CART_BUTTON = "#header-cart button"
    LOGO = "#logo"
    NAVBAR = ".navbar"
    SLIDESHOW = "#slideshow0"
    FEATURED_PRODUCTS = "#content .row"
    PRODUCT_CARD = ".product-thumb"
    PRODUCT_NAME = ".product-thumb .description h4 a"
    PRODUCT_PRICE = ".product-thumb .description .price"
    ADD_TO_CART_BUTTON = ".product-thumb .button-group button:first-child"
    MY_ACCOUNT_DROPDOWN = "a[title='My Account']"
    REGISTER_LINK = "a:has-text('Register')"
    LOGIN_LINK = "a:has-text('Login')"
    CURRENCY_DROPDOWN = "#form-currency"
    SHOPPING_CART_LINK = "a[title='Shopping Cart']"
    CHECKOUT_LINK = "a[title='Checkout']"
    SUCCESS_ALERT = ".alert-success"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the home page."""
        self.navigate(self.base_url)

    def search_product(self, product_name: str):
        """Search for a product using the search bar."""
        self.fill(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)

    def get_featured_products(self) -> list[str]:
        """Return a list of featured product names."""
        self.wait_for_element(self.PRODUCT_NAME)
        elements = self.page.locator(self.PRODUCT_NAME).all()
        return [el.text_content() or "" for el in elements]

    def add_featured_product_to_cart(self, index: int = 0):
        """Add a featured product to the cart by index (0-based)."""
        buttons = self.page.locator(self.ADD_TO_CART_BUTTON).all()
        if index < len(buttons):
            buttons[index].click()

    def click_my_account(self):
        """Open the My Account dropdown."""
        self.click(self.MY_ACCOUNT_DROPDOWN)

    def click_register(self):
        """Navigate to the registration page."""
        self.click_my_account()
        self.click(self.REGISTER_LINK)

    def click_login(self):
        """Navigate to the login page."""
        self.click_my_account()
        self.click(self.LOGIN_LINK)

    def is_logo_visible(self) -> bool:
        """Check if the store logo is displayed."""
        return self.is_visible(self.LOGO)

    def is_slideshow_visible(self) -> bool:
        """Check if the slideshow/banner is displayed."""
        return self.is_visible(self.SLIDESHOW)

    def get_cart_count(self) -> str:
        """Get the cart item count text."""
        return self.get_text(self.CART_BUTTON)
