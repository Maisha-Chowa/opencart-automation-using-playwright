"""
Test Suite: Cart (Add to Cart & View Cart)

Strategy: Test the cart *template* with one representative product (MacBook).
Data-driven tests verify the add-to-cart flow for products that can be added
without required options (MacBook, iPhone).

Note: Apple Cinema 30" and Canon EOS 5D have required product options
and need separate "add with options" tests — out of scope here.

Classes:
  TestCartPageTemplate    — cart template structure & data (5 tests, MacBook)
  TestAddToCartDataDriven — each simple product adds correctly (2 tests)
  TestCartInteractions    — update qty, remove, view cart (3 tests, MacBook)
Total: 10 tests
"""

import pytest
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utilities.csv_reader import read_csv

# ── Load CSV data once ──────────────────────────────────────────
CART_CSV_DATA = read_csv("cart_data.csv")


# ================================================================
# Template Tests (single product — MacBook, ID=43)
# ================================================================
@pytest.mark.cart
@pytest.mark.regression
class TestCartPageTemplate:
    """Verify cart page template using one product (MacBook).

    Adds MacBook to the cart, then validates that the cart page
    renders all structural elements correctly.
    """

    PRODUCT_ID = 43
    EXPECTED_NAME = "MacBook"
    EXPECTED_PRICE = "$602.00"
    EXPECTED_MODEL = "Product 16"

    def _add_macbook_to_cart(self, page, base_url):
        """Helper: add MacBook to cart via the product page."""
        pp = ProductPage(page, base_url)
        pp.open(self.PRODUCT_ID)
        pp.add_to_cart()
        page.wait_for_selector(".alert-success", timeout=5000)

    def test_all_cart_elements_visible(self, page, base_url):
        """All cart page elements should be visible after adding a product."""
        self._add_macbook_to_cart(page, base_url)
        cp = CartPage(page, base_url)
        cp.open()
        cp.verify_all_cart_elements_visible()

    def test_cart_table_shows_product_details(self, page, base_url):
        """Cart table should show correct product name, model, and price."""
        self._add_macbook_to_cart(page, base_url)
        cp = CartPage(page, base_url)
        cp.open()

        names = cp.get_product_names()
        assert self.EXPECTED_NAME in names, (
            f"Cart should contain '{self.EXPECTED_NAME}', got {names}"
        )
        assert cp.get_product_model(0) == self.EXPECTED_MODEL
        assert cp.get_unit_price(0) == self.EXPECTED_PRICE
        assert cp.get_row_total(0) == self.EXPECTED_PRICE

    def test_cart_quantity_defaults_to_one(self, page, base_url):
        """Default quantity should be 1 after adding a product."""
        self._add_macbook_to_cart(page, base_url)
        cp = CartPage(page, base_url)
        cp.open()
        assert cp.get_product_quantity(0) == "1"

    def test_totals_section_shows_correct_total(self, page, base_url):
        """Totals footer should display the correct cart total."""
        self._add_macbook_to_cart(page, base_url)
        cp = CartPage(page, base_url)
        cp.open()
        assert cp.get_cart_total() == self.EXPECTED_PRICE

    def test_empty_cart_shows_message(self, page, base_url):
        """Empty cart should show 'Your shopping cart is empty!' message."""
        cp = CartPage(page, base_url)
        cp.open()
        cp.verify_empty_cart()


# ================================================================
# Data-Driven: Add to Cart (products without required options)
# ================================================================
@pytest.mark.cart
@pytest.mark.regression
class TestAddToCartDataDriven:
    """Verify each product can be added to cart and appears correctly.

    Uses cart_data.csv which contains products that can be added
    without filling in required options (MacBook, iPhone).
    """

    @pytest.mark.parametrize(
        "row",
        CART_CSV_DATA,
        ids=[row["test_id"] for row in CART_CSV_DATA],
    )
    def test_add_product_and_verify_in_cart(self, page, base_url, row):
        """Add product from product page and verify it appears in cart."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))
        pp.add_to_cart()
        page.wait_for_selector(".alert-success", timeout=5000)

        cp = CartPage(page, base_url)
        cp.open()

        names = cp.get_product_names()
        assert row["name"] in names, (
            f"[{row['test_id']}] '{row['name']}' should appear in cart, "
            f"found: {names}"
        )
        assert cp.get_unit_price(0) == row["unit_price"], (
            f"[{row['test_id']}] Unit price should be {row['unit_price']}"
        )


# ================================================================
# Cart Interactions (single product — MacBook)
# ================================================================
@pytest.mark.cart
@pytest.mark.regression
class TestCartInteractions:
    """Test cart interaction actions using one product (MacBook)."""

    PRODUCT_ID = 43

    def _add_macbook_and_go_to_cart(self, page, base_url) -> CartPage:
        """Helper: add MacBook and navigate to cart."""
        pp = ProductPage(page, base_url)
        pp.open(self.PRODUCT_ID)
        pp.add_to_cart()
        page.wait_for_selector(".alert-success", timeout=5000)
        cp = CartPage(page, base_url)
        cp.open()
        return cp

    def test_update_quantity(self, page, base_url):
        """Updating quantity should reflect in the quantity input."""
        cp = self._add_macbook_and_go_to_cart(page, base_url)
        cp.update_quantity(2, 0)
        assert cp.get_product_quantity(0) == "2", (
            "Quantity should update to 2 after edit"
        )

    def test_remove_item_makes_cart_empty(self, page, base_url):
        """Removing the only item should show empty cart message."""
        cp = self._add_macbook_and_go_to_cart(page, base_url)
        cp.remove_item(0)
        cp.verify_empty_cart()

    def test_view_cart_from_header_widget(self, page, base_url):
        """Clicking 'View Cart' in header widget should navigate to cart page."""
        pp = ProductPage(page, base_url)
        pp.open(self.PRODUCT_ID)
        pp.add_to_cart()
        page.wait_for_selector(".alert-success", timeout=5000)

        cp = CartPage(page, base_url)
        cp.click_view_cart_in_widget()

        assert "checkout/cart" in cp.get_url(), (
            "Should navigate to the cart page via header widget"
        )
