from tests.api.helpers import (
    build_order_payload,
    build_pet_payload,
    build_user_payload,
    unique_id,
    unique_username,
)


def test_unique_id_generates_integer_values():
    first_id = unique_id()
    second_id = unique_id()

    assert isinstance(first_id, int)
    assert isinstance(second_id, int)
    assert first_id != second_id


def test_payload_helpers_use_consistent_unique_values():
    user_id = unique_id()
    username = unique_username()
    user_payload = build_user_payload(user_id=user_id, username=username)
    pet_payload = build_pet_payload(pet_id=user_id)
    order_payload = build_order_payload(order_id=user_id, pet_id=pet_payload["id"])

    assert user_payload["id"] == user_id
    assert user_payload["username"] == username
    assert user_payload["email"] == f"{username}@example.com"
    assert pet_payload["id"] == user_id
    assert pet_payload["status"] == "available"
    assert order_payload["id"] == user_id
    assert order_payload["petId"] == pet_payload["id"]
