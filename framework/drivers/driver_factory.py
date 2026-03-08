from framework.utils.helper_functions import Logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:
    """Factory class to create and configure Selenium WebDriver instances."""
    
    logger = Logger.get_logger("DriverFactory")

    @staticmethod
    def get_chrome_driver() -> webdriver.Chrome:
        """
        Instantiates and configures a Chrome WebDriver.
        Uses WebDriver Manager to handle the binary automatically.
        Wraps initialization in a try-except to catch driver binary or permission errors.
        """
        try:
            service = ChromeService(ChromeDriverManager().install())
    
            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=1280,800")
            options.add_argument("--incognito") # Avoiding Chrome alert from Google Password Manager
            
            driver_instance = webdriver.Chrome(service=service, options=options)
            
            # Implicit wait as a fallback, though explicit waits in SeleniumWrapper are preferred.
            driver_instance.implicitly_wait(5)
            
            DriverFactory.logger.info("Chrome WebDriver instantiated successfully.")
            return driver_instance
        except Exception as e:
            DriverFactory.logger.error(f"Failed to instantiate Chrome WebDriver: {e}")
            raise
