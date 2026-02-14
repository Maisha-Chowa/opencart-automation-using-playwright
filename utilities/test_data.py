"""
Test data constants, parametrize data sets, and generators for OpenCart automation tests.
"""

import time


# ============================================================
# Admin Credentials (matches docker-compose.yml defaults)
# ============================================================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# ============================================================
# Valid Test User
# ============================================================
VALID_USER = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "Test@1234",
}

# ============================================================
# Sample Products (default OpenCart demo data)
# ============================================================
SAMPLE_PRODUCTS = [
    "MacBook",
    "iPhone",
    "Apple Cinema 30\"",
    "Canon EOS 5D",
    "Samsung SyncMaster 941BW",
    "iPod Classic",
    "HP LP3065",
]

# ============================================================
# Invalid Test Data
# ============================================================
INVALID_EMAIL = "invalid-email"
SHORT_PASSWORD = "123"
EMPTY_STRING = ""

# ============================================================
# Registration Validation Data (Data-Driven)
# Format: (test_id, first_name, last_name, email, password, agree_privacy, expected_error)
# ============================================================
REGISTRATION_VALIDATION_DATA = [
    (
        "missing_firstname",
        "",                         # first_name empty
        "User",
        "nofirst@example.com",
        "Test@1234",
        True,
        "First Name",
    ),
    (
        "missing_lastname",
        "Test",
        "",                         # last_name empty
        "nolast@example.com",
        "Test@1234",
        True,
        "Last Name",
    ),
    (
        "invalid_email",
        "Test",
        "User",
        "invalid-email",            # malformed email
        "Test@1234",
        True,
        "E-Mail",
    ),
    (
        "short_password",
        "Test",
        "User",
        "shortpw@example.com",
        "123",                      # too short
        True,
        "Password",
    ),
    (
        "no_privacy_policy",
        "Test",
        "User",
        "noprivacy@example.com",
        "Test@1234",
        False,                      # privacy not accepted
        "Warning",
    ),
]

# ============================================================
# Login Test Data
# ============================================================
INVALID_LOGIN_DATA = [
    (
        "invalid_password",
        "john.doe@example.com",
        "WrongPassword!",
        "Warning",
    ),
    (
        "unregistered_email",
        "nonexistent_user_999@example.com",
        "Test@1234",
        "Warning",
    ),
    (
        "empty_email_and_password",
        "",
        "",
        "Warning",
    ),
]

# ============================================================
# API Configuration
# ============================================================
API_ROUTES = {
    "cart_add": "/index.php?route=api/cart.add",
    "cart_products": "/index.php?route=api/cart.products",
    "currency": "/index.php?route=api/currency",
    "login": "/index.php?route=api/account.login",
    "session": "/index.php?route=api/session",
}

# ============================================================
# Checkout Test Data
# ============================================================
GUEST_CHECKOUT_DATA = {
    "first_name": "Guest",
    "last_name": "Buyer",
    "email": "guest.buyer@example.com",
    "company": "",
    "address_1": "123 Test Street",
    "address_2": "",
    "city": "Test City",
    "postcode": "12345",
    "country": "United States",
    "zone": "California",
}


def generate_unique_email(prefix: str = "testuser") -> str:
    """Generate a unique email address using a timestamp."""
    return f"{prefix}_{int(time.time())}@example.com"
