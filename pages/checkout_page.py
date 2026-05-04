from selenium.common.exceptions import TimeoutException
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
        self._error_message = (By.CSS_SELECTOR, '[data-test="error"]')

    def preencher_dados(self, nome: str, sobrenome: str, cep: str):
        self.type_text(self._first_name, nome)
        self.type_text(self._last_name, sobrenome)
        self.type_text(self._postal_code, cep)

    def continuar(self):
        self.click(self._continue_button)
        try:
            self.wait_url_contains("checkout-step-two.html")
        except TimeoutException as exc:
            raise TimeoutException(
                f"Não avançou para a revisão do checkout após clicar em Continue. "
                f"url_atual={self.driver.current_url!r}, "
                f"erro_formulario={self._mensagem_erro_checkout()!r}"
            ) from exc

    def finalizar(self):
        self.click(self._finish_button)
        self.wait_url_contains("checkout-complete.html")

    def _mensagem_erro_checkout(self) -> str:
        elementos = self.driver.find_elements(*self._error_message)
        mensagens = [elemento.text.strip() for elemento in elementos if elemento.text.strip()]
        return " | ".join(mensagens)

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
