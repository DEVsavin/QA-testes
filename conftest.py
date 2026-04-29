import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    # 1. Configurações para localizar o Chrome
    chrome_options = Options()
    
    # Se o erro de "binary not found" persistir, descomente a linha abaixo 
    # e coloque o caminho do seu chrome.exe:
    # chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    # 2. Configuração do WebDriver (Download automático do driver correto) [cite: 37]
    service = Service(ChromeDriverManager().install())
    
    # 3. Inicializa o navegador com as opções [cite: 38]
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.implicitly_wait(10) # Aguarda até 10 segundos pelos elementos [cite: 43]
    driver.maximize_window()
    
    yield driver
    
    # 4. Fecha o navegador após a execução [cite: 51]
    driver.quit()