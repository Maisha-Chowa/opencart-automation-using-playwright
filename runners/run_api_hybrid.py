"""
Run API + UI Network Monitoring Tests
Executes all tests in the tests/api/ folder that monitor backend
API calls triggered by UI interactions.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("=========================================")
    print("  Running: API + UI NETWORK MONITORING TESTS")
    print("=========================================")

    exit_code = subprocess.call([
        sys.executable, "-m", "pytest", "-v",
        "tests/api/",
        "--tb=short",
    ])
    sys.exit(exit_code)
