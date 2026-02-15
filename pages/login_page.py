"""
LoginPage - Page Object for the OpenCart user login page.

Note: OpenCart 4.x login uses standard form POST. On invalid credentials,
a warning alert is injected at the top of the form. On success, the browser
redirects to the account dashboard with a dynamic customer_token.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page, expect, TimeoutError as PwTimeout


class LoginPage(BasePage):
    """Page object for the OpenCart login page."""

    LOGIN_URL_PATH = "index.php?route=account/login&language=en-gb"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the login page via UI (My Account -> Login).

        Navigating through the UI ensures session cookies are properly
        established, which is required by OpenCart 4.x.
        """
        self.navigate(self.base_url)
        self.page.locator("a.dropdown-toggle", has_text="My Account").first.click()
        self.page.get_by_role("link", name="Login").click()
        self.page.wait_for_load_state("networkidle")

    def open_direct(self):
        """Navigate directly to the login URL."""
        self.navigate(f"{self.base_url}{self.LOGIN_URL_PATH}")

    # ── Visibility checks: Returning Customer (Login Form) ─────────

    def verify_returning_customer_heading_visible(self):
        """Assert that the 'Returning Customer' heading is visible."""
        expect(self.page.get_by_role("heading", name="Returning Customer")).to_be_visible()

    def verify_returning_customer_text_visible(self):
        """Assert that the 'I am a returning customer' text is visible."""
        expect(self.page.get_by_text("I am a returning customer")).to_be_visible()

    def verify_email_label_visible(self):
        """Assert that the 'E-Mail Address' label is visible."""
        expect(
            self.page.locator("#form-login div").filter(has_text="E-Mail Address")
        ).to_be_visible()

    def verify_email_input_visible(self):
        """Assert that the E-Mail Address input field is visible."""
        expect(self.page.get_by_placeholder("E-Mail Address")).to_be_visible()

    def verify_password_label_visible(self):
        """Assert that the 'Password' label text is visible."""
        expect(self.page.get_by_text("Password", exact=True)).to_be_visible()

    def verify_password_input_visible(self):
        """Assert that the Password input field is visible."""
        expect(self.page.get_by_placeholder("Password")).to_be_visible()

    def verify_forgotten_password_link_visible(self):
        """Assert that the Forgotten Password link is visible."""
        expect(
            self.page.locator("#form-login").get_by_role("link", name="Forgotten Password")
        ).to_be_visible()

    def verify_login_button_visible(self):
        """Assert that the Login button is visible."""
        expect(self.page.get_by_role("button", name="Login")).to_be_visible()

    # ── Visibility checks: New Customer Section ────────────────────

    def verify_new_customer_section_visible(self):
        """Assert that the 'Register Account' section is visible."""
        expect(
            self.page.locator("p").filter(has_text="Register Account")
        ).to_be_visible()

    def verify_new_customer_description_visible(self):
        """Assert that the 'By creating an account you' description is visible."""
        expect(self.page.get_by_text("By creating an account you")).to_be_visible()

    # ── Visibility checks: Post-Login (My Account Page) ────────────

    def verify_my_account_heading_visible(self):
        """Assert that the 'My Account' heading is visible after login."""
        expect(
            self.page.locator("#content").get_by_role("heading", name="My Account")
        ).to_be_visible()

    # ── Visibility checks: Logout Page ─────────────────────────────

    def verify_logout_heading_visible(self):
        """Assert that the 'Account Logout' heading is visible."""
        expect(self.page.get_by_role("heading", name="Account Logout")).to_be_visible()

    def verify_logout_continue_link_visible(self):
        """Assert that the 'Continue' link on the logout page is visible."""
        expect(self.page.get_by_role("link", name="Continue")).to_be_visible()

    # ── Aggregate visibility checks ────────────────────────────────

    def verify_all_fields_visible(self):
        """Assert that all login form fields and elements are visible."""
        self.verify_returning_customer_heading_visible()
        self.verify_returning_customer_text_visible()
        self.verify_email_label_visible()
        self.verify_email_input_visible()
        self.verify_password_label_visible()
        self.verify_password_input_visible()
        self.verify_forgotten_password_link_visible()
        self.verify_login_button_visible()
        self.verify_new_customer_section_visible()
        self.verify_new_customer_description_visible()

    # ── Form actions ───────────────────────────────────────────────

    def login(self, email: str, password: str):
        """Fill in login credentials and submit the form."""
        self.page.get_by_placeholder("E-Mail Address").fill(email)
        self.page.get_by_placeholder("Password").fill(password)
        self.page.get_by_role("button", name="Login").click()
        self.page.wait_for_load_state("networkidle")

    def is_login_successful(self) -> bool:
        """Check if login was successful by verifying redirect to account page.

        After login the URL contains a dynamic customer_token, e.g.
        /index.php?route=account/account&language=en-gb&customer_token=<random>
        """
        try:
            self.page.wait_for_url("**/route=account/account**", timeout=10000)
            return True
        except PwTimeout:
            pass

        # Fallback: check URL directly
        if "route=account/account" in self.page.url:
            return True

        return False

    def get_error_message(self) -> str:
        """Return the page-level error alert message, if any.

        Waits briefly for the alert to appear (may be AJAX-injected).
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

    def click_forgotten_password(self):
        """Click the Forgotten Password link."""
        self.page.locator("#form-login").get_by_role(
            "link", name="Forgotten Password"
        ).click()
        self.page.wait_for_load_state("networkidle")

    def logout(self):
        """Log out the currently logged-in user via the My Account dropdown."""
        self.navigate(self.base_url)
        self.page.locator("a.dropdown-toggle", has_text="My Account").first.click()
        self.page.get_by_role("link", name="Logout").click()
        self.page.wait_for_load_state("networkidle")

    def is_logout_successful(self) -> bool:
        """Check if logout was successful by verifying the logout confirmation page."""
        try:
            heading = self.page.locator("#content h1")
            heading.wait_for(state="visible", timeout=5000)
            text = (heading.text_content() or "").strip()
            return "logout" in text.lower()
        except PwTimeout:
            return False
