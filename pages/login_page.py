from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage, FindBy
from pages.inventory_page import InventoryPage
from pages.base_page import BasePage, FindBy

class LoginPage(BasePage):
    """Page Object for the SauceDemo Login Page."""
    
    @FindBy(By.ID, "user-name")
    def username_input(self) -> WebElement: pass

    @FindBy(By.ID, "password")
    def password_input(self) -> WebElement: pass

    @FindBy(By.ID, "login-button")
    def login_btn(self) -> WebElement: pass
    
    def fill_username(self, username: str) -> None:
        self.type_text(self.username_input, username)
        
    def fill_password(self, password: str) -> None:
        self.type_text(self.password_input, password)
        
    def click_login(self) -> InventoryPage:
        self.click(self.login_btn)
        return InventoryPage(self.driver)
        
    def login(self, username: str, password: str) -> InventoryPage:
        """Helper method to perform a full login action and return the Inventory Page."""
        self.fill_username(username)
        self.fill_password(password)
        inventory_page = self.click_login()
        
        return inventory_page
