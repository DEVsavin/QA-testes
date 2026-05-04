from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self._add_to_cart_button = (
            By.CSS_SELECTOR,
            '[data-test="add-to-cart-sauce-labs-backpack"]',
        )
        self._cart_badge = (By.CSS_SELECTOR, '[data-test="shopping-cart-badge"]')
        self._cart_icon = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
        self._inventory_item_name = (
            By.CSS_SELECTOR,
            '[data-test="inventory-item-name"]',
        )
        self._checkout_button = (By.CSS_SELECTOR, '[data-test="checkout"]')

    def adicionar_produto_ao_carrinho(self):
        self.click(self._add_to_cart_button)
        self.wait_visible(self._cart_badge)

    def acessar_carrinho(self):
        self.click(self._cart_icon)
        self.wait_url_contains("cart.html")

    def iniciar_checkout(self):
        self.click(self._checkout_button)
        self.wait_url_contains("checkout-step-one.html")

    def nome_produto_no_carrinho(self) -> str:
        return self.text_of(self._inventory_item_name)

    def produto_no_carrinho_visivel(self) -> bool:
        return self.wait_visible(self._inventory_item_name).is_displayed()
