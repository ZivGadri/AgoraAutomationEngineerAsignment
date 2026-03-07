from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage, FindBy

class CheckoutCompletePage(BasePage):
    """Page Object for the Checkout Complete (Success) Page."""
    
    @FindBy(By.CLASS_NAME, "complete-header")
    def complete_header(self) -> WebElement: pass
    
    def get_confirmation_message(self) -> str:
        """Retrieves the final success confirmation message text."""
        return self.get_text(self.complete_header)
