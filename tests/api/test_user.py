from tests.api.helpers import build_user_payload, unique_username


def test_cria_consulta_e_remove_usuario(api_client):
    payload = build_user_payload()
    username = payload["username"]

    create_response = api_client.post("/user", json=payload)
    api_client.assert_status(create_response, 200, "/user")

    try:
        get_response = api_client.get(f"/user/{username}")
        api_client.assert_status(get_response, 200, f"/user/{username}")
        user = api_client.json(get_response)

        assert user["id"] == payload["id"], "ID do usuário retornado não confere"
        assert user["username"] == username, "Username retornado não confere"
        assert user["email"] == payload["email"], "E-mail retornado não confere"
        assert user["userStatus"] == payload["userStatus"], "Status do usuário não confere"
    finally:
        delete_response = api_client.delete(f"/user/{username}")
        api_client.assert_status(delete_response, 200, f"/user/{username}")


def test_consulta_usuario_inexistente_retorna_404(api_client):
    username = unique_username(prefix="usuario_inexistente")

    response = api_client.get(f"/user/{username}")

    api_client.assert_status(response, 404, f"/user/{username}")
    body = api_client.json(response)
    assert body["type"] == "error", "Tipo do erro deveria indicar falha"
    assert "User not found" in body["message"], "Mensagem deveria indicar usuário inexistente"
