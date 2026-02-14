"""
Test Suite: User Login / Logout
Covers visibility, positive, negative, blank, and CSV data-driven tests.
"""

import pytest
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utilities.test_data import generate_unique_email
from utilities.csv_reader import read_csv

# ── Load CSV data once ──────────────────────────────────────────
LOGIN_CSV_DATA = read_csv("login_data.csv")


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


@pytest.mark.account
@pytest.mark.regression
class TestLoginPositive:
    """Positive login tests."""

    @pytest.fixture()
    def registered_user(self, page, base_url):
        """Register a fresh user and return credentials for login tests."""
        rp = RegisterPage(page, base_url)
        rp.open()

        email = generate_unique_email("login_pos")
        password = "Test@1234"

        rp.register(
            first_name="Login",
            last_name="Tester",
            email=email,
            password=password,
            agree_privacy=True,
        )
        rp.page.wait_for_load_state("networkidle")

        # Logout after registration so we can test login
        lp = LoginPage(page, base_url)
        lp.logout()

        return {"email": email, "password": password}

    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, page, base_url, registered_user):
        """A registered user can log in successfully."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.login(registered_user["email"], registered_user["password"])
        assert lp.is_login_successful(), "Should redirect to account page after login"

    def test_logout_successfully(self, page, base_url, registered_user):
        """A logged-in user can logout and sees confirmation."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.login(registered_user["email"], registered_user["password"])
        assert lp.is_login_successful(), "Login should succeed before testing logout"

        lp.logout()
        assert lp.is_logout_successful(), "Should see logout confirmation page"


@pytest.mark.account
@pytest.mark.regression
class TestLoginNegative:
    """Negative login tests."""

    def test_login_with_wrong_password(self, page, base_url):
        """Login should fail with incorrect password."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.login("user@gmail.com", "WrongPass123")
        error = lp.get_error_message()
        assert "warning" in error.lower(), f"Expected warning, got: {error}"

    def test_login_with_unregistered_email(self, page, base_url):
        """Login should fail with an email that is not registered."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.login("nonexistent_9999@example.com", "Test@1234")
        error = lp.get_error_message()
        assert "warning" in error.lower(), f"Expected warning, got: {error}"

    def test_login_with_invalid_email_format(self, page, base_url):
        """Login should fail with a malformed email."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.login("not-an-email", "Test@1234")
        error = lp.get_error_message()
        assert "warning" in error.lower(), f"Expected warning, got: {error}"


@pytest.mark.account
@pytest.mark.regression
class TestLoginBlankFields:
    """Blank / empty field login tests."""

    def test_login_with_blank_email(self, page, base_url):
        """Login should fail when email is blank."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.login("", "mchowa")
        error = lp.get_error_message()
        assert "warning" in error.lower(), f"Expected warning, got: {error}"

    def test_login_with_blank_password(self, page, base_url):
        """Login should fail when password is blank."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.login("user@gmail.com", "")
        error = lp.get_error_message()
        assert "warning" in error.lower(), f"Expected warning, got: {error}"

    def test_login_with_both_fields_blank(self, page, base_url):
        """Login should fail when both email and password are blank."""
        lp = LoginPage(page, base_url)
        lp.open()
        lp.login("", "")
        error = lp.get_error_message()
        assert "warning" in error.lower(), f"Expected warning, got: {error}"


@pytest.mark.account
@pytest.mark.regression
class TestLoginDataDriven:
    """Data-driven login tests loaded from login_data.csv."""

    @pytest.fixture()
    def registered_user(self, page, base_url):
        """Register a fresh user and return credentials (used by positive CSV rows)."""
        rp = RegisterPage(page, base_url)
        rp.open()

        email = generate_unique_email("login_csv")
        password = "Test@1234"

        rp.register(
            first_name="CSV",
            last_name="Tester",
            email=email,
            password=password,
            agree_privacy=True,
        )
        rp.page.wait_for_load_state("networkidle")

        lp = LoginPage(page, base_url)
        lp.logout()

        return {"email": email, "password": password}

    @pytest.mark.parametrize(
        "row",
        LOGIN_CSV_DATA,
        ids=[row["test_id"] for row in LOGIN_CSV_DATA],
    )
    def test_login_from_csv(self, page, base_url, row, registered_user):
        """Run login test case defined in CSV."""
        lp = LoginPage(page, base_url)
        lp.open()

        # For the positive test, use the freshly registered credentials
        if row["expected_result"] == "pass":
            lp.login(registered_user["email"], registered_user["password"])
            assert lp.is_login_successful(), (
                f"[{row['test_id']}] Login should succeed"
            )
        else:
            lp.login(row["email"], row["password"])
            error = lp.get_error_message()
            expected = row["expected_error"]
            assert expected.lower() in error.lower(), (
                f"[{row['test_id']}] Expected error containing '{expected}', got: '{error}'"
            )
