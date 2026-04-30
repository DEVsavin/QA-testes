from tests.api.helpers import build_pet_payload, unique_id


def test_cria_atualiza_consulta_e_remove_pet(api_client):
    payload = build_pet_payload(status="available")
    pet_id = payload["id"]

    create_response = api_client.post("/pet", json=payload)
    api_client.assert_status(create_response, 200, "/pet")
    created_pet = api_client.json(create_response)

    assert created_pet["id"] == pet_id, "ID do pet criado não confere"
    assert created_pet["name"] == payload["name"], "Nome do pet criado não confere"
    assert created_pet["status"] == "available", "Status inicial do pet não confere"

    try:
        updated_payload = {**payload, "status": "sold", "name": f"{payload['name']}-updated"}
        update_response = api_client.put("/pet", json=updated_payload)
        api_client.assert_status(update_response, 200, "/pet")
        updated_pet = api_client.json(update_response)

        assert updated_pet["id"] == pet_id, "ID do pet atualizado não confere"
        assert updated_pet["name"] == updated_payload["name"], "Nome atualizado não confere"
        assert updated_pet["status"] == "sold", "Status atualizado do pet não confere"

        get_response = api_client.get(f"/pet/{pet_id}")
        api_client.assert_status(get_response, 200, f"/pet/{pet_id}")
        fetched_pet = api_client.json(get_response)

        assert fetched_pet["id"] == pet_id, "ID do pet consultado não confere"
        assert fetched_pet["name"] == updated_payload["name"], "Nome consultado não confere"
        assert fetched_pet["status"] == "sold", "Status consultado não confere"
    finally:
        delete_response = api_client.delete(f"/pet/{pet_id}")
        api_client.assert_status(delete_response, 200, f"/pet/{pet_id}")


def test_consulta_pet_inexistente_retorna_404(api_client):
    missing_pet_id = unique_id()

    response = api_client.get(f"/pet/{missing_pet_id}")

    api_client.assert_status(response, 404, f"/pet/{missing_pet_id}")
    body = api_client.json(response)
    assert body["type"] == "error", "Tipo do erro deveria indicar falha"
    assert "Pet not found" in body["message"], "Mensagem deveria indicar pet inexistente"


def test_lista_pets_por_status_disponivel(api_client):
    response = api_client.get("/pet/findByStatus", params={"status": "available"})

    api_client.assert_status(response, 200, "/pet/findByStatus")
    pets = api_client.json(response)

    assert isinstance(pets, list), "Busca por status deveria retornar uma lista"
    assert pets, "Lista de pets disponíveis não deveria estar vazia na base pública"
    assert all("status" in pet for pet in pets[:10]), "Pets retornados deveriam ter campo status"
