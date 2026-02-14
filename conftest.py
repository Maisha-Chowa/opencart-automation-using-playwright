"""
Root conftest.py - Playwright fixtures, trace-on-failure, and configuration
for OpenCart automation.
"""

import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost")
ADMIN_URL = os.getenv("ADMIN_URL", "http://localhost/admin")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))

# Directories for test artifacts
SCREENSHOTS_DIR = Path("screenshots")
TRACES_DIR = Path("traces")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override default browser context arguments."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": None,
    }


@pytest.fixture(scope="session")
def base_url():
    """Return the base URL for the OpenCart storefront."""
    return BASE_URL


@pytest.fixture(scope="session")
def admin_url():
    """Return the admin panel URL."""
    return ADMIN_URL


@pytest.fixture()
def home_page(page: Page, base_url: str) -> Page:
    """Navigate to the OpenCart home page before each test."""
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    return page


# ============================================================
# Trace on Failure & Screenshot Capture
# ============================================================

@pytest.fixture(autouse=True)
def _capture_trace(page: Page, request):
    """
    Start a Playwright trace before each test.
    On failure: save the trace zip and a screenshot.
    On success: discard the trace.
    """
    # Ensure artifact directories exist
    SCREENSHOTS_DIR.mkdir(exist_ok=True)
    TRACES_DIR.mkdir(exist_ok=True)

    # Start tracing with screenshots and snapshots
    page.context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield

    # Determine test outcome
    # pytest_runtest_makereport stores the result on the request node
    failed = request.node.rep_call.failed if hasattr(request.node, "rep_call") else False

    if failed:
        # Generate a safe filename from the test name
        test_name = request.node.name.replace("/", "_").replace("::", "_")

        # Save screenshot
        screenshot_path = SCREENSHOTS_DIR / f"{test_name}.png"
        try:
            page.screenshot(path=str(screenshot_path), full_page=True)
        except Exception:
            pass  # Page may have closed or navigated away

        # Save trace
        trace_path = TRACES_DIR / f"{test_name}.zip"
        page.context.tracing.stop(path=str(trace_path))
    else:
        # Discard the trace on success
        page.context.tracing.stop()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test result and attach it to the test item node,
    so the _capture_trace fixture can determine pass/fail.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        item.rep_call = report
