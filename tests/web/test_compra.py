import os
import pytest
from dotenv import load_dotenv
from pages.login_page import LoginPage
from pages.cart_page import CartPage
from selenium.webdriver.common.by import By

load_dotenv()

def test_fluxo_compra_completo(driver):
    login_page = LoginPage(driver)
    login_page.acessar()
    login_page.logar(os.getenv("LOGIN_USER"), os.getenv("LOGIN_PASSWORD"))
    
    cart_page = CartPage(driver)
    cart_page.adicionar_produto_ao_carrinho()
    cart_page.acessar_carrinho()
    
    assert "cart.html" in driver.current_url, "Falha ao navegar para o carrinho!"
    
    item_no_carrinho = driver.find_element(By.CLASS_NAME, "inventory_item_name")
    assert item_no_carrinho.is_displayed(), "Produto não encontrado no carrinho!"
