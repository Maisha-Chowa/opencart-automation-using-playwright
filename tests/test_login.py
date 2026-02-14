"""
Test Suite: User Login / Logout
Validates the OpenCart authentication flows.
"""

import pytest
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from utilities.test_data import generate_unique_email, INVALID_LOGIN_DATA


@pytest.mark.account
@pytest.mark.regression
class TestUserLogin:
    """Tests for the user login and logout features."""

    @pytest.fixture()
    def registered_user(self, page, base_url):
        """Register a fresh user and return credentials for login tests."""
        rp = RegisterPage(page, base_url)
        rp.open()

        email = generate_unique_email("login_test")
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
        """Verify a registered user can log in successfully."""
        lp = LoginPage(page, base_url)
        lp.open()

        lp.login(registered_user["email"], registered_user["password"])

        assert lp.is_login_successful(), (
            "User should be redirected to account page after successful login"
        )

    @pytest.mark.parametrize(
        "test_id, email, password, expected_error",
        INVALID_LOGIN_DATA,
        ids=[data[0] for data in INVALID_LOGIN_DATA],
    )
    def test_login_with_invalid_credentials(
        self, page, base_url, test_id, email, password, expected_error
    ):
        """Verify login fails with invalid credentials and shows error message."""
        lp = LoginPage(page, base_url)
        lp.open()

        lp.login(email, password)

        error = lp.get_error_message()
        assert expected_error.lower() in error.lower(), (
            f"[{test_id}] Expected error containing '{expected_error}', got: '{error}'"
        )

    def test_logout_successfully(self, page, base_url, registered_user):
        """Verify a logged-in user can logout and sees confirmation."""
        lp = LoginPage(page, base_url)
        lp.open()

        # Login first
        lp.login(registered_user["email"], registered_user["password"])
        assert lp.is_login_successful(), "Login should succeed before testing logout"

        # Logout
        lp.logout()

        assert lp.is_logout_successful(), (
            "User should see logout confirmation page after logging out"
        )
