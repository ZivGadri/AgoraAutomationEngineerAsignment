from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:
    """Factory class to create and configure Selenium WebDriver instances."""

    @staticmethod
    def get_chrome_driver() -> webdriver.Chrome:
        """
        Instantiates and configures a Chrome WebDriver.
        Uses WebDriver Manager to handle the binary automatically.
        """
        service = ChromeService(ChromeDriverManager().install())

        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1280,800")
        options.add_argument("--incognito") # Avoiding Chrome alert from Google Password Manager
        
        driver_instance = webdriver.Chrome(service=service, options=options)
        
        # Implicit wait as a fallback, though explicit waits in SeleniumWrapper are preferred.
        driver_instance.implicitly_wait(5)
        
        return driver_instance
