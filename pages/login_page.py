from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "https://www.saucedemo.com/"
        # Mapeamento dos elementos (Elementos são privados/protegidos)
        self._user_field = (By.ID, "user-name")
        self._pass_field = (By.ID, "password")
        self._login_button = (By.ID, "login-button")

    def acessar(self):
        self.driver.get(self.url)

    def logar(self, usuario, senha):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located(self._user_field)).send_keys(usuario)
        self.driver.find_element(*self._pass_field).send_keys(senha)
        self.driver.find_element(*self._login_button).click()