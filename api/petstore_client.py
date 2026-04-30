from __future__ import annotations
from typing import Any
from urllib.parse import urljoin
import requests
from config import settings


class PetstoreClient:
    def __init__(self, base_url: str | None = None, timeout: int = 15):
        self.base_url = (base_url or settings.petstore_base_url).rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def request(self, method: str, endpoint: str, **kwargs: Any) -> requests.Response:
        url = self._url(endpoint)
        kwargs.setdefault("timeout", self.timeout)
        response = self.session.request(method=method, url=url, **kwargs)
        return response

    def get(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs: Any) -> requests.Response:
        return self.request("DELETE", endpoint, **kwargs)

    def assert_status(
        self,
        response: requests.Response,
        expected_status: int | tuple[int, ...],
        endpoint: str | None = None,
    ) -> None:
        expected = (
            expected_status
            if isinstance(expected_status, tuple)
            else (expected_status,)
        )

        if response.status_code in expected:
            return

        method = response.request.method if response.request else "UNKNOWN"
        resolved_endpoint = endpoint or self._endpoint_from_response(response)
        expected_text = ", ".join(str(status) for status in expected)

        raise AssertionError(
            "Resposta inesperada da Petstore.\n"
            f"Método: {method}\n"
            f"Endpoint: {resolved_endpoint}\n"
            f"Status esperado: {expected_text}\n"
            f"Status recebido: {response.status_code}\n"
            f"Body: {self._safe_body(response)}"
        )

    def json(self, response: requests.Response) -> Any:
        try:
            return response.json()
        except ValueError as exc:
            raise AssertionError(
                "Resposta da Petstore não é JSON válido.\n"
                f"Status recebido: {response.status_code}\n"
                f"Body: {self._safe_body(response)}"
            ) from exc

    def _url(self, endpoint: str) -> str:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        normalized_endpoint = endpoint.lstrip("/")
        return urljoin(f"{self.base_url}/", normalized_endpoint)

    def _endpoint_from_response(self, response: requests.Response) -> str:
        url = response.url
        if url.startswith(self.base_url):
            return url.removeprefix(self.base_url) or "/"
        return url

    @staticmethod
    def _safe_body(response: requests.Response, max_length: int = 1000) -> str:
        body = response.text or "<empty>"
        if len(body) <= max_length:
            return body
        return f"{body[:max_length]}... <truncated>"
