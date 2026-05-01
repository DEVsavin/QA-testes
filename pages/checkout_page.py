from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self._first_name = (By.ID, "first-name")
        self._last_name = (By.ID, "last-name")
        self._postal_code = (By.ID, "postal-code")
        self._continue_button = (By.ID, "continue")
        self._finish_button = (By.ID, "finish")
        self._subtotal = (By.CLASS_NAME, "summary_subtotal_label")
        self._tax = (By.CLASS_NAME, "summary_tax_label")
        self._total = (By.CLASS_NAME, "summary_total_label")
        self._complete_header = (By.CLASS_NAME, "complete-header")
        self._complete_text = (By.CLASS_NAME, "complete-text")

    def preencher_dados(self, nome: str, sobrenome: str, cep: str):
        self.type_text(self._first_name, nome)
        self.type_text(self._last_name, sobrenome)
        self.type_text(self._postal_code, cep)

    def continuar(self):
        self.click(self._continue_button)
        self.wait_url_contains("checkout-step-two.html")

    def finalizar(self):
        self.click(self._finish_button)
        self.wait_url_contains("checkout-complete.html")

    def subtotal(self) -> str:
        return self.text_of(self._subtotal)

    def imposto(self) -> str:
        return self.text_of(self._tax)

    def total(self) -> str:
        return self.text_of(self._total)

    def cabecalho_confirmacao(self) -> str:
        return self.text_of(self._complete_header)

    def texto_confirmacao(self) -> str:
        return self.text_of(self._complete_text)
