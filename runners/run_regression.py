"""
Run Regression Tests
Full regression suite covering all feature areas.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("=========================================")
    print("  Running: REGRESSION TESTS")
    print("=========================================")

    exit_code = subprocess.call([sys.executable, "-m", "pytest", "-v", "-m", "regression", "--tb=short"])
    sys.exit(exit_code)
