"""
CheckoutPage - Page Object for the OpenCart checkout flow.

Covers:
  1. Checkout page template (heading, fieldsets, order summary)
  2. Account type toggle (Register / Guest)
  3. Guest checkout form (personal details + shipping address)
  4. Form validation (required field errors)
  5. Payment method selection & order confirmation
  6. Cart page coupon & gift certificate accordion forms

OpenCart 4.x uses a single-page AJAX checkout.  After filling the address
and clicking Continue, shipping and payment methods load via AJAX.

Note: Complete order placement requires shipping & payment extensions to be
properly configured in admin.  The template tests focus on the form
structure and validation, which work regardless of extension config.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class CheckoutPage(BasePage):
    """Page object for the OpenCart checkout page."""

    CHECKOUT_URL_PATH = "index.php?route=checkout/checkout&language=en-gb"
    CART_URL_PATH = "index.php?route=checkout/cart&language=en-gb"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the checkout page."""
        self.navigate(f"{self.base_url}{self.CHECKOUT_URL_PATH}")

    def open_cart(self):
        """Navigate to the cart page (for coupon/gift certificate tests)."""
        self.navigate(f"{self.base_url}{self.CART_URL_PATH}")

    # ================================================================
    # Visibility checks: Checkout Page Template
    # ================================================================

    def verify_heading_visible(self):
        """Assert that the Checkout heading is visible."""
        expect(self.page.locator("#content h1")).to_be_visible()

    def verify_personal_details_fieldset_visible(self):
        """Assert that the 'Your Personal Details' fieldset is visible."""
        expect(
            self.page.locator("fieldset legend", has_text="Your Personal Details")
        ).to_be_visible()

    def verify_shipping_address_fieldset_visible(self):
        """Assert that the 'Shipping Address' fieldset is visible."""
        expect(
            self.page.locator("#shipping-address legend", has_text="Shipping Address")
        ).to_be_visible()

    def verify_guest_radio_visible(self):
        """Assert that the Guest Checkout radio is visible."""
        expect(self.page.locator("#input-guest")).to_be_visible()

    def verify_register_radio_visible(self):
        """Assert that the Register Account radio is visible."""
        expect(self.page.locator("#input-register")).to_be_visible()

    def verify_firstname_input_visible(self):
        """Assert that the First Name input is visible."""
        expect(self.page.locator("#input-firstname")).to_be_visible()

    def verify_lastname_input_visible(self):
        """Assert that the Last Name input is visible."""
        expect(self.page.locator("#input-lastname")).to_be_visible()

    def verify_email_input_visible(self):
        """Assert that the E-Mail input is visible."""
        expect(self.page.locator("#input-email")).to_be_visible()

    def verify_continue_button_visible(self):
        """Assert that the Continue button is visible."""
        expect(self.page.locator("#button-register")).to_be_visible()

    def verify_order_summary_visible(self):
        """Assert that the order summary table is visible in checkout."""
        expect(
            self.page.locator("#checkout-confirm table")
        ).to_be_visible()

    def verify_all_checkout_elements_visible(self):
        """Assert all essential checkout elements are visible (aggregate)."""
        self.verify_heading_visible()
        self.verify_personal_details_fieldset_visible()
        self.verify_shipping_address_fieldset_visible()
        self.verify_guest_radio_visible()
        self.verify_register_radio_visible()
        self.verify_firstname_input_visible()
        self.verify_lastname_input_visible()
        self.verify_email_input_visible()
        self.verify_continue_button_visible()
        self.verify_order_summary_visible()

    # ================================================================
    # Visibility checks: Cart Page Coupon & Gift Certificate
    # ================================================================

    def verify_coupon_accordion_visible(self):
        """Assert the 'Use Coupon Code' accordion button is visible on cart page."""
        expect(
            self.page.locator('button:has-text("Use Coupon Code")')
        ).to_be_visible()

    def verify_gift_accordion_visible(self):
        """Assert the 'Use Gift Certificate' accordion button is visible on cart page."""
        expect(
            self.page.locator('button:has-text("Use Gift Certificate")')
        ).to_be_visible()

    def verify_coupon_form_visible(self):
        """Open the coupon accordion and assert the form is visible."""
        self.page.locator('button:has-text("Use Coupon Code")').click()
        self.page.wait_for_timeout(500)
        expect(self.page.locator("#input-coupon")).to_be_visible()
        expect(
            self.page.locator('#form-coupon button[type="submit"]')
        ).to_be_visible()

    def verify_gift_form_visible(self):
        """Open the gift certificate accordion and assert the form is visible."""
        self.page.locator('button:has-text("Use Gift Certificate")').click()
        self.page.wait_for_timeout(500)
        expect(self.page.locator("#input-voucher")).to_be_visible()
        expect(
            self.page.locator('#form-voucher button[type="submit"]')
        ).to_be_visible()

    # ================================================================
    # Data extraction
    # ================================================================

    def get_heading_text(self) -> str:
        """Return the checkout heading text."""
        return (
            self.page.locator("#content h1").text_content() or ""
        ).strip()

    def get_order_summary_total(self) -> str:
        """Return the Total from the checkout order summary."""
        row = self.page.locator(
            "#checkout-confirm tfoot tr", has_text="Total"
        ).last
        return (row.locator("td:last-child").text_content() or "").strip()

    def get_order_summary_product_names(self) -> list[str]:
        """Return product names from the checkout order summary."""
        links = self.page.locator("#checkout-confirm tbody a").all()
        return [(el.text_content() or "").strip() for el in links]

    def get_validation_errors(self) -> list[str]:
        """Return all visible validation error messages after form submit."""
        errors = self.page.locator(".is-invalid, .invalid-feedback").all()
        return [
            (e.text_content() or "").strip()
            for e in errors
            if e.is_visible() and (e.text_content() or "").strip()
        ]

    def get_alert_text(self) -> str:
        """Return the text of any visible alert on the page."""
        alert = self.page.locator(".alert").first
        if alert.count() and alert.is_visible():
            return (alert.text_content() or "").strip()
        return ""

    def has_success_alert(self) -> bool:
        """Check if a success alert is visible."""
        return self.page.locator(".alert-success").count() > 0

    def has_danger_alert(self) -> bool:
        """Check if a danger alert is visible."""
        return self.page.locator(".alert-danger").count() > 0

    # ================================================================
    # Checkout actions
    # ================================================================

    def select_guest_checkout(self):
        """Select the Guest Checkout radio button."""
        self.page.locator("#input-guest").click()
        self.page.wait_for_timeout(500)

    def select_register_account(self):
        """Select the Register Account radio button."""
        self.page.locator("#input-register").click()
        self.page.wait_for_timeout(500)

    def fill_guest_details(
        self,
        firstname: str,
        lastname: str,
        email: str,
        address_1: str,
        city: str,
        postcode: str,
        country: str = "",
        zone: str = "",
    ):
        """Fill the guest checkout form fields."""
        self.page.fill("#input-firstname", firstname)
        self.page.fill("#input-lastname", lastname)
        self.page.fill("#input-email", email)
        self.page.fill("#input-shipping-address-1", address_1)
        self.page.fill("#input-shipping-city", city)
        self.page.fill("#input-shipping-postcode", postcode)

        if country:
            self.page.select_option(
                "#input-shipping-country", label=country
            )
            self.page.wait_for_timeout(1500)

        if zone:
            self.page.select_option(
                "#input-shipping-zone", label=zone
            )

    def click_continue(self):
        """Submit the checkout form via Playwright's request API."""
        json_resp = self._oc_submit(
            "#form-register",
            url=f"{self.base_url}index.php?route=checkout/register|save&language=en-gb",
        )
        if isinstance(json_resp, dict) and json_resp.get("redirect"):
            self.page.goto(json_resp["redirect"])
        self.page.wait_for_load_state("networkidle")

    # ================================================================
    # Coupon actions (on the cart page)
    # ================================================================

    def apply_coupon(self, code: str):
        """Open the coupon accordion, enter code, and apply."""
        accordion = self.page.locator('button:has-text("Use Coupon Code")')
        collapsed = self.page.locator("#collapse-coupon")
        if not collapsed.is_visible():
            accordion.click()
            self.page.wait_for_timeout(500)

        self.page.fill("#input-coupon", code)

        self._oc_submit("#form-coupon")
        reload_url = f"{self.base_url}index.php?route=checkout/cart|list&language=en-gb"
        self._oc_reload_html(reload_url, "#shopping-cart")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(500)

    def apply_gift_certificate(self, code: str):
        """Open the gift certificate accordion, enter code, and apply."""
        accordion = self.page.locator(
            'button:has-text("Use Gift Certificate")'
        )
        collapsed = self.page.locator("#collapse-voucher")
        if not collapsed.is_visible():
            accordion.click()
            self.page.wait_for_timeout(500)

        self.page.fill("#input-voucher", code)

        self._oc_submit("#form-voucher")
        reload_url = f"{self.base_url}index.php?route=checkout/cart|list&language=en-gb"
        self._oc_reload_html(reload_url, "#shopping-cart")
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(500)

    def get_cart_totals(self) -> dict[str, str]:
        """Return cart totals as a dict (e.g. {'Sub-Total': '$500.00'})."""
        rows = self.page.locator("#checkout-total tr").all()
        totals = {}
        for tr in rows:
            cells = tr.locator("td").all()
            if len(cells) == 2:
                label = (cells[0].text_content() or "").strip()
                value = (cells[1].text_content() or "").strip()
                totals[label] = value
        return totals

    # ================================================================
    # Backward compatibility aliases
    # ================================================================

    def fill_billing_details(self, **kwargs):
        """Alias for ``fill_guest_details`` (backward compat)."""
        self.fill_guest_details(**kwargs)

    def is_order_confirmed(self) -> bool:
        """Check if the order success page is displayed."""
        url = self.get_url()
        heading = self.get_heading_text()
        return (
            "success" in url.lower()
            or "your order has been placed" in heading.lower()
        )

    def is_cart_empty_redirect(self) -> bool:
        """Check if checkout redirected due to empty cart."""
        url = self.get_url()
        if "cart" in url.lower():
            return "empty" in (
                self.page.locator("#content p").first.text_content() or ""
            ).lower()
        return False
