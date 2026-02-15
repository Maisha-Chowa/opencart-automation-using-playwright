"""
Test Suite: User Login / Logout
Covers visibility checks and fully data-driven tests from login_data.csv.
"""

import time

import pytest
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utilities.test_data import generate_unique_email
from utilities.csv_reader import read_csv

# ── Load CSV data once ──────────────────────────────────────────
LOGIN_CSV_DATA = read_csv("login_data.csv")

# Delay (seconds) after each form submission so you can visually inspect the result.
# Set to 0 when you no longer need visual debugging.
VISUAL_DELAY = 2


# ── Helper: resolve placeholders in CSV values ──────────────────
def _resolve(
    value: str,
    registered_email: str = "",
    registered_password: str = "",
) -> str:
    """Replace CSV placeholders with actual runtime values."""
    if "{registered_email}" in value:
        return registered_email
    if "{registered_password}" in value:
        return registered_password
    return value


# ================================================================
# Visibility Tests (no CSV data needed)
# ================================================================
@pytest.mark.account
@pytest.mark.regression
class TestLoginPageVisibility:
    """Verify all login page elements are visible."""

    def test_all_fields_visible(self, page, base_url):
        """All login form elements should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_all_fields_visible()

    def test_returning_customer_heading_visible(self, page, base_url):
        """'Returning Customer' heading should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_returning_customer_heading_visible()

    def test_returning_customer_text_visible(self, page, base_url):
        """'I am a returning customer' text should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_returning_customer_text_visible()

    def test_email_label_visible(self, page, base_url):
        """'E-Mail Address' label should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_email_label_visible()

    def test_email_input_visible(self, page, base_url):
        """E-Mail Address input should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_email_input_visible()

    def test_password_label_visible(self, page, base_url):
        """Password label should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_password_label_visible()

    def test_password_input_visible(self, page, base_url):
        """Password input should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_password_input_visible()

    def test_forgotten_password_link_visible(self, page, base_url):
        """Forgotten Password link should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_forgotten_password_link_visible()

    def test_login_button_visible(self, page, base_url):
        """Login button should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_login_button_visible()

    def test_new_customer_section_visible(self, page, base_url):
        """'Register Account' section should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_new_customer_section_visible()

    def test_new_customer_description_visible(self, page, base_url):
        """'By creating an account you' description should be visible."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.verify_new_customer_description_visible()


# ================================================================
# Data-Driven Tests (all values from login_data.csv)
# ================================================================
@pytest.mark.account
@pytest.mark.regression
class TestLoginDataDriven:
    """Data-driven login tests — every scenario is defined in login_data.csv."""

    @pytest.fixture(autouse=True)
    def _register_user(self, page, base_url):
        """Register a fresh user before each test and store credentials.

        Each parametrized test gets a new page context, so we register
        a unique user and log out to leave the browser in a clean state.
        """
        rp = RegisterPage(page, base_url)
        rp.open()

        self._registered_email = generate_unique_email("login")
        self._registered_password = "Test@1234"

        rp.register(
            first_name="Login",
            last_name="Tester",
            email=self._registered_email,
            password=self._registered_password,
            agree_privacy=True,
        )
        time.sleep(VISUAL_DELAY)

        # Logout after registration (user is auto-logged-in)
        rp.logout()

    @pytest.mark.parametrize(
        "row",
        LOGIN_CSV_DATA,
        ids=[row["test_id"] for row in LOGIN_CSV_DATA],
    )
    def test_login_from_csv(self, page, base_url, row):
        """Run a single login test case from CSV."""
        lp = LoginPage(page, base_url)
        test_id = row["test_id"]

        # ── Open login page and fill form with CSV values ────
        lp.open()

        email = _resolve(
            row["email"], self._registered_email, self._registered_password
        )
        password = _resolve(
            row["password"], self._registered_email, self._registered_password
        )

        lp.login(email, password)
        time.sleep(VISUAL_DELAY)

        # ── Assert ──────────────────────────────────────────────
        if row["expected_result"] == "pass":
            assert lp.is_login_successful(), (
                f"[{test_id}] Login should succeed"
            )

        elif row["expected_result"] == "pass_logout":
            assert lp.is_login_successful(), (
                f"[{test_id}] Login should succeed before testing logout"
            )
            lp.logout()
            assert lp.is_logout_successful(), (
                f"[{test_id}] Logout should succeed"
            )

        else:
            # Read page-level error (alerts auto-dismiss after ~7s)
            error = lp.get_error_message()
            expected = row["expected_error"]
            assert expected.lower() in error.lower(), (
                f"[{test_id}] Expected error containing '{expected}', "
                f"got: '{error}'"
            )
