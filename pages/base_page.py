"""
BasePage - Common page actions and utilities shared across all page objects.

Includes a portable AJAX form-submission helper that bypasses OpenCart 4.x's
``data-oc-toggle="ajax"`` / jQuery handlers.  In CI the OpenCart JavaScript
framework sometimes fails to attach its event handlers, so every AJAX
interaction is done via the browser Fetch API instead.
"""

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects with common helper methods."""

    # JS executed inside page.evaluate().  Accepts an options dict:
    #   formSelector  – CSS selector for the <form>
    #   url           – (optional) override POST URL; defaults to form.action
    #   extraData     – (optional) dict of extra key/value pairs to append
    #   reload        – (optional) {url, target} to fetch HTML and inject
    _OC_SUBMIT_JS = """async (opts) => {
        const form = document.querySelector(opts.formSelector);
        if (!form) return {ok: false, reason: 'form not found'};

        const fd = new URLSearchParams(new FormData(form));
        if (opts.extraData) {
            for (const [k, v] of Object.entries(opts.extraData)) fd.set(k, v);
        }

        const resp = await fetch(opts.url || form.action, {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded',
                       'X-Requested-With': 'XMLHttpRequest'},
            body: fd
        });
        const json = await resp.json();

        // ── Clear previous state ──
        form.querySelectorAll('.is-invalid').forEach(
            el => el.classList.remove('is-invalid'));
        form.querySelectorAll('.invalid-feedback').forEach(
            el => el.classList.remove('d-block'));
        document.querySelectorAll('#alert .alert').forEach(el => el.remove());

        // ── Errors ──
        if (json.error) {
            const showAlert = (msg) => {
                let box = document.getElementById('alert');
                if (!box) {
                    box = document.createElement('div');
                    box.id = 'alert';
                    (document.getElementById('content') || document.body)
                        .prepend(box);
                }
                box.innerHTML +=
                    '<div class="alert alert-danger alert-dismissible">'
                    + msg + '</div>';
            };

            if (typeof json.error === 'string') {
                showAlert(json.error);
            } else {
                for (const [key, msg] of Object.entries(json.error)) {
                    if (key === 'warning') { showAlert(msg); continue; }
                    const dashKey = key.replaceAll('_', '-');
                    const el = document.getElementById('error-' + dashKey);
                    if (el) { el.classList.add('d-block'); el.textContent = msg; }
                    const inp = document.getElementById('input-' + dashKey);
                    if (inp) inp.classList.add('is-invalid');
                }
            }
        }

        // ── Success alert ──
        if (json.success) {
            let box = document.getElementById('alert');
            if (!box) {
                box = document.createElement('div');
                box.id = 'alert';
                (document.getElementById('content') || document.body)
                    .prepend(box);
            }
            box.innerHTML =
                '<div class="alert alert-success alert-dismissible">'
                + json.success + '</div>';
        }

        // ── Reload a target element (mirrors data-oc-load / data-oc-target) ──
        if (opts.reload) {
            const html = await (await fetch(opts.reload.url)).text();
            const tgt = document.querySelector(opts.reload.target);
            if (tgt) tgt.innerHTML = html;
        }

        return {ok: true, json: json, redirect: json.redirect || null};
    }"""

    def _oc_submit(self, form_selector: str, *,
                   url: str | None = None,
                   extra_data: dict | None = None,
                   reload: dict | None = None) -> dict:
        """Submit an OpenCart AJAX form via the Fetch API.

        Returns the parsed JSON response dict (wrapped in ``{ok, json, redirect}``).
        """
        opts: dict = {"formSelector": form_selector}
        if url:
            opts["url"] = url
        if extra_data:
            opts["extraData"] = extra_data
        if reload:
            opts["reload"] = reload
        return self.page.evaluate(self._OC_SUBMIT_JS, opts) or {}

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
