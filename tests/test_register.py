"""
Test Suite: User Registration (Data-Driven)
Validates the OpenCart user registration flow using parametrized test data.
"""

import pytest
from pages.register_page import RegisterPage
from utilities.test_data import generate_unique_email, REGISTRATION_VALIDATION_DATA


@pytest.mark.account
@pytest.mark.regression
class TestUserRegistration:
    """Tests for the user registration feature."""

    @pytest.mark.smoke
    def test_successful_registration(self, page, base_url):
        """Verify a new user can register successfully with valid data."""
        rp = RegisterPage(page, base_url)
        rp.open()

        rp.register(
            first_name="Test",
            last_name="User",
            email=generate_unique_email("success"),
            password="Test@1234",
            agree_privacy=True,
        )

        assert rp.is_registration_successful(), "Registration should be successful"

    @pytest.mark.parametrize(
        "test_id, first_name, last_name, email, password, agree_privacy, expected_error",
        REGISTRATION_VALIDATION_DATA,
        ids=[data[0] for data in REGISTRATION_VALIDATION_DATA],
    )
    def test_registration_validation(
        self,
        page,
        base_url,
        test_id,
        first_name,
        last_name,
        email,
        password,
        agree_privacy,
        expected_error,
    ):
        """Verify registration form shows correct validation errors for invalid data."""
        rp = RegisterPage(page, base_url)
        rp.open()

        rp.register(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            agree_privacy=agree_privacy,
        )

        # Check for field-level errors or page-level alert
        field_errors = rp.get_field_errors()
        page_error = rp.get_error_message()
        all_errors = " ".join(field_errors) + " " + page_error

        assert expected_error.lower() in all_errors.lower() or len(field_errors) > 0, (
            f"[{test_id}] Expected error containing '{expected_error}', "
            f"got field errors: {field_errors}, page error: '{page_error}'"
        )

    def test_registration_with_existing_email(self, page, base_url):
        """Verify registration fails with an already registered email."""
        rp = RegisterPage(page, base_url)
        rp.open()

        # First registration
        unique_email = generate_unique_email("duplicate")
        rp.register(
            first_name="First",
            last_name="User",
            email=unique_email,
            password="Test@1234",
        )

        # Second registration with the same email
        rp.open()
        rp.register(
            first_name="Second",
            last_name="User",
            email=unique_email,
            password="Test@1234",
        )

        error = rp.get_error_message()
        assert error, "Should show error for duplicate email registration"
