from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self._add_to_cart_button = (
            By.CSS_SELECTOR,
            '[data-test="add-to-cart-sauce-labs-backpack"]',
        )
        self._cart_icon = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
        self._inventory_item_name = (By.CLASS_NAME, "inventory_item_name")
        self._checkout_button = (By.ID, "checkout")

    def adicionar_produto_ao_carrinho(self):
        self.click(self._add_to_cart_button)

    def acessar_carrinho(self):
        cart_icon = self.wait_clickable(self._cart_icon)
        self.driver.execute_script("arguments[0].click();", cart_icon)
        self.wait_url_contains("cart.html")

    def iniciar_checkout(self):
        checkout_button = self.wait_clickable(self._checkout_button)
        
        try:
            checkout_button.click()
        except Exception:
            # Fallback para clique via JavaScript se o físico falhar no CI
            self.driver.execute_script("arguments[0].click();", checkout_button)
            
        self.wait_url_contains("checkout-step-one.html")

    def nome_produto_no_carrinho(self) -> str:
        return self.text_of(self._inventory_item_name)

    def produto_no_carrinho_visivel(self) -> bool:
        return self.wait_visible(self._inventory_item_name).is_displayed()