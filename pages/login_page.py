"""
LoginPage - Page Object for the OpenCart user login page.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class LoginPage(BasePage):
    """Page object for the OpenCart login page."""

    LOGIN_URL_PATH = "index.php?route=account/login&language=en-gb"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the login page."""
        self.navigate(f"{self.base_url}{self.LOGIN_URL_PATH}")

    # ── Visibility checks ──────────────────────────────────────────

    def verify_returning_customer_heading_visible(self):
        """Assert that the 'Returning Customer' heading is visible."""
        expect(self.page.get_by_role("heading", name="Returning Customer")).to_be_visible()

    def verify_returning_customer_text_visible(self):
        """Assert that the 'I am a returning customer' text is visible."""
        expect(self.page.get_by_text("I am a returning customer")).to_be_visible()

    def verify_email_input_visible(self):
        """Assert that the E-Mail Address input field is visible."""
        expect(self.page.get_by_role("textbox", name="E-Mail Address")).to_be_visible()

    def verify_password_label_visible(self):
        """Assert that the 'Password' label text is visible."""
        expect(self.page.get_by_text("Password", exact=True)).to_be_visible()

    def verify_password_input_visible(self):
        """Assert that the Password input field is visible."""
        expect(self.page.get_by_role("textbox", name="Password")).to_be_visible()

    def verify_forgotten_password_link_visible(self):
        """Assert that the Forgotten Password link is visible."""
        expect(
            self.page.locator("#form-login").get_by_role("link", name="Forgotten Password")
        ).to_be_visible()

    def verify_login_button_visible(self):
        """Assert that the Login button is visible."""
        expect(self.page.get_by_role("button", name="Login")).to_be_visible()

    def verify_all_fields_visible(self):
        """Assert that all login form fields and elements are visible."""
        self.verify_returning_customer_heading_visible()
        self.verify_returning_customer_text_visible()
        self.verify_email_input_visible()
        self.verify_password_label_visible()
        self.verify_password_input_visible()
        self.verify_forgotten_password_link_visible()
        self.verify_login_button_visible()

    # ── Form actions ───────────────────────────────────────────────

    def login(self, email: str, password: str):
        """Fill in login credentials and submit."""
        self.page.get_by_role("textbox", name="E-Mail Address").fill(email)
        self.page.get_by_role("textbox", name="Password").fill(password)
        self.page.get_by_role("button", name="Login").click()

    def is_login_successful(self) -> bool:
        """Check if login was successful by verifying redirect to account page.

        After login the URL contains a dynamic customer_token, e.g.
        /index.php?route=account/account&language=en-gb&customer_token=<random>
        """
        self.page.wait_for_load_state("networkidle")
        url = self.get_url().lower()
        return "route=account/account" in url and "customer_token" in url

    def get_error_message(self) -> str:
        """Return the error alert message, if any."""
        alert = self.page.locator(".alert-danger")
        if alert.is_visible():
            return (alert.text_content() or "").strip()
        return ""

    def click_forgotten_password(self):
        """Click the Forgotten Password link."""
        self.page.locator("#form-login").get_by_role("link", name="Forgotten Password").click()

    def logout(self):
        """Logout by clicking My Account dropdown then Logout link."""
        self.page.get_by_role("link", name=" My Account ").click()
        self.page.get_by_role("link", name="Logout").click()
        self.page.wait_for_load_state("networkidle")

    def is_logout_successful(self) -> bool:
        """Check if logout was successful by verifying the logout confirmation page."""
        heading = self.page.locator("#content h1").text_content() or ""
        return "logout" in heading.lower()
