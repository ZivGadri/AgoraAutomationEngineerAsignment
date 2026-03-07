"""
pages/base_page.py

Abstract base class for all Page Objects.
Encapsulates common Selenium WebDriver browser interactions.
"""
import time
from typing import List, Callable, Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.constants import Timeouts, TestConstants
from utils.config import Logger

def FindBy(by: str, value: str) -> Callable[[Callable[..., Any]], property]:
    """
    Decorate a dummy method to turn it into a property returning a single resolved WebElement.
    """
    def decorator(func: Callable[..., Any]) -> property:
        @property
        def wrapper(self: Any) -> WebElement:
            locator = (by, value)
            return self.wait.until(EC.visibility_of_element_located(locator))
        return wrapper
    return decorator


def FindAll(by: str, value: str) -> Callable[[Callable[..., Any]], property]:
    """
    Decorate a dummy method to turn it into a property returning a list of resolved WebElements.
    """
    def decorator(func: Callable[..., Any]) -> property:
        @property
        def wrapper(self: Any) -> List[WebElement]:
            locator = (by, value)
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        return wrapper
    return decorator



class BasePage:
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
        if isinstance(locator, tuple):
            return self.wait.until(EC.visibility_of_element_located(locator))
        else:
            return locator


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
        if isinstance(locator, tuple):
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        else:
            locator.click()
        time.sleep(timeout)

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