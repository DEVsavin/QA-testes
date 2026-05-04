from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class BasePage:
    def __init__(self, driver, timeout: int = 20):
        self.driver = driver
        self.timeout = timeout

    def open(self, url: str):
        self.driver.get(url)

    def _wait_until(self, condition, description: str):
        try:
            return WebDriverWait(self.driver, self.timeout).until(condition)
        except TimeoutException as exc:
            current_url = self.driver.current_url
            title = self.driver.title
            ready_state = self.driver.execute_script("return document.readyState")
            raise TimeoutException(
                f"Timeout após {self.timeout}s aguardando {description}. "
                f"url={current_url!r}, title={title!r}, readyState={ready_state!r}"
            ) from exc

    def wait_visible(self, locator):
        return self._wait_until(
            EC.visibility_of_element_located(locator),
            f"elemento visível {locator}",
        )

    def wait_clickable(self, locator):
        return self._wait_until(
            EC.element_to_be_clickable(locator),
            f"elemento clicável {locator}",
        )

    def wait_url_contains(self, texto_url: str):
        return self._wait_until(
            EC.url_contains(texto_url),
            f"URL conter {texto_url!r}",
        )

    def click(self, locator):
        element = self.wait_clickable(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});",
            element,
        )
        self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text: str):
        field = self.wait_visible(locator)
        field.clear()
        field.send_keys(text)

    def text_of(self, locator) -> str:
        return self.wait_visible(locator).text