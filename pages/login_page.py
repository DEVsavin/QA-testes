from selenium.webdriver.common.by import By

from config import settings
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = settings.saucedemo_base_url
        self._user_field = (By.ID, "user-name")
        self._pass_field = (By.ID, "password")
        self._login_button = (By.ID, "login-button")
        self._inventory_container = (By.ID, "inventory_container")
        self._error_message = (By.CSS_SELECTOR, '[data-test="error"]')

    def acessar(self):
        self.open(self.url)
        self.wait_visible(self._user_field)

    def logar(self, usuario, senha, aguardar_sucesso: bool = False):
        self.type_text(self._user_field, usuario)
        self.type_text(self._pass_field, senha)
        self.click(self._login_button)

        if aguardar_sucesso:
            self.wait_url_contains("inventory.html")
            self.wait_visible(self._inventory_container)

    def mensagem_erro(self) -> str:
        return self.text_of(self._error_message)
