"""
Run Cart Tests
Validates shopping cart add-to-cart, view cart, update quantity, and remove flows.
"""

import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

if __name__ == "__main__":
    print("=========================================")
    print("  Running: CART TESTS")
    print("=========================================")

    exit_code = subprocess.call([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_cart.py",
        "--tb=short",
    ])
    sys.exit(exit_code)
