"""
Run Cross-Browser Tests
Executes the smoke suite across Chromium, Firefox, and WebKit with a summary.
"""

import subprocess
import sys

BROWSERS = ["chromium", "firefox", "webkit"]


def run_browser(browser: str) -> int:
    """Run smoke tests on a specific browser and return the exit code."""
    print(f"\n----- {browser.capitalize()} -----")
    return subprocess.call([
        sys.executable, "-m", "pytest", "-v",
        "-m", "smoke",
        "--browser", browser,
        "--tb=short",
    ])


if __name__ == "__main__":
    print("=========================================")
    print("  Running: CROSS-BROWSER TESTS")
    print("=========================================")

    results = {}
    for browser in BROWSERS:
        results[browser] = run_browser(browser)

    print("\n=========================================")
    print("  Cross-Browser Results")
    print("=========================================")
    for browser, code in results.items():
        status = "PASSED" if code == 0 else "FAILED"
        print(f"  {browser.capitalize():10s}: {status}")
    print("=========================================")

    # Exit with failure if any browser failed
    sys.exit(0 if all(code == 0 for code in results.values()) else 1)
