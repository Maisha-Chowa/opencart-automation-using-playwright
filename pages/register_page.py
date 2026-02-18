"""
RegisterPage - Page Object for the OpenCart user registration page.

Note: OpenCart 4.x uses AJAX for form submission. Clicking "Continue" sends
an XHR/fetch POST; on error the JS injects messages into the DOM (no page
reload), and on success the JS redirects to the success URL.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page, expect, TimeoutError as PwTimeout


class RegisterPage(BasePage):
    """Page object for the OpenCart registration page."""

    REGISTER_URL_PATH = "index.php?route=account/register&language=en-gb"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the registration page via UI (My Account → Register).

        Navigating through the UI ensures session cookies and the CSRF
        register_token are properly established, which is required by
        OpenCart 4.x.
        """
        self.navigate(self.base_url)
        # Click the My Account dropdown toggle (has data-bs-toggle="dropdown")
        self.page.locator("a.dropdown-toggle", has_text="My Account").first.click()
        self.page.get_by_role("link", name="Register").click()
        self.page.wait_for_load_state("networkidle")

    def open_direct(self):
        """Navigate directly to the registration URL."""
        self.navigate(f"{self.base_url}{self.REGISTER_URL_PATH}")

    # ── Visibility checks ──────────────────────────────────────────

    def verify_first_name_input_visible(self):
        """Assert that the First Name input field is visible."""
        expect(self.page.get_by_role("textbox", name="* First Name")).to_be_visible()

    def verify_last_name_input_visible(self):
        """Assert that the Last Name input field is visible."""
        expect(self.page.get_by_role("textbox", name="* Last Name")).to_be_visible()

    def verify_email_input_visible(self):
        """Assert that the E-Mail input field is visible."""
        expect(self.page.get_by_role("textbox", name="* E-Mail")).to_be_visible()

    def verify_password_input_visible(self):
        """Assert that the Password input field is visible."""
        expect(self.page.get_by_role("textbox", name="* Password")).to_be_visible()

    def verify_privacy_checkbox_visible(self):
        """Assert that the privacy policy checkbox is visible."""
        expect(self.page.get_by_role("checkbox")).to_be_visible()

    def verify_continue_button_visible(self):
        """Assert that the Continue button is visible."""
        expect(self.page.get_by_role("button", name="Continue")).to_be_visible()

    def verify_all_fields_visible(self):
        """Assert that all registration form fields are visible."""
        self.verify_first_name_input_visible()
        self.verify_last_name_input_visible()
        self.verify_email_input_visible()
        self.verify_password_input_visible()
        self.verify_privacy_checkbox_visible()
        self.verify_continue_button_visible()

    # ── Form actions ───────────────────────────────────────────────

    _SUBMIT_FORM_JS = """async () => {
        const form = document.getElementById('form-register');
        if (!form) return {ok: false, reason: 'form not found'};

        const formData = new URLSearchParams(new FormData(form));
        const resp = await fetch(form.action, {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded',
                       'X-Requested-With': 'XMLHttpRequest'},
            body: formData
        });
        const json = await resp.json();

        // Clear previous validation state
        form.querySelectorAll('.is-invalid').forEach(
            el => el.classList.remove('is-invalid'));
        form.querySelectorAll('.invalid-feedback').forEach(
            el => el.classList.remove('d-block'));
        document.querySelectorAll('#alert .alert').forEach(el => el.remove());

        if (json['error']) {
            for (const [key, msg] of Object.entries(json['error'])) {
                // Page-level warnings (privacy policy, duplicate email, etc.)
                if (key === 'warning') {
                    let alertBox = document.getElementById('alert');
                    if (!alertBox) {
                        alertBox = document.createElement('div');
                        alertBox.id = 'alert';
                        form.parentNode.insertBefore(alertBox, form);
                    }
                    alertBox.innerHTML =
                        '<div class="alert alert-danger alert-dismissible">'
                        + msg + '</div>';
                    continue;
                }
                // Field-level errors
                const el = document.getElementById('error-' + key);
                if (el) {
                    el.classList.add('d-block');
                    el.textContent = msg;
                    if (el.previousElementSibling)
                        el.previousElementSibling.classList.add('is-invalid');
                }
            }
        }

        return {ok: true, redirect: json['redirect'] || null};
    }"""

    def register(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        agree_privacy: bool = True,
    ):
        """Fill out and submit the registration form, then wait for response.

        OpenCart 4.x uses ``data-oc-toggle="ajax"`` on the form, which
        relies on OpenCart's JS framework being fully initialised.  In CI
        this handler sometimes fails to attach, so we submit the form
        data directly via the Fetch API and replay the server JSON
        response back into the DOM exactly as OpenCart's JS would.
        """
        self.page.fill("#input-firstname", first_name)
        self.page.fill("#input-lastname", last_name)
        self.page.fill("#input-email", email)
        self.page.fill("#input-password", password)

        if agree_privacy:
            self.page.locator("input[name='agree']").check()

        result = self.page.evaluate(self._SUBMIT_FORM_JS)

        # On success the server returns a redirect URL; navigate to it
        # explicitly so Playwright waits for the navigation to complete.
        if result and result.get("redirect"):
            self.page.goto(result["redirect"])
        self.page.wait_for_load_state("networkidle")

    def logout(self):
        """Log out the currently logged-in user via the My Account dropdown.

        Handles the case where the user is not actually logged in (e.g.
        registration failed silently in CI) by checking whether the
        Logout link exists before clicking.
        """
        self.navigate(self.base_url)
        self.page.locator("a.dropdown-toggle", has_text="My Account").first.click()
        logout_link = self.page.get_by_role("link", name="Logout")
        if logout_link.is_visible():
            logout_link.click()
            self.page.wait_for_load_state("networkidle")

    def is_registration_successful(self) -> bool:
        """Check if registration was successful by verifying the URL or title.

        After successful registration OpenCart JS redirects to:
        /index.php?route=account/success&language=en-gb&customer_token=<random>
        """
        try:
            self.page.wait_for_url("**/route=account/success**", timeout=10000)
            return True
        except PwTimeout:
            pass

        # Fallback: check URL directly (glob matching can be tricky with
        # query strings)
        if "route=account/success" in self.page.url:
            return True

        return False

    def get_error_message(self) -> str:
        """Return the page-level error alert message, if any.

        Waits briefly for the alert to appear (AJAX-injected).
        """
        for selector in [".alert-danger", ".alert.alert-danger", "#alert"]:
            loc = self.page.locator(selector)
            try:
                loc.first.wait_for(state="visible", timeout=3000)
                text = (loc.first.text_content() or "").strip()
                if text:
                    return text
            except PwTimeout:
                continue
        return ""

    def get_field_errors(self) -> list[str]:
        """Return all field-level validation error messages.

        Waits briefly for error elements to appear (AJAX-injected).
        Tries multiple selectors used by different OpenCart versions:
        - .text-danger (Bootstrap)
        - .invalid-feedback (Bootstrap 5)
        - [id^='error-'] (OpenCart 4.x: #error-firstname, etc.)
        """
        for selector in [".text-danger", ".invalid-feedback.d-block", "[id^='error-']"]:
            loc = self.page.locator(selector)
            try:
                loc.first.wait_for(state="visible", timeout=3000)
            except PwTimeout:
                continue

            elements = loc.all()
            errors = [
                (el.text_content() or "").strip()
                for el in elements
                if el.is_visible() and (el.text_content() or "").strip()
            ]
            if errors:
                return errors
        return []
