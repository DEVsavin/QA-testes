from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    def __init__(self, driver):
        self.driver = driver
        # Mapeamento dos elementos
        self._add_to_cart_button = (By.ID, "add-to-cart-sauce-labs-backpack")
        self._cart_icon = (By.CLASS_NAME, "shopping_cart_link")

    def adicionar_produto_ao_carrinho(self):
        wait = WebDriverWait(self.driver, 10)
        # Espera o botão estar visível antes de clicar
        botao = wait.until(EC.element_to_be_clickable(self._add_to_cart_button))
        botao.click()

    def acessar_carrinho(self):
        self.driver.find_element(*self._cart_icon).click()