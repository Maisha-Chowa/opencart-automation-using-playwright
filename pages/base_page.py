"""BasePage - Common page actions and utilities shared across all page objects."""

from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects with common helper methods."""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to a URL and wait for network idle."""
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def get_title(self) -> str:
        """Return the page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current URL."""
        return self.page.url

    def click(self, selector: str):
        """Click on an element."""
        self.page.click(selector)

    def fill(self, selector: str, text: str):
        """Clear and fill text into an input field."""
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        """Get the text content of an element."""
        return self.page.text_content(selector) or ""

    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        return self.page.is_visible(selector)

    def wait_for_element(self, selector: str, timeout: int = 10000):
        """Wait for an element to be visible."""
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def take_screenshot(self, name: str):
        """Take a screenshot and save it to the screenshots directory."""
        self.page.screenshot(path=f"screenshots/{name}.png", full_page=True)

    def expect_element_visible(self, selector: str):
        """Assert that an element is visible using Playwright's expect."""
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text_present(self, selector: str, text: str):
        """Assert that an element contains specific text."""
        expect(self.page.locator(selector)).to_contain_text(text)
