from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.timeout = timeout

    def open(self, url: str):
        self.driver.get(url)

    def wait_visible(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_present(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.presence_of_element_located(locator)
        )

    def wait_clickable(self, locator):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_url_contains(self, texto_url: str):
        return WebDriverWait(self.driver, self.timeout).until(
            EC.url_contains(texto_url)
        )

    def click(self, locator):
        element = self.wait_clickable(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            element,
        )
        element.click()

    def type_text(self, locator, text: str):
        field = self.wait_visible(locator)
        field.clear()
        field.send_keys(text)

    def text_of(self, locator) -> str:
        return self.wait_visible(locator).text
