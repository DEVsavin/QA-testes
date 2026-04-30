from config import settings
from pages.login_page import LoginPage


def test_login_com_campos_obrigatorios_vazios_exibe_erro(driver):
    login_page = LoginPage(driver)
    login_page.acessar()
    login_page.logar("", "")

    assert (
        login_page.mensagem_erro() == "Epic sadface: Username is required"
    ), "Mensagem de erro para login vazio não confere!"


def test_login_com_credenciais_invalidas_exibe_erro(driver):
    login_page = LoginPage(driver)
    login_page.acessar()
    login_page.logar("usuario_invalido", "senha_invalida")

    assert (
        login_page.mensagem_erro()
        == "Epic sadface: Username and password do not match any user in this service"
    ), "Mensagem de erro para credenciais inválidas não confere!"


def test_login_com_usuario_bloqueado_exibe_erro(driver):
    login_page = LoginPage(driver)
    login_page.acessar()
    login_page.logar(settings.saucedemo_locked_user, settings.saucedemo_password)

    assert (
        login_page.mensagem_erro()
        == "Epic sadface: Sorry, this user has been locked out."
    ), "Mensagem de erro para usuário bloqueado não confere!"
