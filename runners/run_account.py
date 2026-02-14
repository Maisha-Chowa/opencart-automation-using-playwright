"""
Run Account Tests (Registration + Login)
Validates user registration and authentication flows.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("=========================================")
    print("  Running: ACCOUNT TESTS (Register + Login)")
    print("=========================================")

    exit_code = subprocess.call([
        sys.executable, "-m", "pytest", "-v",
        "tests/test_register.py", "tests/test_login.py",
        "--tb=short",
    ])
    sys.exit(exit_code)
