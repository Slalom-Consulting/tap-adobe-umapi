"""REST client handling, including AdobeUmapiStream base class."""

from typing import Callable, Generator, Any, Optional
from singer_sdk.streams import RESTStream
from tap_adobe_umapi.auth import AdobeUmapiAuthenticator
from tap_adobe_umapi.paginator import AdobeUmapiPaginator
from memoization import cached
from urllib.parse import urljoin
import requests

PAGINATION_INDEX = 0
API_URL = 'https://usermanagement.adobe.io'


class AdobeUmapiStream(RESTStream):
    """AdobeUmapi stream class."""
    @property
    def url_base(self) -> str:
        base = self.config.get('api_url', API_URL)
        endpoint = '/v2/usermanagement'
        return urljoin(base, endpoint)

    @property
    @cached
    def authenticator(self) -> AdobeUmapiAuthenticator:
        return AdobeUmapiAuthenticator(self, oauth_scopes=['ent_user_sdk'])

    @property
    def http_headers(self) -> dict:
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'x-api-key': str(self.config.get('client_id')),
        }

        if self.config.get('user_agent'):
            headers['User-Agent'] = self.config.get('user_agent')

        return headers

    def backoff_wait_generator(self) -> Callable[..., Generator[int, Any, None]]:
        def _backoff_from_headers(retriable_api_error) -> int:
            response_headers = retriable_api_error.response.headers
            retry_after = response_headers.get('Retry-After', 0)
            return int(retry_after)

        return self.backoff_runtime(value=_backoff_from_headers)

    def get_new_paginator(self) -> AdobeUmapiPaginator:
        return AdobeUmapiPaginator(PAGINATION_INDEX)

    def prepare_request(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> requests.PreparedRequest:
        context = context.copy() if context else {}
        context['page'] = next_page_token or PAGINATION_INDEX
        return super().prepare_request(context, None)
