"""
Test Suite: Product Page

Strategy: Test the *template* using one representative product (MacBook).
If MacBook renders correctly, iPhone / Canon / Cinema use the same code.

Exception: Featured products — one lightweight test per product to verify
the query that pulls them isn't broken.

Classes:
  TestProductPageTemplate      — template structure & data (5 tests, MacBook)
  TestFeaturedProductsIntegrity — each featured product loads correctly (4 tests)
  TestProductServerResponse    — server HTML vs UI (5 tests, MacBook)
Total: 14 tests
"""

import pytest
from pages.product_page import ProductPage
from utilities.csv_reader import read_csv

# ── Load CSV data once ──────────────────────────────────────────
PRODUCT_CSV_DATA = read_csv("product_data.csv")


# ================================================================
# Template Tests (single product — MacBook, ID=43)
# ================================================================
@pytest.mark.ui
@pytest.mark.regression
class TestProductPageTemplate:
    """Verify product page template using one representative product (MacBook).

    If the MacBook page works, the iPhone / Canon / Cinema pages work too
    because they share the same underlying template code.
    """

    PRODUCT_ID = 43

    def test_all_product_info_visible(self, page, base_url):
        """All product info (name, price, brand, code, availability) should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(self.PRODUCT_ID)
        pp.verify_all_product_info_visible()

    def test_product_images_section(self, page, base_url):
        """Main image and thumbnail gallery should be present."""
        pp = ProductPage(page, base_url)
        pp.open(self.PRODUCT_ID)
        pp.verify_main_image_visible()
        pp.verify_product_images_present(1)

    def test_tab_structure(self, page, base_url):
        """Description and Review tabs should be visible; content loads correctly."""
        pp = ProductPage(page, base_url)
        pp.open(self.PRODUCT_ID)
        pp.verify_description_tab_visible()
        pp.verify_review_tab_visible()
        pp.verify_description_content_visible()

    def test_action_buttons_visible(self, page, base_url):
        """Add to Cart, quantity, wishlist, and compare buttons should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(self.PRODUCT_ID)
        pp.verify_all_action_buttons_visible()

    def test_product_data_renders_correctly(self, page, base_url):
        """Product data should render correctly for the representative product."""
        pp = ProductPage(page, base_url)
        pp.open(self.PRODUCT_ID)

        assert pp.get_product_name() == "MacBook"
        assert pp.get_product_price() == "$602.00"
        assert pp.get_product_ex_tax() == "Ex Tax: $500.00"
        assert pp.get_brand() == "Apple"
        assert pp.get_product_code() == "Product 16"
        assert pp.get_availability() == "In Stock"


# ================================================================
# Featured Products Integrity (the exception)
# ================================================================
@pytest.mark.ui
@pytest.mark.regression
class TestFeaturedProductsIntegrity:
    """Verify each featured product page loads — ensures the query works.

    This is the exception to 'test one product': we check that all 4
    featured products resolve to valid, loadable pages with correct names.
    """

    @pytest.mark.parametrize(
        "row",
        PRODUCT_CSV_DATA,
        ids=[row["test_id"] for row in PRODUCT_CSV_DATA],
    )
    def test_featured_product_page_loads_with_correct_name(self, page, base_url, row):
        """Each featured product should load and display its correct name."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))

        actual_name = pp.get_product_name()
        assert actual_name == row["name"], (
            f"[{row['test_id']}] Expected name '{row['name']}', "
            f"got '{actual_name}'"
        )


# ================================================================
# Server Response vs UI (single product — MacBook, ID=43)
# ================================================================
@pytest.mark.ui
@pytest.mark.regression
class TestProductServerResponse:
    """Validate the server-rendered HTML response matches the UI display.

    OpenCart 4.x does not expose a public JSON API for product details.
    These tests intercept the HTML page response returned by the server
    and verify that the rendered DOM matches the raw HTML payload.
    Runs against a single product (MacBook) to avoid redundancy.
    """

    PRODUCT_ID = "43"
    EXPECTED_NAME = "MacBook"
    EXPECTED_PRICE = "$602.00"
    EXPECTED_BRAND = "Apple"
    EXPECTED_DESC = "Intel Core 2 Duo processor"

    def test_server_response_status_and_content_type(self, page, base_url):
        """Server should return HTTP 200 with text/html content type."""
        pp = ProductPage(page, base_url)

        with page.expect_response(
            lambda r: f"product_id={self.PRODUCT_ID}" in r.url
            and r.status == 200
        ) as response_info:
            pp.open(int(self.PRODUCT_ID))

        response = response_info.value
        assert response.status == 200, (
            f"Expected 200, got {response.status}"
        )
        assert "text/html" in response.headers.get("content-type", ""), (
            "Response content-type should be text/html"
        )

    def test_server_html_contains_product_name(self, page, base_url):
        """Server HTML should contain the product name that the UI displays."""
        pp = ProductPage(page, base_url)

        with page.expect_response(
            lambda r: f"product_id={self.PRODUCT_ID}" in r.url
            and r.status == 200
        ) as response_info:
            pp.open(int(self.PRODUCT_ID))

        response_html = response_info.value.text()
        assert self.EXPECTED_NAME in response_html, (
            f"Server HTML should contain '{self.EXPECTED_NAME}'"
        )

        ui_name = pp.get_product_name()
        assert ui_name == self.EXPECTED_NAME, (
            f"UI name '{ui_name}' should match server data "
            f"'{self.EXPECTED_NAME}'"
        )

    def test_server_html_contains_product_price(self, page, base_url):
        """Server HTML should contain the product price that the UI displays."""
        pp = ProductPage(page, base_url)

        with page.expect_response(
            lambda r: f"product_id={self.PRODUCT_ID}" in r.url
            and r.status == 200
        ) as response_info:
            pp.open(int(self.PRODUCT_ID))

        response_html = response_info.value.text()
        assert self.EXPECTED_PRICE in response_html, (
            f"Server HTML should contain price '{self.EXPECTED_PRICE}'"
        )

        ui_price = pp.get_product_price()
        assert ui_price == self.EXPECTED_PRICE, (
            f"UI price '{ui_price}' should match server data "
            f"'{self.EXPECTED_PRICE}'"
        )

    def test_server_html_contains_brand(self, page, base_url):
        """Server HTML should contain the brand name that the UI displays."""
        pp = ProductPage(page, base_url)

        with page.expect_response(
            lambda r: f"product_id={self.PRODUCT_ID}" in r.url
            and r.status == 200
        ) as response_info:
            pp.open(int(self.PRODUCT_ID))

        response_html = response_info.value.text()
        assert self.EXPECTED_BRAND in response_html, (
            f"Server HTML should contain brand '{self.EXPECTED_BRAND}'"
        )

        ui_brand = pp.get_brand()
        assert ui_brand == self.EXPECTED_BRAND, (
            f"UI brand '{ui_brand}' should match server data "
            f"'{self.EXPECTED_BRAND}'"
        )

    def test_server_html_contains_description(self, page, base_url):
        """Server HTML should contain the description that the UI displays."""
        pp = ProductPage(page, base_url)

        with page.expect_response(
            lambda r: f"product_id={self.PRODUCT_ID}" in r.url
            and r.status == 200
        ) as response_info:
            pp.open(int(self.PRODUCT_ID))

        response_html = response_info.value.text()
        assert self.EXPECTED_DESC.lower() in response_html.lower(), (
            f"Server HTML should contain description "
            f"'{self.EXPECTED_DESC}'"
        )

        ui_desc = pp.get_description_text()
        assert self.EXPECTED_DESC.lower() in ui_desc.lower(), (
            f"UI description should contain '{self.EXPECTED_DESC}'"
        )
