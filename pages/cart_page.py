"""
CartPage - Page Object for the OpenCart shopping cart page.

Covers:
  1. Cart page template (heading, table, totals, action buttons)
  2. Product row data (name, model, quantity, unit price, row total)
  3. Cart actions (update quantity, remove item, checkout, continue shopping)
  4. Header cart widget (view cart navigation)

Note: Apple Cinema 30" and Canon EOS 5D have required product options and
cannot be added to cart without filling them in.  Those are excluded from
the basic add-to-cart data-driven tests.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class CartPage(BasePage):
    """Page object for the OpenCart shopping cart page."""

    CART_URL_PATH = "index.php?route=checkout/cart&language=en-gb"

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate directly to the cart page."""
        self.navigate(f"{self.base_url}{self.CART_URL_PATH}")

    # ================================================================
    # Visibility checks: Cart Page Template
    # ================================================================

    def verify_heading_visible(self):
        """Assert that the Shopping Cart heading is visible."""
        expect(self.page.locator("#content h1")).to_be_visible()

    def verify_cart_table_visible(self):
        """Assert that the cart product table is visible."""
        expect(
            self.page.locator("#shopping-cart table.table-bordered")
        ).to_be_visible()

    def verify_quantity_input_visible(self):
        """Assert that the quantity input is visible for the first product."""
        expect(
            self.page.locator(
                '#shopping-cart input[name="quantity"]'
            ).first
        ).to_be_visible()

    def verify_update_button_visible(self):
        """Assert that the Update button is visible."""
        expect(
            self.page.locator(
                '#shopping-cart button[aria-label="Update"]'
            ).first
        ).to_be_visible()

    def verify_remove_button_visible(self):
        """Assert that the Remove button is visible."""
        expect(
            self.page.locator(
                '#shopping-cart button[aria-label="Remove"]'
            ).first
        ).to_be_visible()

    def verify_totals_visible(self):
        """Assert that the totals footer (Sub-Total and Total) is visible."""
        expect(self.page.locator("#checkout-total")).to_be_visible()

    def verify_continue_shopping_visible(self):
        """Assert that the Continue Shopping link is visible."""
        expect(
            self.page.locator('#content a:has-text("Continue Shopping")')
        ).to_be_visible()

    def verify_checkout_button_visible(self):
        """Assert that the Checkout link is visible."""
        expect(
            self.page.locator('#content a:has-text("Checkout")')
        ).to_be_visible()

    def verify_all_cart_elements_visible(self):
        """Assert all populated-cart elements are visible (aggregate)."""
        self.verify_heading_visible()
        self.verify_cart_table_visible()
        self.verify_quantity_input_visible()
        self.verify_update_button_visible()
        self.verify_remove_button_visible()
        self.verify_totals_visible()
        self.verify_continue_shopping_visible()
        self.verify_checkout_button_visible()

    def verify_empty_cart(self):
        """Assert that the cart shows the empty message."""
        expect(
            self.page.locator(
                "#content p", has_text="Your shopping cart is empty"
            )
        ).to_be_visible()

    # ================================================================
    # Data extraction
    # ================================================================

    def get_heading_text(self) -> str:
        """Return the cart page heading text."""
        return (
            self.page.locator("#content h1").text_content() or ""
        ).strip()

    def get_cart_items_count(self) -> int:
        """Return the number of product rows in the cart table."""
        return self.page.locator(
            "#shopping-cart table tbody tr"
        ).count()

    def get_product_names(self) -> list[str]:
        """Return product names from the cart table."""
        links = self.page.locator(
            "#shopping-cart table tbody td:nth-child(2) a"
        ).all()
        return [(el.text_content() or "").strip() for el in links]

    def get_product_model(self, index: int = 0) -> str:
        """Return the model text for a cart row by index."""
        return (
            self.page.locator("#shopping-cart table tbody tr")
            .nth(index)
            .locator("td:nth-child(3)")
            .text_content() or ""
        ).strip()

    def get_product_quantity(self, index: int = 0) -> str:
        """Return the quantity input value for a cart row by index."""
        return (
            self.page.locator('#shopping-cart input[name="quantity"]')
            .nth(index)
            .get_attribute("value") or ""
        )

    def get_unit_price(self, index: int = 0) -> str:
        """Return the unit price text for a cart row by index."""
        return (
            self.page.locator("#shopping-cart table tbody tr")
            .nth(index)
            .locator("td:nth-child(5)")
            .text_content() or ""
        ).strip()

    def get_row_total(self, index: int = 0) -> str:
        """Return the row total text for a cart row by index."""
        return (
            self.page.locator("#shopping-cart table tbody tr")
            .nth(index)
            .locator("td:nth-child(6)")
            .text_content() or ""
        ).strip()

    def get_cart_total(self) -> str:
        """Return the cart Total from the totals footer."""
        row = self.page.locator(
            "#checkout-total tr", has_text="Total"
        ).last
        return (row.locator("td:last-child").text_content() or "").strip()

    def get_sub_total(self) -> str:
        """Return the Sub-Total from the totals footer."""
        row = self.page.locator(
            "#checkout-total tr", has_text="Sub-Total"
        )
        return (row.locator("td:last-child").text_content() or "").strip()

    def get_header_cart_text(self) -> str:
        """Return the header cart button text (e.g. '1 item(s) - $602.00')."""
        return (
            self.page.locator(
                "#header-cart > div > button.btn-inverse"
            ).text_content() or ""
        ).strip()

    # ================================================================
    # Cart actions
    # ================================================================

    _CART_ACTION_JS = """async (opts) => {
        const forms = document.querySelectorAll('#shopping-cart form');
        const form = forms[opts.index];
        if (!form) return {ok: false, reason: 'form not found at index ' + opts.index};

        if (opts.quantity !== undefined) {
            const qtyInput = form.querySelector('input[name="quantity"]');
            if (qtyInput) qtyInput.value = String(opts.quantity);
        }

        const fd = new URLSearchParams(new FormData(form));
        const resp = await fetch(opts.url, {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded',
                       'X-Requested-With': 'XMLHttpRequest'},
            body: fd
        });
        const json = await resp.json();

        if (json.redirect) return {ok: true, json: json, redirect: json.redirect};

        // Reload the cart list (mirrors data-oc-load / data-oc-target)
        const html = await (await fetch(opts.reloadUrl)).text();
        const tgt = document.querySelector('#shopping-cart');
        if (tgt) tgt.innerHTML = html;

        return {ok: true, json: json};
    }"""

    def update_quantity(self, qty: int, index: int = 0):
        """Update the quantity for a cart row via direct AJAX POST."""
        result = self.page.evaluate(self._CART_ACTION_JS, {
            "index": index,
            "quantity": qty,
            "url": f"{self.base_url}index.php?route=checkout/cart|edit&language=en-gb",
            "reloadUrl": f"{self.base_url}index.php?route=checkout/cart|list&language=en-gb",
        })
        if result and result.get("redirect"):
            self.page.goto(result["redirect"])
        self.page.wait_for_load_state("networkidle")

    def remove_item(self, index: int = 0):
        """Remove a product from the cart by index via direct AJAX POST."""
        result = self.page.evaluate(self._CART_ACTION_JS, {
            "index": index,
            "url": f"{self.base_url}index.php?route=checkout/cart|remove&language=en-gb",
            "reloadUrl": f"{self.base_url}index.php?route=checkout/cart|list&language=en-gb",
        })
        if result and result.get("redirect"):
            self.page.goto(result["redirect"])
        self.page.wait_for_load_state("networkidle")

    def click_continue_shopping(self):
        """Click the Continue Shopping link."""
        self.page.locator(
            '#content a:has-text("Continue Shopping")'
        ).click()
        self.page.wait_for_load_state("networkidle")

    def click_checkout(self):
        """Click the Checkout link."""
        self.page.locator('#content a:has-text("Checkout")').click()
        self.page.wait_for_load_state("networkidle")

    def open_header_cart_widget(self):
        """Open the header cart dropdown widget."""
        self.page.locator(
            "#header-cart > div > button.btn-inverse"
        ).click()
        self.page.wait_for_timeout(500)

    def click_view_cart_in_widget(self):
        """Click 'View Cart' in the header cart dropdown."""
        self.open_header_cart_widget()
        self.page.locator(
            '#header-cart a:has-text("View Cart")'
        ).click()
        self.page.wait_for_load_state("networkidle")

    def is_cart_empty(self) -> bool:
        """Check if the cart is empty (backward compatibility)."""
        text = (
            self.page.locator("#content p").first.text_content() or ""
        ).lower()
        return "your shopping cart is empty" in text
