"""
LoginPage - Page Object for the OpenCart user login page.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):
    """Page object for the OpenCart login page."""

    # Locators
    PAGE_HEADING = "#content h1"
    EMAIL_INPUT = "#input-email"
    PASSWORD_INPUT = "#input-password"
    LOGIN_BUTTON = "button[type='submit']"
    FORGOTTEN_PASSWORD_LINK = "a:has-text('Forgotten Password')"
    ERROR_ALERT = ".alert-danger"
    MY_ACCOUNT_HEADING = "#content h2"
    REGISTER_LINK = "a:has-text('Continue')"

    LOGIN_URL_PATH = "/index.php?route=account/login"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the login page."""
        self.navigate(f"{self.base_url}{self.LOGIN_URL_PATH}")

    def login(self, email: str, password: str):
        """Fill in login credentials and submit."""
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_login_successful(self) -> bool:
        """Check if login was successful by verifying account page heading."""
        self.page.wait_for_load_state("networkidle")
        return "account" in self.get_url().lower()

    def get_error_message(self) -> str:
        """Return the error alert message, if any."""
        if self.is_visible(self.ERROR_ALERT):
            return self.get_text(self.ERROR_ALERT).strip()
        return ""

    def click_forgotten_password(self):
        """Click the Forgotten Password link."""
        self.click(self.FORGOTTEN_PASSWORD_LINK)
