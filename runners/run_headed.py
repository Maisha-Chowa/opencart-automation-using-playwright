"""
Run All Tests in Headed Mode (Visible Browser)
Useful for debugging and demos.

Usage:
    python runners/run_headed.py            # default, no slow motion
    python runners/run_headed.py 500        # 500ms slow motion
"""

import subprocess
import sys

if __name__ == "__main__":
    slowmo = sys.argv[1] if len(sys.argv) > 1 else "0"

    print("=========================================")
    print("  Running: ALL TESTS (Headed Mode)")
    print(f"  Slow Motion: {slowmo}ms")
    print("=========================================")

    exit_code = subprocess.call([
        sys.executable, "-m", "pytest", "-v",
        "--headed", "--slowmo", slowmo,
        "--tb=short",
    ])
    sys.exit(exit_code)
