from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage, FindBy
from pages.checkout_complete_page import CheckoutCompletePage
from pages.base_page import BasePage, FindBy

class CheckoutOverviewPage(BasePage):
    """Page Object for the Checkout Overview step (Step 2)."""
    
    @FindBy(By.CLASS_NAME, "summary_subtotal_label")
    def item_total_label(self) -> WebElement: pass
    
    @FindBy(By.CLASS_NAME, "summary_tax_label")
    def tax_label(self) -> WebElement: pass
    
    @FindBy(By.CLASS_NAME, "summary_total_label")
    def total_label(self) -> WebElement: pass
    
    @FindBy(By.ID, "finish")
    def finish_btn(self) -> WebElement: pass
    
    def get_item_total(self) -> float:
        """Retrieves and parses the item total subtotal."""
        text = self.item_total_label.text
        return float(text.split("$")[-1].strip())
        
    def get_tax(self) -> float:
        """Retrieves and parses the tax amount."""
        text = self.tax_label.text
        return float(text.split("$")[-1].strip())
        
    def get_total(self) -> float:
        """Retrieves and parses the final total amount."""
        text = self.total_label.text
        return float(text.split("$")[-1].strip())
        
    def click_finish(self) -> CheckoutCompletePage:
        """Clicks the finish button to complete the flow."""
        self.click(self.finish_btn)
        return CheckoutCompletePage(self.driver)
