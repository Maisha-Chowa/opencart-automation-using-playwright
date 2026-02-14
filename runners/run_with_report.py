"""
Run All Tests with HTML Report
Generates a self-contained HTML report in the reports/ folder.
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

if __name__ == "__main__":
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = reports_dir / f"report_{timestamp}.html"

    print("=========================================")
    print("  Running: ALL TESTS (with HTML Report)")
    print(f"  Report: {report_file}")
    print("=========================================")

    exit_code = subprocess.call([
        sys.executable, "-m", "pytest", "-v",
        "--tb=short",
        f"--html={report_file}",
        "--self-contained-html",
    ])

    print(f"\nReport saved to: {report_file}")
    sys.exit(exit_code)
