"""
pages/base_page.py

Abstract base class for all Page Objects.
Encapsulates common Selenium WebDriver browser interactions.
"""

from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.constants import Timeouts


class BasePage:
    """
    Base class for all Page Objects in the framework.
    Provides robust wrapper methods around common Selenium interactions,
    always prioritizing explicit waits over implicit or static sleeps.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Standard explicit wait object to be reused by interactions
        self.wait = WebDriverWait(
            self.driver, 
            Timeouts.DEFAULT_TIMEOUT_IN_SEC
        )

    def navigate(self, url: str) -> None:
        """Navigates the browser to the specified URL."""
        self.driver.get(url)

    def find_element(self, locator: tuple[str, str]) -> WebElement:
        """
        Wait for an element to be both present in the DOM and visible.
        Locator should be a tuple like (By.ID, "login-button").
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements(self, locator: tuple[str, str]) -> List[WebElement]:
        """
        Wait for at least one element to be present and return all matches.
        """
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator: tuple[str, str]) -> None:
        """Wait for an element to be clickable and then click it."""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def type_text(self, locator: tuple[str, str], text: str) -> None:
        """Wait for an element to be visible, clear its contents, and type text."""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[str, str]) -> str:
        """Wait for an element to be visible and return its text content."""
        return self.find_element(locator).text

