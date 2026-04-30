from tests.api.helpers import build_order_payload, unique_id


def test_cria_consulta_e_remove_pedido(api_client):
    payload = build_order_payload(quantity=2, status="placed", complete=True)
    order_id = payload["id"]

    create_response = api_client.post("/store/order", json=payload)
    api_client.assert_status(create_response, 200, "/store/order")
    created_order = api_client.json(create_response)

    assert created_order["id"] == order_id, "ID do pedido criado não confere"
    assert created_order["petId"] == payload["petId"], "Pet ID do pedido criado não confere"
    assert created_order["quantity"] == payload["quantity"], "Quantidade criada não confere"
    assert created_order["status"] == payload["status"], "Status criado não confere"
    assert created_order["complete"] is True, "Pedido deveria estar completo"

    try:
        get_response = api_client.get(f"/store/order/{order_id}")
        api_client.assert_status(get_response, 200, f"/store/order/{order_id}")
        fetched_order = api_client.json(get_response)

        assert fetched_order["id"] == order_id, "ID do pedido consultado não confere"
        assert fetched_order["petId"] == payload["petId"], "Pet ID consultado não confere"
        assert fetched_order["quantity"] == payload["quantity"], "Quantidade consultada não confere"
        assert fetched_order["status"] == payload["status"], "Status consultado não confere"
        assert fetched_order["complete"] is True, "Pedido consultado deveria estar completo"
    finally:
        delete_response = api_client.delete(f"/store/order/{order_id}")
        api_client.assert_status(delete_response, 200, f"/store/order/{order_id}")


def test_consulta_pedido_inexistente_retorna_404(api_client):
    missing_order_id = unique_id()

    response = api_client.get(f"/store/order/{missing_order_id}")

    api_client.assert_status(response, 404, f"/store/order/{missing_order_id}")
    body = api_client.json(response)
    assert body["type"] == "error", "Tipo do erro deveria indicar falha"
    assert "Order not found" in body["message"], "Mensagem deveria indicar pedido inexistente"


def test_consulta_inventario_da_loja(api_client):
    response = api_client.get("/store/inventory")

    api_client.assert_status(response, 200, "/store/inventory")
    inventory = api_client.json(response)

    assert isinstance(inventory, dict), "Inventário deveria retornar um objeto JSON"
    assert inventory, "Inventário não deveria estar vazio na base pública"
    assert any(
        status in inventory for status in ("available", "pending", "sold")
    ), "Inventário deveria conter ao menos um status conhecido"
    assert all(
        isinstance(quantity, int) for quantity in inventory.values()
    ), "Quantidades do inventário deveriam ser inteiros"
