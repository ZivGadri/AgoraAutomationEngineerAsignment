from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage, FindBy, FindAll
from pages.checkout_info_page import CheckoutInfoPage
from pages.base_page import BasePage, FindBy

class CartPage(BasePage):
    """Page Object for the SauceDemo Cart Page."""

    @FindAll(By.XPATH, "//div[@class='cart_item']")
    def cart_items(self) -> list[WebElement]: pass
    
    @FindBy(By.ID, "checkout")
    def checkout_btn(self) -> WebElement: pass

    ITEM_NAME_CHILD_XPATH = ".//div[@class='inventory_item_name']"

    ITEM_REMOVE_BTM_CHILD_XPATH = ".//button"
    
    def _get_remove_element(self, product_name: str) -> tuple[str, str] | WebElement:
        for item in self.cart_items:
            item_name = self.get_text(item.find_element(By.XPATH, self.ITEM_NAME_CHILD_XPATH))
            if item_name.lower() == product_name.lower():
                return item.find_element(By.XPATH, self.ITEM_REMOVE_BTM_CHILD_XPATH)
        self.logger.error("Failed to find item name '{}' in cart page".format(product_name))
        return None
        
    def remove_product(self, product_name: str) -> None:
        """Clicks the remove button for the specified product."""
        remove_element = self._get_remove_element(product_name)
        self.click(remove_element)
        
    def click_checkout(self) -> CheckoutInfoPage:
        """Proceeds to the first step of checkout."""
        self.checkout_btn.click()
        return CheckoutInfoPage(self.driver)
