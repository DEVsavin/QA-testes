from config import settings
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage


def test_fluxo_compra_completo(driver):
    login_page = LoginPage(driver)
    login_page.acessar()
    login_page.logar(
        settings.saucedemo_standard_user,
        settings.saucedemo_password,
        aguardar_sucesso=True,
    )

    cart_page = CartPage(driver)
    cart_page.adicionar_produto_ao_carrinho()
    cart_page.acessar_carrinho()

    assert "cart.html" in driver.current_url, "Falha ao navegar para o carrinho!"
    assert cart_page.produto_no_carrinho_visivel(), "Produto não encontrado no carrinho!"
    assert (
        cart_page.nome_produto_no_carrinho() == "Sauce Labs Backpack"
    ), "Produto esperado não apareceu no carrinho!"

    cart_page.iniciar_checkout()
    assert (
        "checkout-step-one.html" in driver.current_url
    ), "Falha ao navegar para o formulário de checkout!"

    checkout_page = CheckoutPage(driver)
    checkout_page.preencher_dados("GSD", "Automation", "12345")
    checkout_page.continuar()

    assert (
        "checkout-step-two.html" in driver.current_url
    ), "Falha ao navegar para a revisão do checkout!"
    assert "Item total:" in checkout_page.subtotal(), "Subtotal não foi exibido!"
    assert "Tax:" in checkout_page.imposto(), "Imposto não foi exibido!"
    assert "Total:" in checkout_page.total(), "Total não foi exibido!"

    checkout_page.finalizar()

    assert (
        "checkout-complete.html" in driver.current_url
    ), "Falha ao finalizar a compra!"
    assert (
        checkout_page.cabecalho_confirmacao() == "Thank you for your order!"
    ), "Mensagem final de sucesso não confere!"
    assert (
        "Your order has been dispatched" in checkout_page.texto_confirmacao()
    ), "Texto de confirmação da compra não foi exibido!"
