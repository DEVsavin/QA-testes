from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self._add_to_cart_button = (By.ID, "add-to-cart-sauce-labs-backpack")
        self._cart_icon = (By.CLASS_NAME, "shopping_cart_link")
        self._inventory_item_name = (By.CLASS_NAME, "inventory_item_name")
        self._checkout_button = (By.ID, "checkout")

    def adicionar_produto_ao_carrinho(self):
        self.click(self._add_to_cart_button)

    def acessar_carrinho(self):
        self.click(self._cart_icon)
        self.wait_url_contains("cart.html")

    def iniciar_checkout(self):
        btn = self.wait_clickable(self._checkout_button)
        for _ in range(3):
            try:
                btn.click()
               
                self.wait_url_contains("checkout-step-one.html")
                return 
            except Exception:
        
                self.driver.execute_script("arguments[0].click();", btn)
                time.sleep(1) 
        
    
        self.wait_url_contains("checkout-step-one.html")

    def nome_produto_no_carrinho(self) -> str:
        return self.text_of(self._inventory_item_name)

    def produto_no_carrinho_visivel(self) -> bool:
        return self.wait_visible(self._inventory_item_name).is_displayed()