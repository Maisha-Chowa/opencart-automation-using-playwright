"""
Run All Tests
Executes the complete test suite across all modules.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("=========================================")
    print("  Running: ALL TESTS")
    print("=========================================")

    exit_code = subprocess.call([sys.executable, "-m", "pytest", "-v", "--tb=short"])
    sys.exit(exit_code)
