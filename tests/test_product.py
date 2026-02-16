"""
Test Suite: Product Page
Covers visibility checks, data-driven tests from product_data.csv,
and API response validation against the UI.
"""

import time

import pytest
from pages.product_page import ProductPage
from utilities.csv_reader import read_csv

# ── Load CSV data once ──────────────────────────────────────────
PRODUCT_CSV_DATA = read_csv("product_data.csv")


# Set to 0 when  no longer need visual debugging.
VISUAL_DELAY = 2


# ================================================================
# Visibility Tests (using MacBook product_id=43 as reference)
# ================================================================
@pytest.mark.ui
@pytest.mark.regression
class TestProductPageVisibility:
    """Verify all product page elements are visible."""

    def test_all_product_info_visible(self, page, base_url):
        """All product info elements should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_all_product_info_visible()

    def test_product_name_visible(self, page, base_url):
        """Product name heading should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_product_name_visible()

    def test_product_price_visible(self, page, base_url):
        """Product price should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_product_price_visible()

    def test_product_ex_tax_visible(self, page, base_url):
        """Ex-tax text should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_product_ex_tax_visible()

    def test_brand_visible(self, page, base_url):
        """Brand info should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_brand_visible()

    def test_product_code_visible(self, page, base_url):
        """Product code should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_product_code_visible()

    def test_availability_visible(self, page, base_url):
        """Availability info should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_availability_visible()

    def test_main_image_visible(self, page, base_url):
        """Main product image should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_main_image_visible()

    def test_description_tab_visible(self, page, base_url):
        """Description tab should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_description_tab_visible()

    def test_review_tab_visible(self, page, base_url):
        """Reviews tab should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_review_tab_visible()

    def test_description_content_visible(self, page, base_url):
        """Description tab content should be visible by default."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_description_content_visible()

    def test_all_action_buttons_visible(self, page, base_url):
        """Add to Cart, quantity, wishlist, and compare should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_all_action_buttons_visible()

    def test_add_to_cart_button_visible(self, page, base_url):
        """Add to Cart button should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_add_to_cart_button_visible()

    def test_quantity_input_visible(self, page, base_url):
        """Quantity input should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_quantity_input_visible()

    def test_wishlist_button_visible(self, page, base_url):
        """Wishlist button should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_wishlist_button_visible()

    def test_compare_button_visible(self, page, base_url):
        """Compare button should be visible."""
        pp = ProductPage(page, base_url)
        pp.open(43)
        pp.verify_compare_button_visible()


# ================================================================
# Data-Driven Tests (all values from product_data.csv)
# ================================================================
@pytest.mark.ui
@pytest.mark.regression
class TestProductDataDriven:
    """Data-driven product tests — every product is defined in product_data.csv."""

    @pytest.mark.parametrize(
        "row",
        PRODUCT_CSV_DATA,
        ids=[row["test_id"] for row in PRODUCT_CSV_DATA],
    )
    def test_product_name_matches_csv(self, page, base_url, row):
        """Product name on the page should match CSV data."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))
        time.sleep(VISUAL_DELAY)

        actual_name = pp.get_product_name()
        assert actual_name == row["name"], (
            f"[{row['test_id']}] Expected name '{row['name']}', "
            f"got '{actual_name}'"
        )

    @pytest.mark.parametrize(
        "row",
        PRODUCT_CSV_DATA,
        ids=[row["test_id"] for row in PRODUCT_CSV_DATA],
    )
    def test_product_price_matches_csv(self, page, base_url, row):
        """Product price on the page should match CSV data."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))

        actual_price = pp.get_product_price()
        assert actual_price == row["price"], (
            f"[{row['test_id']}] Expected price '{row['price']}', "
            f"got '{actual_price}'"
        )

    @pytest.mark.parametrize(
        "row",
        PRODUCT_CSV_DATA,
        ids=[row["test_id"] for row in PRODUCT_CSV_DATA],
    )
    def test_product_ex_tax_matches_csv(self, page, base_url, row):
        """Product ex-tax on the page should match CSV data."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))

        actual_tax = pp.get_product_ex_tax()
        assert actual_tax == row["ex_tax"], (
            f"[{row['test_id']}] Expected ex-tax '{row['ex_tax']}', "
            f"got '{actual_tax}'"
        )

    @pytest.mark.parametrize(
        "row",
        PRODUCT_CSV_DATA,
        ids=[row["test_id"] for row in PRODUCT_CSV_DATA],
    )
    def test_product_brand_matches_csv(self, page, base_url, row):
        """Product brand on the page should match CSV data."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))

        actual_brand = pp.get_brand()
        assert actual_brand == row["brand"], (
            f"[{row['test_id']}] Expected brand '{row['brand']}', "
            f"got '{actual_brand}'"
        )

    @pytest.mark.parametrize(
        "row",
        PRODUCT_CSV_DATA,
        ids=[row["test_id"] for row in PRODUCT_CSV_DATA],
    )
    def test_product_code_matches_csv(self, page, base_url, row):
        """Product code on the page should match CSV data."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))

        actual_code = pp.get_product_code()
        assert actual_code == row["product_code"], (
            f"[{row['test_id']}] Expected code '{row['product_code']}', "
            f"got '{actual_code}'"
        )

    @pytest.mark.parametrize(
        "row",
        PRODUCT_CSV_DATA,
        ids=[row["test_id"] for row in PRODUCT_CSV_DATA],
    )
    def test_product_availability_matches_csv(self, page, base_url, row):
        """Product availability on the page should match CSV data."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))

        actual_avail = pp.get_availability()
        assert actual_avail == row["availability"], (
            f"[{row['test_id']}] Expected availability '{row['availability']}', "
            f"got '{actual_avail}'"
        )

    @pytest.mark.parametrize(
        "row",
        PRODUCT_CSV_DATA,
        ids=[row["test_id"] for row in PRODUCT_CSV_DATA],
    )
    def test_product_images_count(self, page, base_url, row):
        """Product should have at least the expected number of images."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))

        min_images = int(row["min_images"])
        pp.verify_product_images_present(min_images)

    @pytest.mark.parametrize(
        "row",
        PRODUCT_CSV_DATA,
        ids=[row["test_id"] for row in PRODUCT_CSV_DATA],
    )
    def test_product_description_contains(self, page, base_url, row):
        """Product description should contain the expected text."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))

        if row["has_description"].lower() == "true":
            desc = pp.get_description_text()
            expected = row["description_contains"]
            assert expected.lower() in desc.lower(), (
                f"[{row['test_id']}] Description should contain "
                f"'{expected}', got: '{desc[:100]}...'"
            )

    @pytest.mark.parametrize(
        "row",
        PRODUCT_CSV_DATA,
        ids=[row["test_id"] for row in PRODUCT_CSV_DATA],
    )
    def test_product_specification_tab_presence(self, page, base_url, row):
        """Specification tab should match expected presence from CSV."""
        pp = ProductPage(page, base_url)
        pp.open(int(row["product_id"]))

        expected_has_spec = row["has_specification"].lower() == "true"
        actual_has_spec = pp.has_specification_tab()
        assert actual_has_spec == expected_has_spec, (
            f"[{row['test_id']}] Specification tab expected={expected_has_spec}, "
            f"actual={actual_has_spec}"
        )


# ================================================================
# Server Response vs UI Tests (single product – MacBook, ID=43)
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
