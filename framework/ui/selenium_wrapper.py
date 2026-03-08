"""
pages/selenium_wrapper.py

Abstract base class for all Page Objects.
Encapsulates common Selenium WebDriver browser interactions.
"""
import time
from typing import List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from framework.ui.ui_constants import Timeouts
from framework.utils.helper_functions import Logger

class SeleniumWrapper:
    """
    Base class for all Page Objects in the framework.
    Provides robust wrapper methods around common Selenium interactions,
    always prioritizing explicit waits over implicit or static sleeps.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.wait = WebDriverWait(
            self.driver, 
            Timeouts.DEFAULT_TIMEOUT_IN_SEC
        )
        self.logger.info("Initialized Page Object")

    def navigate(self, url: str) -> None:
        """Navigates the browser to the specified URL."""
        self.driver.get(url)

    def find_element(self, locator: tuple[str, str] | WebElement) -> WebElement:
        """
        Wait for an element to be both present in the DOM and visible.
        Locator should be a tuple like (By.ID, "login-button").
        """
        try:
            if isinstance(locator, tuple):
                self.logger.debug(f"Locating element by {locator[0]}: '{locator[1]}'")
                return self.wait.until(EC.visibility_of_element_located(locator))
            else:
                return locator
        except TimeoutException as e:
            self.logger.error(f"TimeoutException finding element: {locator}")
            raise e
        except WebDriverException as e:
            self.logger.error(f"WebDriverException finding element: {locator}. Error: {e}")
            raise e


    def find_elements(self, locator: tuple[str, str] | WebElement) -> List[WebElement]:
        """
        Wait for at least one element to be present and return all matches.
        """
        if isinstance(locator, tuple):
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        else:
            return locator

    def click(self, locator: tuple[str, str] | WebElement, timeout: float = Timeouts.DEFAULT_SLEEP_IN_SEC) -> None:
        """Wait for an element to be clickable and then click it."""
        try:
            if isinstance(locator, tuple):
                self.logger.info(f"Clicking element by {locator[0]}: '{locator[1]}'")
                element = self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
            else:
                self.logger.info("Clicking WebElement directly.")
                locator.click()
            time.sleep(timeout)
        except Exception as e:
            self.logger.error(f"Failed to click element {locator}. Exception: {e}")
            raise e

    def type_text(self, locator: tuple[str, str] | WebElement, text: str, timeout: float = Timeouts.DEFAULT_SLEEP_IN_SEC) -> None:
        """Wait for an element to be visible, clear its contents, and type text."""
        if isinstance(locator, tuple):
            element = self.find_element(locator)
        else:
            element = locator
        self.logger.info(f"Typing Text: '{text}'")
        element.clear()
        element.send_keys(text)
        time.sleep(timeout)

    def get_text(self, locator: tuple[str, str] | WebElement) -> str:
        """Wait for an element to be visible and return its text content."""
        if isinstance(locator, tuple):
            return self.find_element(locator).text
        else:
            return locator.text