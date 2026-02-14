"""
Run Cart Tests
Validates shopping cart add, remove, and update flows.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("=========================================")
    print("  Running: CART TESTS")
    print("=========================================")

    exit_code = subprocess.call([sys.executable, "-m", "pytest", "-v", "tests/test_cart.py", "--tb=short"])
    sys.exit(exit_code)
