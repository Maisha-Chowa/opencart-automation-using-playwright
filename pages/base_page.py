"""
BasePage - Common page actions and utilities shared across all page objects.

Includes portable AJAX form-submission helpers that bypass OpenCart 4.x's
``data-oc-toggle="ajax"`` / jQuery handlers.  In CI the OpenCart JavaScript
framework sometimes fails to attach its event handlers, so every AJAX
interaction uses Playwright's ``page.request`` API (which shares the
browser context's cookie jar) instead of in-page ``fetch()``.
"""

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects with common helper methods."""

    # ── JS snippets for injecting server responses into the DOM ────

    _INJECT_ERRORS_JS = """(json) => {
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

    _SET_INNER_HTML_JS = """([selector, html]) => {
        const el = document.querySelector(selector);
        if (el) el.innerHTML = html;
    }"""

    # ── Helpers ────────────────────────────────────────────────────

    @staticmethod
    def _read_form_data(page: Page, form_selector: str) -> dict:
        """Read all form field values as a dict via the browser DOM."""
        return page.evaluate(
            """(sel) => {
                const form = document.querySelector(sel);
                if (!form) return {};
                return Object.fromEntries(new FormData(form));
            }""",
            form_selector,
        )

    @staticmethod
    def _read_form_action(page: Page, form_selector: str) -> str:
        """Read the form's ``action`` attribute."""
        return page.evaluate(
            """(sel) => {
                const form = document.querySelector(sel);
                return form ? form.action : '';
            }""",
            form_selector,
        )

    def _oc_reload_html(self, url: str, target_selector: str):
        """GET HTML via Playwright's request API and inject it into a DOM element."""
        resp = self.page.request.get(url)
        self.page.evaluate(self._SET_INNER_HTML_JS, [target_selector, resp.text()])

    def _oc_post(self, url: str, data: dict) -> dict:
        """POST form data via Playwright's request API (shares session cookies).

        Returns the parsed JSON response body.
        """
        resp = self.page.request.post(url, form=data)
        return resp.json()

    def _oc_submit(self, form_selector: str, *,
                   url: str | None = None,
                   extra_data: dict | None = None) -> dict:
        """Read form data from the DOM, POST it, and inject the JSON
        response (errors / success alerts) back into the page.

        Returns the parsed JSON response (dict or list).
        """
        data = self._read_form_data(self.page, form_selector)
        if extra_data:
            data.update(extra_data)
        post_url = url or self._read_form_action(self.page, form_selector)

        self.page.evaluate(self._CLEAR_FORM_ERRORS_JS, form_selector)

        json_resp = self._oc_post(post_url, data)
        if isinstance(json_resp, dict):
            self.page.evaluate(self._INJECT_ERRORS_JS, json_resp)
        return json_resp

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
