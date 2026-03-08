from typing import List, Callable, Any

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC


def find_by(by: str, value: str) -> Callable[[Callable[..., Any]], property]:
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


def find_all(by: str, value: str) -> Callable[[Callable[..., Any]], property]:
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