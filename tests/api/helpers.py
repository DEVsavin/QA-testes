from __future__ import annotations

from datetime import datetime, timezone
import random
import time


def unique_id() -> int:
    """Gera um ID numérico grande o suficiente para evitar colisões na Petstore pública."""
    timestamp_ms = int(time.time() * 1000)
    suffix = random.randint(1000, 9999)
    return int(f"{timestamp_ms}{suffix}")


def unique_username(prefix: str = "gsd_user") -> str:
    return f"{prefix}_{unique_id()}"


def build_user_payload(user_id: int | None = None, username: str | None = None) -> dict:
    resolved_id = user_id or unique_id()
    resolved_username = username or f"gsd_user_{resolved_id}"

    return {
        "id": resolved_id,
        "username": resolved_username,
        "firstName": "GSD",
        "lastName": "Automation",
        "email": f"{resolved_username}@example.com",
        "password": "secret123",
        "phone": "11999999999",
        "userStatus": 1,
    }


def build_pet_payload(pet_id: int | None = None, status: str = "available") -> dict:
    resolved_id = pet_id or unique_id()

    return {
        "id": resolved_id,
        "category": {"id": 1, "name": "dogs"},
        "name": f"pet-{resolved_id}",
        "photoUrls": ["https://example.com/pet.png"],
        "tags": [{"id": 1, "name": "automation"}],
        "status": status,
    }


def build_order_payload(
    order_id: int | None = None,
    pet_id: int | None = None,
    quantity: int = 1,
    status: str = "placed",
    complete: bool = True,
) -> dict:
    resolved_order_id = order_id or unique_id()
    resolved_pet_id = pet_id or unique_id()

    return {
        "id": resolved_order_id,
        "petId": resolved_pet_id,
        "quantity": quantity,
        "shipDate": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "complete": complete,
    }
