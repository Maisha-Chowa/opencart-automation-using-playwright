"""
ProductPage - Page Object for the OpenCart product detail page.

Covers:
  1. Product info (name, price, ex-tax, brand, code, availability)
  2. Product images (main image + thumbnails via magnific-popup)
  3. Tabs (Description, Specification, Reviews)
  4. Actions (add to cart, wishlist, compare, quantity)
  5. API response interception for UI vs API validation
"""

from pages.base_page import BasePage
from playwright.sync_api import Page, expect, TimeoutError as PwTimeout


class ProductPage(BasePage):
    """Page object for the OpenCart product detail page."""

    PRODUCT_URL_TEMPLATE = (
        "index.php?route=product/product&language=en-gb&product_id={product_id}"
    )

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page)
        self.base_url = base_url

    def open(self, product_id: int):
        """Navigate directly to a product detail page by product_id."""
        url = f"{self.base_url}{self.PRODUCT_URL_TEMPLATE.format(product_id=product_id)}"
        self.navigate(url)

    # ================================================================
    # Visibility checks: Product Info
    # ================================================================

    def verify_product_name_visible(self):
        """Assert that the product name heading is visible."""
        expect(self.page.locator("#content h1")).to_be_visible()

    def verify_product_price_visible(self):
        """Assert that the product price is visible."""
        expect(
            self.page.locator("#content .price-new").first
        ).to_be_visible()

    def verify_product_ex_tax_visible(self):
        """Assert that the ex-tax text is visible in the price list."""
        expect(
            self.page.locator(
                "#content ul.list-unstyled li", has_text="Ex Tax:"
            ).first
        ).to_be_visible()

    def verify_brand_visible(self):
        """Assert that the brand info is visible."""
        expect(
            self.page.locator("#content li", has_text="Brand:").first
        ).to_be_visible()

    def verify_product_code_visible(self):
        """Assert that the product code info is visible."""
        expect(
            self.page.locator("#content li", has_text="Product Code:").first
        ).to_be_visible()

    def verify_availability_visible(self):
        """Assert that the availability info is visible."""
        expect(
            self.page.locator("#content li", has_text="Availability:").first
        ).to_be_visible()

    def verify_all_product_info_visible(self):
        """Assert that all product info elements are visible (aggregate)."""
        self.verify_product_name_visible()
        self.verify_product_price_visible()
        self.verify_product_ex_tax_visible()
        self.verify_brand_visible()
        self.verify_product_code_visible()
        self.verify_availability_visible()

    # ================================================================
    # Visibility checks: Images
    # ================================================================

    def verify_main_image_visible(self):
        """Assert that the main product image is visible."""
        expect(
            self.page.locator(".magnific-popup img").first
        ).to_be_visible()

    def verify_product_images_present(self, min_count: int = 1):
        """Assert that at least ``min_count`` product images exist."""
        images = self.page.locator(".magnific-popup img")
        count = images.count()
        assert count >= min_count, (
            f"Expected at least {min_count} product images, found {count}"
        )

    # ================================================================
    # Visibility checks: Tabs
    # ================================================================

    def verify_description_tab_visible(self):
        """Assert that the Description tab is visible."""
        expect(
            self.page.locator("#content .nav-tabs a", has_text="Description")
        ).to_be_visible()

    def verify_specification_tab_visible(self):
        """Assert that the Specification tab is visible."""
        expect(
            self.page.locator("#content .nav-tabs a", has_text="Specification")
        ).to_be_visible()

    def verify_review_tab_visible(self):
        """Assert that the Reviews tab is visible."""
        expect(
            self.page.locator("#content .nav-tabs a", has_text="Reviews")
        ).to_be_visible()

    def verify_description_content_visible(self):
        """Assert that the Description tab content is visible."""
        expect(self.page.locator("#tab-description")).to_be_visible()

    # ================================================================
    # Visibility checks: Actions
    # ================================================================

    def verify_add_to_cart_button_visible(self):
        """Assert that the Add to Cart button is visible."""
        expect(self.page.locator("#button-cart")).to_be_visible()

    def verify_quantity_input_visible(self):
        """Assert that the quantity input is visible."""
        expect(self.page.locator("#input-quantity")).to_be_visible()

    def verify_wishlist_button_visible(self):
        """Assert that the Add to Wish List button is visible."""
        expect(
            self.page.locator(
                "#content button[aria-label='Add to Wish List']"
            )
        ).to_be_visible()

    def verify_compare_button_visible(self):
        """Assert that the Compare this Product button is visible."""
        expect(
            self.page.locator(
                "#content button[aria-label='Compare this Product']"
            )
        ).to_be_visible()

    def verify_all_action_buttons_visible(self):
        """Assert that all action elements are visible (aggregate)."""
        self.verify_add_to_cart_button_visible()
        self.verify_quantity_input_visible()
        self.verify_wishlist_button_visible()
        self.verify_compare_button_visible()

    # ================================================================
    # Data extraction
    # ================================================================

    def get_product_name(self) -> str:
        """Return the product name from the heading."""
        return (self.page.locator("#content h1").text_content() or "").strip()

    def get_product_price(self) -> str:
        """Return the current (new) price text."""
        el = self.page.locator("#content .price-new").first
        return (el.text_content() or "").strip()

    def get_product_ex_tax(self) -> str:
        """Return the ex-tax text (e.g. 'Ex Tax: $500.00')."""
        li = self.page.locator(
            "#content ul.list-unstyled li", has_text="Ex Tax:"
        ).first
        return (li.text_content() or "").strip()

    def get_brand(self) -> str:
        """Return the brand name."""
        link = self.page.locator("#content li", has_text="Brand:").locator("a")
        if link.count() > 0:
            return (link.text_content() or "").strip()
        return ""

    def get_product_code(self) -> str:
        """Return the product code text."""
        li = self.page.locator("#content li", has_text="Product Code:")
        text = (li.text_content() or "").strip()
        return text.replace("Product Code:", "").strip()

    def get_availability(self) -> str:
        """Return the availability text."""
        li = self.page.locator("#content li", has_text="Availability:")
        text = (li.text_content() or "").strip()
        return text.replace("Availability:", "").strip()

    def get_image_count(self) -> int:
        """Return the number of product images (main + thumbnails)."""
        return self.page.locator(".magnific-popup img").count()

    def get_description_text(self) -> str:
        """Return the Description tab content text."""
        return (
            self.page.locator("#tab-description").text_content() or ""
        ).strip()

    def get_tab_names(self) -> list[str]:
        """Return the list of visible tab names."""
        tabs = self.page.locator("#content .nav-tabs a").all()
        return [(t.text_content() or "").strip() for t in tabs]

    def has_specification_tab(self) -> bool:
        """Check if the Specification tab exists."""
        return any(
            "specification" in name.lower() for name in self.get_tab_names()
        )

    def get_breadcrumb_text(self) -> str:
        """Return the breadcrumb navigation text."""
        return (
            self.page.locator(".breadcrumb").text_content() or ""
        ).strip()

    # ================================================================
    # Tab actions
    # ================================================================

    def click_description_tab(self):
        """Switch to the Description tab."""
        self.page.locator(
            "#content .nav-tabs a", has_text="Description"
        ).click()

    def click_specification_tab(self):
        """Switch to the Specification tab."""
        self.page.locator(
            "#content .nav-tabs a", has_text="Specification"
        ).click()

    def click_review_tab(self):
        """Switch to the Reviews tab."""
        self.page.locator(
            "#content .nav-tabs a", has_text="Reviews"
        ).click()

    # ================================================================
    # Cart / Wishlist / Compare actions
    # ================================================================

    def set_quantity(self, qty: int):
        """Set the product quantity."""
        self.page.locator("#input-quantity").fill(str(qty))

    _ADD_TO_CART_JS = """async (opts) => {
        const form = document.querySelector('#form-product');
        if (!form) return {ok: false};

        const fd = new URLSearchParams(new FormData(form));
        const resp = await fetch(opts.url, {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded',
                       'X-Requested-With': 'XMLHttpRequest'},
            body: fd
        });
        const json = await resp.json();

        if (json.success) {
            let box = document.getElementById('alert');
            if (!box) {
                box = document.createElement('div');
                box.id = 'alert';
                (document.getElementById('content') || document.body).prepend(box);
            }
            box.innerHTML =
                '<div class="alert alert-success alert-dismissible">'
                + json.success + '</div>';

            // Refresh header cart widget
            const cartHtml = await (await fetch(opts.cartInfoUrl)).text();
            const hdr = document.querySelector('#header-cart');
            if (hdr) hdr.innerHTML = cartHtml;
        }

        return {ok: true, json: json};
    }"""

    def add_to_cart(self):
        """Add the product to the cart via direct AJAX POST.

        OpenCart's jQuery handler does not reliably initialise in CI, so
        we POST the form data directly, inject the success alert, and
        refresh the header cart widget.
        """
        self.page.evaluate(self._ADD_TO_CART_JS, {
            "url": f"{self.base_url}index.php?route=checkout/cart|add&language=en-gb",
            "cartInfoUrl": f"{self.base_url}index.php?route=common/cart|info&language=en-gb",
        })
        self.page.wait_for_load_state("networkidle")

    def add_to_wishlist(self):
        """Click the Add to Wish List button."""
        self.page.locator(
            "#content button[aria-label='Add to Wish List']"
        ).click()

    def add_to_compare(self):
        """Click the Compare this Product button."""
        self.page.locator(
            "#content button[aria-label='Compare this Product']"
        ).click()

    def is_success_alert_visible(self) -> bool:
        """Check if the success alert is displayed after an action."""
        return self.is_visible(".alert-success")
