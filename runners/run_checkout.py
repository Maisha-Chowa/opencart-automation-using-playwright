"""
Run Checkout Tests
Validates checkout page template, form validation, coupon & gift certificate.
"""

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

if __name__ == "__main__":
    print("=========================================")
    print("  Running: CHECKOUT TESTS")
    print("=========================================")

    exit_code = subprocess.call([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_checkout.py",
        "--tb=short",
    ])
    sys.exit(exit_code)
