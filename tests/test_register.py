"""
Test Suite: User Registration
Covers visibility, positive, negative, blank, and CSV data-driven tests.
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


@pytest.mark.account
@pytest.mark.regression
class TestRegisterPositive:
    """Positive registration tests."""

    @pytest.mark.smoke
    def test_successful_registration(self, page, base_url):
        """A new user can register with valid data."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.register(
            first_name="Test",
            last_name="User",
            email=generate_unique_email("success"),
            password="Test@1234",
            agree_privacy=True,
        )
        time.sleep(VISUAL_DELAY)
        assert rp.is_registration_successful(), "Registration should be successful"

    def test_registration_with_long_valid_data(self, page, base_url):
        """Registration succeeds with maximum-length valid input."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.register(
            first_name="A" * 32,
            last_name="B" * 32,
            email=generate_unique_email("longdata"),
            password="ValidPass@123",
            agree_privacy=True,
        )
        time.sleep(VISUAL_DELAY)
        assert rp.is_registration_successful(), "Registration with long valid data should succeed"


@pytest.mark.account
@pytest.mark.regression
class TestRegisterNegative:
    """Negative registration tests."""

    def test_register_with_invalid_email(self, page, base_url):
        """Registration should fail with a malformed email."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.register(
            first_name="Test",
            last_name="User",
            email="invalid-email",
            password="Test@1234",
            agree_privacy=True,
        )
        time.sleep(VISUAL_DELAY)
        errors = rp.get_field_errors()
        page_error = rp.get_error_message()
        all_errors = " ".join(errors) + " " + page_error
        assert "e-mail" in all_errors.lower() or len(errors) > 0, (
            f"Expected email error, got field errors: {errors}, page error: '{page_error}'"
        )

    def test_register_with_short_password(self, page, base_url):
        """Registration should fail with a password that is too short."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.register(
            first_name="Test",
            last_name="User",
            email=generate_unique_email("shortpw"),
            password="12",
            agree_privacy=True,
        )
        time.sleep(VISUAL_DELAY)
        errors = rp.get_field_errors()
        page_error = rp.get_error_message()
        all_errors = " ".join(errors) + " " + page_error
        assert "password" in all_errors.lower() or len(errors) > 0, (
            f"Expected password error, got field errors: {errors}, page error: '{page_error}'"
        )

    def test_register_without_privacy_policy(self, page, base_url):
        """Registration should fail when privacy policy is not accepted."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.register(
            first_name="Test",
            last_name="User",
            email=generate_unique_email("noprivacy"),
            password="Test@1234",
            agree_privacy=False,
        )
        time.sleep(VISUAL_DELAY)
        page_error = rp.get_error_message()
        errors = rp.get_field_errors()
        assert page_error or len(errors) > 0, (
            f"Expected privacy warning, got page error: '{page_error}', field errors: {errors}"
        )

    def test_register_with_existing_email(self, page, base_url):
        """Registration should fail when email is already registered."""
        rp = RegisterPage(page, base_url)
        rp.open()

        # First registration
        email = generate_unique_email("duplicate")
        rp.register(first_name="First", last_name="User", email=email, password="Test@1234")
        time.sleep(VISUAL_DELAY)

        # After successful registration the user is logged in.
        # Log out via My Account dropdown → Logout
        page.goto(base_url)
        page.locator("a.dropdown-toggle", has_text="My Account").first.click()
        page.get_by_role("link", name="Logout").click()
        page.wait_for_load_state("networkidle")

        # Second registration with the same email
        rp.open()
        rp.register(first_name="Second", last_name="User", email=email, password="Test@1234")
        time.sleep(VISUAL_DELAY)

        error = rp.get_error_message()
        assert error, "Should show error for duplicate email registration"


@pytest.mark.account
@pytest.mark.regression
class TestRegisterBlankFields:
    """Blank / empty field registration tests."""

    def test_register_with_blank_first_name(self, page, base_url):
        """Registration should fail when first name is empty."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.register(
            first_name="",
            last_name="User",
            email=generate_unique_email("nofirst"),
            password="Test@1234",
        )
        time.sleep(VISUAL_DELAY)
        errors = rp.get_field_errors()
        page_error = rp.get_error_message()
        assert len(errors) > 0 or page_error, (
            f"Should show validation error for blank first name. "
            f"Field errors: {errors}, page error: '{page_error}'"
        )

    def test_register_with_blank_last_name(self, page, base_url):
        """Registration should fail when last name is empty."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.register(
            first_name="Test",
            last_name="",
            email=generate_unique_email("nolast"),
            password="Test@1234",
        )
        time.sleep(VISUAL_DELAY)
        errors = rp.get_field_errors()
        page_error = rp.get_error_message()
        assert len(errors) > 0 or page_error, (
            f"Should show validation error for blank last name. "
            f"Field errors: {errors}, page error: '{page_error}'"
        )

    def test_register_with_blank_email(self, page, base_url):
        """Registration should fail when email is empty."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.register(
            first_name="Test",
            last_name="User",
            email="",
            password="Test@1234",
        )
        time.sleep(VISUAL_DELAY)
        errors = rp.get_field_errors()
        page_error = rp.get_error_message()
        assert len(errors) > 0 or page_error, (
            f"Should show validation error for blank email. "
            f"Field errors: {errors}, page error: '{page_error}'"
        )

    def test_register_with_blank_password(self, page, base_url):
        """Registration should fail when password is empty."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.register(
            first_name="Test",
            last_name="User",
            email=generate_unique_email("nopw"),
            password="",
        )
        time.sleep(VISUAL_DELAY)
        errors = rp.get_field_errors()
        page_error = rp.get_error_message()
        assert len(errors) > 0 or page_error, (
            f"Should show validation error for blank password. "
            f"Field errors: {errors}, page error: '{page_error}'"
        )

    def test_register_with_all_fields_blank(self, page, base_url):
        """Registration should fail when all fields are empty."""
        rp = RegisterPage(page, base_url)
        rp.open()
        rp.register(
            first_name="",
            last_name="",
            email="",
            password="",
        )
        time.sleep(VISUAL_DELAY)
        errors = rp.get_field_errors()
        page_error = rp.get_error_message()
        assert len(errors) >= 1 or page_error, (
            f"Should show validation errors for all blank fields. "
            f"Field errors: {errors}, page error: '{page_error}'"
        )


@pytest.mark.account
@pytest.mark.regression
class TestRegisterDataDriven:
    """Data-driven registration tests loaded from register_data.csv."""

    @pytest.mark.parametrize(
        "row",
        REGISTER_CSV_DATA,
        ids=[row["test_id"] for row in REGISTER_CSV_DATA],
    )
    def test_register_from_csv(self, page, base_url, row):
        """Run registration test case defined in CSV."""
        rp = RegisterPage(page, base_url)
        rp.open()

        # Replace {unique_email} placeholder with a real unique email
        email = row["email"]
        if "{unique_email}" in email:
            email = generate_unique_email(row["test_id"])

        agree_privacy = row["agree_privacy"].lower() == "true"

        rp.register(
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=email,
            password=row["password"],
            agree_privacy=agree_privacy,
        )
        time.sleep(VISUAL_DELAY)

        if row["expected_result"] == "pass":
            assert rp.is_registration_successful(), (
                f"[{row['test_id']}] Registration should succeed"
            )
        else:
            # Read page-level error FIRST (alerts auto-dismiss after ~7s)
            page_error = rp.get_error_message()
            field_errors = rp.get_field_errors()
            all_errors = " ".join(field_errors) + " " + page_error
            expected = row["expected_error"]
            assert expected.lower() in all_errors.lower() or len(field_errors) > 0, (
                f"[{row['test_id']}] Expected error containing '{expected}', "
                f"got field errors: {field_errors}, page error: '{page_error}'"
            )
