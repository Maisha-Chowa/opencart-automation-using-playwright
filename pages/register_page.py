"""
RegisterPage - Page Object for the OpenCart user registration page.
"""

from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class RegisterPage(BasePage):
    """Page object for the OpenCart registration page."""

    REGISTER_URL_PATH = "index.php?route=account/register&language=en-gb"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self):
        """Navigate to the registration page."""
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

    def register(
        self,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        agree_privacy: bool = True,
    ):
        """Fill out and submit the registration form."""
        self.page.get_by_role("textbox", name="* First Name").fill(first_name)
        self.page.get_by_role("textbox", name="* Last Name").fill(last_name)
        self.page.get_by_role("textbox", name="* E-Mail").fill(email)
        self.page.get_by_role("textbox", name="* Password").fill(password)

        if agree_privacy:
            self.page.get_by_role("checkbox").check()

        self.page.get_by_role("button", name="Continue").click()

    def is_registration_successful(self) -> bool:
        """Check if registration was successful."""
        self.page.wait_for_load_state("networkidle")
        heading = self.page.locator("#content h1").text_content() or ""
        return "your account has been created" in heading.lower()

    def get_error_message(self) -> str:
        """Return the error alert message, if any."""
        alert = self.page.locator(".alert-danger")
        if alert.is_visible():
            return (alert.text_content() or "").strip()
        return ""

    def get_field_errors(self) -> list[str]:
        """Return all field-level validation error messages."""
        elements = self.page.locator(".text-danger").all()
        return [el.text_content() or "" for el in elements]
