from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage, FindBy, FindAll
from pages.cart_page import CartPage
from pages.base_page import BasePage, FindBy
from utils.config import Logger


class InventoryPage(BasePage):
    """Page Object for the SauceDemo Inventory Page."""

    
    @FindBy(By.ID, "shopping_cart_container")
    def cart_icon(self) -> WebElement: pass

    @FindAll(By.XPATH, "//div[@class='inventory_item']")
    def items_list(self) -> list[WebElement]: pass

    PRODUCT_NAME_CHILD_XPATH = ".//div[@class='inventory_item_label']//div"
    ADD_TO_CART_BTN_CHILD_XPATH = ".//div[@class='pricebar']/button"
    ITEM_PRICE_CHILD_XPATH = ".//div[@class='inventory_item_price']"
    
    # Dynamic locator generator for products
    def _add_product_to_cart(self, item: WebElement) -> None:
        """Returns the Add to Cart button element for a given product element."""
        try:
            add_to_cart_btn = item.find_element(By.XPATH, self.ADD_TO_CART_BTN_CHILD_XPATH)
            self.click(add_to_cart_btn)
        except NoSuchElementException:
            self.logger.error("Failed to find Add to Cart button")
            raise NoSuchElementException("Failed to find Add to Cart button")

    def _get_product_price(self, item: WebElement) -> str:
        """Returns the price locator for a given product."""
        try:
            item_price_elem = item.find_element(By.XPATH, self.ITEM_PRICE_CHILD_XPATH)
        except NoSuchElementException:
            self.logger.error("Failed to find Add to Cart button")
            raise NoSuchElementException("Failed to find Add to Cart button")

        item_price = self.get_text(item_price_elem)
        return float(item_price.replace("$", "").strip())
        
    def go_to_cart(self) -> CartPage:
        """Clicks on the cart icon to navigate to the Cart page."""
        self.click(self.cart_icon)
        return CartPage(self.driver)

    def add_products_to_cart(self, products: list[str]) -> dict[str, float]:
        products_added = dict.fromkeys([p.lower() for p in products], 0.0)

        for item in self.items_list:
            # Check if item is in the requested list
            item_name = self.get_text(item.find_element(By.XPATH, self.PRODUCT_NAME_CHILD_XPATH)).lower()
            if item_name in products_added.keys():
                # If it is on the list, click "Add to cart" and add its price to the dict
                self._add_product_to_cart(item)
                item_price = self._get_product_price(item)
                products_added[item_name] = item_price

        self.logger.info("Added {} products to cart.".format(len(products_added)))
        self.logger.info("The total value of the products added is {}.".format(sum(products_added.values())))
        return products_added
