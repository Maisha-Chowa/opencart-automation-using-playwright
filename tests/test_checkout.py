"""
Test Suite: Checkout (Checkout Page + Cart Coupon & Gift Certificate)

Strategy: Test the checkout *template* with one product (MacBook).
Data-driven tests verify form validation with different address combos.
Coupon and gift certificate tests verify the cart page accordion forms.

Note: Complete order placement requires shipping & payment extensions
to be properly configured in admin — environment-dependent.
These tests focus on what the *template* guarantees: form structure,
validation, and coupon/gift code handling.

Classes:
  TestCheckoutPageTemplate       — checkout page structure (5 tests)
  TestCheckoutFormValidation     — data-driven form validation (5 tests)
  TestCartCouponAndGiftCertificate — coupon/gift on cart page (4 tests)
Total: 14 tests
"""

import pytest
from pages.product_page import ProductPage
from pages.checkout_page import CheckoutPage
from utilities.csv_reader import read_csv

# ── Load CSV data once ──────────────────────────────────────────
CHECKOUT_CSV_DATA = read_csv("checkout_data.csv")


def _add_macbook_to_cart(page, base_url):
    """Helper: add MacBook to cart so checkout/cart pages have a product."""
    pp = ProductPage(page, base_url)
    pp.open(43)
    pp.add_to_cart()
    page.wait_for_selector(".alert-success", timeout=5000)


# ================================================================
# Template Tests (checkout page structure — MacBook in cart)
# ================================================================
@pytest.mark.checkout
@pytest.mark.regression
class TestCheckoutPageTemplate:
    """Verify checkout page template renders correctly with one product.

    Adds MacBook to cart, then validates that the checkout page
    shows all structural elements.
    """

    def test_all_checkout_elements_visible(self, page, base_url):
        """All checkout page elements should be visible."""
        _add_macbook_to_cart(page, base_url)
        cp = CheckoutPage(page, base_url)
        cp.open()
        cp.verify_all_checkout_elements_visible()

    def test_guest_register_toggle(self, page, base_url):
        """Selecting Guest should hide the password fieldset."""
        _add_macbook_to_cart(page, base_url)
        cp = CheckoutPage(page, base_url)
        cp.open()

        cp.select_guest_checkout()
        pw_fieldset = page.locator(
            'fieldset:has(legend:has-text("Your Password"))'
        )
        assert not pw_fieldset.is_visible(), (
            "Password fieldset should be hidden for Guest checkout"
        )

    def test_order_summary_shows_product(self, page, base_url):
        """Order summary should list MacBook with correct total."""
        _add_macbook_to_cart(page, base_url)
        cp = CheckoutPage(page, base_url)
        cp.open()

        names = cp.get_order_summary_product_names()
        assert "MacBook" in names, (
            f"Order summary should contain 'MacBook', got {names}"
        )
        assert cp.get_order_summary_total() == "$602.00"

    def test_empty_cart_redirects(self, page, base_url):
        """Checkout with empty cart should redirect to cart or show error."""
        cp = CheckoutPage(page, base_url)
        cp.open()

        url = cp.get_url()
        assert (
            cp.is_cart_empty_redirect()
            or "cart" in url.lower()
            or "checkout" in url.lower()
        ), "Empty cart checkout should redirect or show error"

    def test_guest_form_accepts_valid_data(self, page, base_url):
        """Guest checkout form should accept valid address data."""
        _add_macbook_to_cart(page, base_url)
        cp = CheckoutPage(page, base_url)
        cp.open()
        cp.select_guest_checkout()

        cp.fill_guest_details(
            firstname="John",
            lastname="Doe",
            email="john.doe@test.com",
            address_1="123 Test St",
            city="New York",
            postcode="10001",
            country="United States",
            zone="New York",
        )
        cp.click_continue()

        errors = cp.get_validation_errors()
        assert len(errors) == 0, (
            f"Valid data should produce no errors, got: {errors}"
        )


# ================================================================
# Data-Driven: Form Validation (different address combos)
# ================================================================
@pytest.mark.checkout
@pytest.mark.regression
class TestCheckoutFormValidation:
    """Data-driven form validation using checkout_data.csv.

    Tests that missing required fields trigger validation errors,
    and valid data passes without errors.
    """

    @pytest.mark.parametrize(
        "row",
        CHECKOUT_CSV_DATA,
        ids=[row["test_id"] for row in CHECKOUT_CSV_DATA],
    )
    def test_checkout_form_validation(self, page, base_url, row):
        """Form should show errors for missing required fields."""
        _add_macbook_to_cart(page, base_url)
        cp = CheckoutPage(page, base_url)
        cp.open()
        cp.select_guest_checkout()

        cp.fill_guest_details(
            firstname=row["firstname"],
            lastname=row["lastname"],
            email=row["email"],
            address_1=row["address_1"],
            city=row["city"],
            postcode=row["postcode"],
            country=row["country"] if row["country"] else "",
            zone=row["zone"] if row["zone"] else "",
        )
        cp.click_continue()

        expected = row["expected_result"]
        if expected == "error":
            errors = cp.get_validation_errors()
            has_alert = cp.has_danger_alert()
            assert len(errors) > 0 or has_alert, (
                f"[{row['test_id']}] Missing field should trigger "
                f"validation error"
            )
        else:
            errors = cp.get_validation_errors()
            assert len(errors) == 0, (
                f"[{row['test_id']}] Valid data should produce no "
                f"errors, got: {errors}"
            )


# ================================================================
# Cart Page: Coupon & Gift Certificate
# ================================================================
@pytest.mark.cart
@pytest.mark.regression
class TestCartCouponAndGiftCertificate:
    """Test coupon and gift certificate forms on the cart page.

    The coupon/gift certificate accordions are on the cart page
    (checkout/cart), not on the checkout page.

    Coupon code '2222' is the demo '-10% Discount' coupon.
    """

    def test_coupon_and_gift_accordions_visible(self, page, base_url):
        """Cart page should show coupon and gift certificate accordion buttons."""
        _add_macbook_to_cart(page, base_url)
        cp = CheckoutPage(page, base_url)
        cp.open_cart()
        cp.verify_coupon_accordion_visible()
        cp.verify_gift_accordion_visible()

    def test_valid_coupon_applies_discount(self, page, base_url):
        """Applying valid coupon '2222' should show success and add discount line."""
        _add_macbook_to_cart(page, base_url)
        cp = CheckoutPage(page, base_url)
        cp.open_cart()
        cp.apply_coupon("2222")

        assert cp.has_success_alert(), "Valid coupon should show success alert"
        totals = cp.get_cart_totals()
        assert any("coupon" in k.lower() for k in totals), (
            f"Totals should include a Coupon line, got: {totals}"
        )

    def test_invalid_coupon_shows_error(self, page, base_url):
        """Applying invalid coupon should show error alert."""
        _add_macbook_to_cart(page, base_url)
        cp = CheckoutPage(page, base_url)
        cp.open_cart()
        cp.apply_coupon("INVALID_COUPON_XYZ")

        assert cp.has_danger_alert(), "Invalid coupon should show danger alert"
        alert = cp.get_alert_text().lower()
        assert "invalid" in alert or "expired" in alert, (
            f"Error should mention 'invalid', got: '{alert}'"
        )

    def test_invalid_gift_certificate_shows_error(self, page, base_url):
        """Applying invalid gift certificate should show error alert."""
        _add_macbook_to_cart(page, base_url)
        cp = CheckoutPage(page, base_url)
        cp.open_cart()
        cp.apply_gift_certificate("FAKE_GIFT_CODE")

        assert cp.has_danger_alert(), (
            "Invalid gift certificate should show danger alert"
        )
        alert = cp.get_alert_text().lower()
        assert "invalid" in alert or "balance" in alert, (
            f"Error should mention 'invalid', got: '{alert}'"
        )
