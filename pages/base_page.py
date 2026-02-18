"""
BasePage - Common page actions and utilities shared across all page objects.

Includes portable AJAX form-submission helpers that bypass OpenCart 4.x's
``data-oc-toggle="ajax"`` / jQuery handlers.  In CI, both in-page
``fetch()`` and Playwright's ``page.request`` API fail to share the PHP
session cookie with the browser.  The only reliable mechanism is native
browser form submission (``form.submit()``), which triggers a real page
navigation and is guaranteed to send cookies.
"""

import json as _json

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects with common helper methods."""

    # ── JS snippets for DOM manipulation ──────────────────────────

    _INJECT_RESPONSE_JS = """(json) => {
        document.querySelectorAll('#alert .alert').forEach(el => el.remove());

        const showAlert = (msg, cls) => {
            let box = document.getElementById('alert');
            if (!box) {
                box = document.createElement('div');
                box.id = 'alert';
                (document.getElementById('content') || document.body).prepend(box);
            }
            box.innerHTML += '<div class="alert ' + cls + ' alert-dismissible">' + msg + '</div>';
        };

        if (json.error) {
            if (typeof json.error === 'string') {
                showAlert(json.error, 'alert-danger');
            } else {
                for (const [key, msg] of Object.entries(json.error)) {
                    if (key === 'warning') { showAlert(msg, 'alert-danger'); continue; }
                    const dashKey = key.replaceAll('_', '-');
                    const el = document.getElementById('error-' + dashKey);
                    if (el) { el.classList.add('d-block'); el.textContent = msg; }
                    const inp = document.getElementById('input-' + dashKey);
                    if (inp) inp.classList.add('is-invalid');
                }
            }
        }
        if (json.success) showAlert(json.success, 'alert-success');
    }"""

    _CLEAR_FORM_ERRORS_JS = """(sel) => {
        const form = document.querySelector(sel);
        if (!form) return;
        form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
        form.querySelectorAll('.invalid-feedback').forEach(el => el.classList.remove('d-block'));
    }"""

    # ── Core helpers: native browser form POST ──────────────────

    def _oc_form_post(self, form_selector: str, url: str | None = None) -> dict | list:
        """Submit an existing DOM form via native browser POST.

        This triggers a real page navigation so the browser's own cookie
        handling is used — the only mechanism that works reliably in CI.
        After reading the JSON body the caller must navigate back.
        """
        js = """([sel, overrideUrl]) => {
            const form = document.querySelector(sel);
            if (!form) return false;
            if (overrideUrl) form.action = overrideUrl;
            form.method = 'POST';
            form.submit();
            return true;
        }"""
        with self.page.expect_navigation(wait_until="networkidle"):
            submitted = self.page.evaluate(js, [form_selector, url or ""])
        if not submitted:
            return {}
        body = self.page.evaluate("() => document.body.innerText")
        try:
            return _json.loads(body)
        except (ValueError, TypeError):
            return {}

    def _oc_data_post(self, url: str, data: dict) -> dict | list:
        """POST arbitrary data via a temporary hidden browser form.

        Creates a hidden ``<form>`` in the DOM, populates it, and submits.
        Same session-cookie guarantee as ``_oc_form_post``.
        """
        js = """([url, data]) => {
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = url;
            form.style.display = 'none';
            for (const [name, value] of Object.entries(data)) {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = name;
                input.value = String(value);
                form.appendChild(input);
            }
            document.body.appendChild(form);
            form.submit();
            return true;
        }"""
        with self.page.expect_navigation(wait_until="networkidle"):
            self.page.evaluate(js, [url, data])
        body = self.page.evaluate("() => document.body.innerText")
        try:
            return _json.loads(body)
        except (ValueError, TypeError):
            return {}

    # ── Standard page object methods ──────────────────────────────

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to a URL and wait for network idle."""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def get_title(self) -> str:
        """Return the page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current URL."""
        return self.page.url

    def click(self, selector: str):
        """Click on an element."""
        self.page.click(selector)

    def fill(self, selector: str, text: str):
        """Clear and fill text into an input field."""
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """Get the text content of an element."""
        return self.page.text_content(selector) or ""

    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        return self.page.is_visible(selector)

    def wait_for_element(self, selector: str, timeout: int = 10000):
        """Wait for an element to be visible."""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def take_screenshot(self, name: str):
        """Take a screenshot and save it to the screenshots directory."""
        self.page.screenshot(path=f"screenshots/{name}.png", full_page=True)

    def expect_element_visible(self, selector: str):
        """Assert that an element is visible using Playwright's expect."""
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text_present(self, selector: str, text: str):
        """Assert that an element contains specific text."""
        expect(self.page.locator(selector)).to_contain_text(text)
