from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage, FindBy
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.base_page import BasePage, FindBy

class CheckoutInfoPage(BasePage):
    """Page Object for the Checkout Information step (Step 1)."""
    
    @FindBy(By.ID, "first-name")
    def first_name_input(self) -> WebElement: pass
    
    @FindBy(By.ID, "last-name")
    def last_name_input(self) -> WebElement: pass
    
    @FindBy(By.ID, "postal-code")
    def postal_code_input(self) -> WebElement: pass
    
    @FindBy(By.ID, "continue")
    def continue_btn(self) -> WebElement: pass
    
    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fills in the required checkout information fields."""
        self.logger.info(f"Filling checkout information")
        self.type_text(self.first_name_input, first_name)
        self.type_text(self.last_name_input, last_name)
        self.type_text(self.postal_code_input, postal_code)
        
    def click_continue(self) -> CheckoutOverviewPage:
        """Proceeds to the checkout overview page."""
        self.click(self.continue_btn)
        return CheckoutOverviewPage(self.driver)
