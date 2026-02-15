"""
Test Suite: User Registration
Covers visibility checks and fully data-driven tests from register_data.csv.
"""

import time

import pytest
from pages.register_page import RegisterPage
from utilities.test_data import generate_unique_email
from utilities.csv_reader import read_csv

# ── Load CSV data once ──────────────────────────────────────────
REGISTER_CSV_DATA = read_csv("register_data.csv")

# Delay (seconds) after each form submission so you can visually inspect the result.
# Set to 0 when you no longer need visual debugging.
VISUAL_DELAY = 2


# ── Helper: resolve placeholders in CSV values ──────────────────
def _resolve(value: str, test_id: str, existing_email: str = "") -> str:
    """Replace CSV placeholders with actual runtime values."""
    if "{unique_email}" in value:
        return generate_unique_email(test_id)
    if "{existing_email}" in value:
        return existing_email
    if "{long_32}" in value:
        return value.replace("{long_32}", "A" * 32)
    return value


# ================================================================
# Visibility Tests (no CSV data needed)
# ================================================================
@pytest.mark.account
@pytest.mark.regression
class TestRegisterPageVisibility:
    """Verify all registration form elements are visible."""

    def test_all_fields_visible(self, page, base_url):
        """All form fields should be visible on the registration page."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.verify_all_fields_visible()

    def test_first_name_input_visible(self, page, base_url):
        """First Name input should be visible."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.verify_first_name_input_visible()

    def test_last_name_input_visible(self, page, base_url):
        """Last Name input should be visible."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.verify_last_name_input_visible()

    def test_email_input_visible(self, page, base_url):
        """E-Mail input should be visible."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.verify_email_input_visible()

    def test_password_input_visible(self, page, base_url):
        """Password input should be visible."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.verify_password_input_visible()

    def test_privacy_checkbox_visible(self, page, base_url):
        """Privacy policy checkbox should be visible."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.verify_privacy_checkbox_visible()

    def test_continue_button_visible(self, page, base_url):
        """Continue button should be visible."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.verify_continue_button_visible()


# ================================================================
# Data-Driven Tests (all values from register_data.csv)
# ================================================================
@pytest.mark.account
@pytest.mark.regression
class TestRegisterDataDriven:
    """Data-driven registration tests — every scenario is defined in register_data.csv."""

    @pytest.mark.parametrize(
        "row",
        REGISTER_CSV_DATA,
        ids=[row["test_id"] for row in REGISTER_CSV_DATA],
    )
    def test_register_from_csv(self, page, base_url, row):
        """Run a single registration test case from CSV."""
        rp = RegisterPage(page, base_url)
        test_id = row["test_id"]

        # ── Handle the "existing_email" scenario ────────────────
        # This test needs a pre-registered email, so register first,
        # log out, then attempt to register again with the same email.
        existing_email = ""
        if "{existing_email}" in row["email"]:
            rp.open()
            existing_email = generate_unique_email("dup")
            rp.register(
                first_name="Pre",
                last_name="Registered",
                email=existing_email,
                password="Test@1234",
                agree_privacy=True,
            )
            time.sleep(VISUAL_DELAY)

            # Log out (user is auto-logged-in after registration)
            rp.logout()

        # ── Open register page and fill form with CSV values ────
        rp.open()

        first_name = _resolve(row["first_name"], test_id)
        last_name = _resolve(row["last_name"], test_id)
        email = _resolve(row["email"], test_id, existing_email)
        password = row["password"]
        agree_privacy = row["agree_privacy"].lower() == "true"

        rp.register(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            agree_privacy=agree_privacy,
        )
        time.sleep(VISUAL_DELAY)

        # ── Assert ──────────────────────────────────────────────
        if row["expected_result"] == "pass":
            assert rp.is_registration_successful(), (
                f"[{test_id}] Registration should succeed"
            )
        else:
            # Read page-level error FIRST (alerts auto-dismiss after ~7s)
            page_error = rp.get_error_message()
            field_errors = rp.get_field_errors()
            all_errors = " ".join(field_errors) + " " + page_error
            expected = row["expected_error"]
            assert expected.lower() in all_errors.lower() or len(field_errors) > 0, (
                f"[{test_id}] Expected error containing '{expected}', "
                f"got field errors: {field_errors}, page error: '{page_error}'"
            )
