"""
Root conftest.py - Playwright fixtures and configuration for OpenCart automation.
"""

import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost")
ADMIN_URL = os.getenv("ADMIN_URL", "http://localhost/admin")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Override default browser context arguments."""
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
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
