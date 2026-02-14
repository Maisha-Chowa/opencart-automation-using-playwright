"""
RegisterPage - Page Object for the OpenCart user registration page.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page


class RegisterPage(BasePage):
    """Page object for the OpenCart registration page."""

    # Locators
    PAGE_HEADING = "#content h1"
    FIRST_NAME_INPUT = "#input-firstname"
    LAST_NAME_INPUT = "#input-lastname"
    EMAIL_INPUT = "#input-email"
    PASSWORD_INPUT = "#input-password"
    NEWSLETTER_TOGGLE = "input[name='newsletter']"
    PRIVACY_POLICY_CHECKBOX = "input[name='agree']"
    CONTINUE_BUTTON = "button[type='submit']"
    SUCCESS_HEADING = "#content h1"
    ERROR_ALERT = ".alert-danger"
    FIELD_ERROR = ".text-danger"

    REGISTER_URL_PATH = "/index.php?route=account/register"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the registration page."""
        self.navigate(f"{self.base_url}{self.REGISTER_URL_PATH}")

    def register(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        agree_privacy: bool = True,
    ):
        """Fill out and submit the registration form."""
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.EMAIL_INPUT, email)
        self.fill(self.PASSWORD_INPUT, password)

        if agree_privacy:
            self.page.locator(self.PRIVACY_POLICY_CHECKBOX).check()

        self.click(self.CONTINUE_BUTTON)

    def is_registration_successful(self) -> bool:
        """Check if registration was successful."""
        self.page.wait_for_load_state("networkidle")
        heading = self.get_text(self.SUCCESS_HEADING)
        return "your account has been created" in heading.lower() if heading else False

    def get_error_message(self) -> str:
        """Return the error alert message, if any."""
        if self.is_visible(self.ERROR_ALERT):
            return self.get_text(self.ERROR_ALERT).strip()
        return ""

    def get_field_errors(self) -> list[str]:
        """Return all field-level validation error messages."""
        elements = self.page.locator(self.FIELD_ERROR).all()
        return [el.text_content() or "" for el in elements]
