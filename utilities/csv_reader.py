"""
CSV Reader utility for loading test data from CSV files.
"""

import csv
from pathlib import Path

TESTDATA_DIR = Path(__file__).resolve().parent.parent / "testdata"


def read_csv(filename: str) -> list[dict[str, str]]:
    """Read a CSV file from the testdata directory and return a list of dicts.

    Each dict represents one row with column headers as keys.
    """
    filepath = TESTDATA_DIR / filename
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
