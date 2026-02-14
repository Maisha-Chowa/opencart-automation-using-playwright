"""
Run Checkout Tests
Validates end-to-end checkout flows including guest checkout.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("=========================================")
    print("  Running: CHECKOUT TESTS")
    print("=========================================")

    exit_code = subprocess.call([sys.executable, "-m", "pytest", "-v", "tests/test_checkout.py", "--tb=short"])
    sys.exit(exit_code)
