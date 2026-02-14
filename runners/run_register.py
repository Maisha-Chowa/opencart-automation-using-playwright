"""
Run Register Tests
Validates user registration: visibility, positive, negative, blank, and data-driven tests.
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
    print("  Running: REGISTER TESTS")
    print("=========================================")

    exit_code = subprocess.call([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_register.py",
        "--tb=short",
    ])
    sys.exit(exit_code)
