"""
Test Suite: User Registration
Validates the OpenCart user registration flow.
"""

import time

import pytest
from pages.register_page import RegisterPage


@pytest.mark.account
@pytest.mark.regression
class TestUserRegistration:
    """Tests for the user registration feature."""

    @pytest.mark.smoke
    def test_successful_registration(self, page, base_url):
        """Verify a new user can register successfully."""
        rp = RegisterPage(page, base_url)
        rp.open()

        # Generate a unique email using timestamp
        unique_email = f"testuser_{int(time.time())}@example.com"

        rp.register(
            first_name="Test",
            last_name="User",
            email=unique_email,
            password="Test@1234",
            agree_privacy=True,
        )

        assert rp.is_registration_successful(), "Registration should be successful"

    def test_registration_without_privacy_policy(self, page, base_url):
        """Verify registration fails without accepting privacy policy."""
        rp = RegisterPage(page, base_url)
        rp.open()

        rp.register(
            first_name="Test",
            last_name="User",
            email="noprivacy@example.com",
            password="Test@1234",
            agree_privacy=False,
        )

        # Should stay on register page or show error
        assert "register" in rp.get_url().lower() or rp.get_error_message(), (
            "Registration should fail without privacy policy acceptance"
        )

    def test_registration_with_existing_email(self, page, base_url):
        """Verify registration fails with an already registered email."""
        rp = RegisterPage(page, base_url)
        rp.open()

        # First registration
        unique_email = f"duplicate_{int(time.time())}@example.com"
        rp.register(
            first_name="First",
            last_name="User",
            email=unique_email,
            password="Test@1234",
        )

        # Second registration with same email
        rp.open()
        rp.register(
            first_name="Second",
            last_name="User",
            email=unique_email,
            password="Test@1234",
        )

        error = rp.get_error_message()
        assert error, "Should show error for duplicate email registration"

    def test_registration_with_empty_fields(self, page, base_url):
        """Verify registration form shows validation errors for empty fields."""
        rp = RegisterPage(page, base_url)
        rp.open()

        rp.register(
            first_name="",
            last_name="",
            email="",
            password="",
            agree_privacy=True,
        )

        errors = rp.get_field_errors()
        assert len(errors) > 0, "Should show validation errors for empty fields"
