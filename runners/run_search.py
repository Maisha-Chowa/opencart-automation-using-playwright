"""
Run Search Tests
Validates product search functionality.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("=========================================")
    print("  Running: SEARCH TESTS")
    print("=========================================")

    exit_code = subprocess.call([sys.executable, "-m", "pytest", "-v", "tests/test_search.py", "--tb=short"])
    sys.exit(exit_code)
