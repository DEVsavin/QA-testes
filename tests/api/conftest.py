import pytest

from api.petstore_client import PetstoreClient


@pytest.fixture(scope="function")
def api_client() -> PetstoreClient:
    return PetstoreClient()
