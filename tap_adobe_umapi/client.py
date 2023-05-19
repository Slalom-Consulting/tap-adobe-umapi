"""REST client handling, including AdobeUmapiStream base class."""

from typing import Any, Generator, Optional
from urllib.parse import parse_qsl, urljoin

import requests
from memoization import cached
from singer_sdk.streams import RESTStream

from tap_adobe_umapi.auth import AdobeUmapiAuthenticator
from tap_adobe_umapi.paginator import AdobeUmapiPaginator

PAGINATION_INDEX = 0
API_URL = "https://usermanagement.adobe.io"


class AdobeUmapiStream(RESTStream):
    """AdobeUmapi stream class."""

    @property
    def url_base(self) -> str:
        base = self.config.get("api_url", API_URL)
        endpoint = "/v2/usermanagement"
        return urljoin(base, endpoint)

    @property
    @cached  # type: ignore[override]
    def authenticator(self) -> AdobeUmapiAuthenticator:
        return AdobeUmapiAuthenticator(self, oauth_scopes="ent_user_sdk")

    @property
    def http_headers(self) -> dict:
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "x-api-key": str(self.config["client_id"]),
        }

        if self.config.get("user_agent"):
            headers["User-Agent"] = str(self.config["user_agent"])

        return headers

    def backoff_wait_generator(self) -> Generator[float, Any, None]:
        def _backoff_from_headers(retriable_api_error) -> int:
            response_headers = retriable_api_error.response.headers
            retry_after = response_headers.get("Retry-After", 0)
            return int(retry_after)

        return self.backoff_runtime(value=_backoff_from_headers)

    def get_new_paginator(self) -> AdobeUmapiPaginator:
        return AdobeUmapiPaginator(PAGINATION_INDEX)

    def _get_strem_config(self) -> dict:
        """Get parameters set in config."""
        config: dict = {}

        stream_configs = self.config.get("stream_config", [])
        if not stream_configs:
            return config

        config_list = [
            conf for conf in stream_configs if conf.get("stream") == self.name
        ] or [None]
        config_dict = config_list[-1] or {}
        stream_config = {k: v for k, v in config_dict.items() if k != "stream"}
        return stream_config

    def _get_stream_params(self) -> dict:
        stream_params = self._get_strem_config().get("parameters", "")
        return {qry[0]: qry[1] for qry in parse_qsl(stream_params.lstrip("?"))}

    def get_url_params(self, context, next_page_token) -> dict:
        """Return a dictionary of values to be used in URL parameterization."""
        return self._get_stream_params()

    def prepare_request(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> requests.PreparedRequest:
        context = context.copy() if context else {}
        context["page"] = next_page_token or PAGINATION_INDEX
        return super().prepare_request(context, None)
