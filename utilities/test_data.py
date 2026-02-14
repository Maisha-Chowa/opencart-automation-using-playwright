"""
Test data constants and generators for OpenCart automation tests.
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


def generate_unique_email(prefix: str = "testuser") -> str:
    """Generate a unique email address using a timestamp."""
    return f"{prefix}_{int(time.time())}@example.com"
