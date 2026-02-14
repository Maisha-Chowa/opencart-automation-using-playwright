"""
CheckoutPage - Page Object for the OpenCart checkout flow.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class CheckoutPage(BasePage):
    """Page object for the OpenCart checkout page."""

    # Locators
    PAGE_HEADING = "#content h1"

    # Guest / Account selection
    GUEST_CHECKOUT_INPUT = "input[value='guest']"
    ACCOUNT_LOGIN_INPUT = "input[value='account']"

    # Shipping / Billing details
    FIRST_NAME_INPUT = "#input-firstname"
    LAST_NAME_INPUT = "#input-lastname"
    EMAIL_INPUT = "#input-email"
    COMPANY_INPUT = "#input-company"
    ADDRESS_1_INPUT = "#input-address-1"
    ADDRESS_2_INPUT = "#input-address-2"
    CITY_INPUT = "#input-city"
    POSTCODE_INPUT = "#input-postcode"
    COUNTRY_SELECT = "#input-country"
    ZONE_SELECT = "#input-zone"

    # Shipping method
    SHIPPING_METHOD_RADIO = "input[name='shipping_method']"

    # Payment method
    PAYMENT_METHOD_RADIO = "input[name='payment_method']"

    # Buttons
    CONTINUE_BUTTON = "#button-register, #button-save"
    SHIPPING_METHOD_BUTTON = "#button-shipping-method"
    PAYMENT_METHOD_BUTTON = "#button-payment-method"
    CONFIRM_ORDER_BUTTON = "#button-confirm"

    # Alerts and messages
    ERROR_ALERT = ".alert-danger"
    SUCCESS_HEADING = "#content h1"
    FIELD_ERROR = ".text-danger"
    EMPTY_CART_MESSAGE = "#content p"

    CHECKOUT_URL_PATH = "/index.php?route=checkout/checkout"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the checkout page."""
        self.navigate(f"{self.base_url}{self.CHECKOUT_URL_PATH}")

    def select_guest_checkout(self):
        """Select the guest checkout option."""
        if self.is_visible(self.GUEST_CHECKOUT_INPUT):
            self.page.locator(self.GUEST_CHECKOUT_INPUT).check()

    def fill_billing_details(
        self,
        first_name: str,
        last_name: str,
        email: str,
        address_1: str,
        city: str,
        postcode: str,
        country: str = "",
        zone: str = "",
    ):
        """Fill in the billing/shipping address form."""
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.ADDRESS_1_INPUT, address_1)
        self.fill(self.CITY_INPUT, city)
        self.fill(self.POSTCODE_INPUT, postcode)

        if country:
            self.page.select_option(self.COUNTRY_SELECT, label=country)
            self.page.wait_for_load_state("networkidle")

        if zone:
            self.page.select_option(self.ZONE_SELECT, label=zone)

    def click_continue(self):
        """Click the Continue button on the checkout form."""
        self.click(self.CONTINUE_BUTTON)
        self.page.wait_for_load_state("networkidle")

    def select_shipping_method(self):
        """Select the first available shipping method."""
        if self.is_visible(self.SHIPPING_METHOD_RADIO):
            self.page.locator(self.SHIPPING_METHOD_RADIO).first.check()

    def click_shipping_method_continue(self):
        """Click Continue on the shipping method step."""
        if self.is_visible(self.SHIPPING_METHOD_BUTTON):
            self.click(self.SHIPPING_METHOD_BUTTON)
            self.page.wait_for_load_state("networkidle")

    def select_payment_method(self):
        """Select the first available payment method."""
        if self.is_visible(self.PAYMENT_METHOD_RADIO):
            self.page.locator(self.PAYMENT_METHOD_RADIO).first.check()

    def click_payment_method_continue(self):
        """Click Continue on the payment method step."""
        if self.is_visible(self.PAYMENT_METHOD_BUTTON):
            self.click(self.PAYMENT_METHOD_BUTTON)
            self.page.wait_for_load_state("networkidle")

    def confirm_order(self):
        """Click the Confirm Order button."""
        if self.is_visible(self.CONFIRM_ORDER_BUTTON):
            self.click(self.CONFIRM_ORDER_BUTTON)
            self.page.wait_for_load_state("networkidle")

    def is_order_confirmed(self) -> bool:
        """Check if the order confirmation/success page is displayed."""
        heading = self.get_text(self.SUCCESS_HEADING)
        url = self.get_url()
        return (
            "success" in url.lower()
            or "your order has been placed" in heading.lower()
            if heading
            else False
        )

    def get_error_message(self) -> str:
        """Return the error alert message, if any."""
        if self.is_visible(self.ERROR_ALERT):
            return self.get_text(self.ERROR_ALERT).strip()
        return ""

    def get_field_errors(self) -> list[str]:
        """Return all field-level validation error messages."""
        elements = self.page.locator(self.FIELD_ERROR).all()
        return [el.text_content() or "" for el in elements]

    def is_cart_empty_redirect(self) -> bool:
        """Check if checkout redirected due to empty cart."""
        url = self.get_url()
        if "cart" in url.lower():
            text = self.get_text(self.EMPTY_CART_MESSAGE)
            return "empty" in text.lower() if text else False
        return False
