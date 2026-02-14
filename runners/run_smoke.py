"""
Run Smoke Tests
Quick critical-path validation to ensure the app is stable.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("=========================================")
    print("  Running: SMOKE TESTS")
    print("=========================================")

    exit_code = subprocess.call([sys.executable, "-m", "pytest", "-v", "-m", "smoke", "--tb=short"])
    sys.exit(exit_code)
