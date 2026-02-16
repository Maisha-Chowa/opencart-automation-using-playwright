"""
Run Product Tests
Validates product page: visibility, data-driven product info, and API response validation.
"""

import os
import subprocess
import sys
from pathlib import Path

# Always run from the project root, regardless of where the script is invoked
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

if __name__ == "__main__":
    print("=========================================")
    print("  Running: PRODUCT TESTS")
    print("=========================================")

    exit_code = subprocess.call([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_product.py",
        "--tb=short",
    ])
    sys.exit(exit_code)
