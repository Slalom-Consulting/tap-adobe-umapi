"""REST client handling, including AdobeUmapiStream base class."""

from typing import Callable, Generator, Any
from singer_sdk.streams import RESTStream
from tap_adobe_umapi.auth import AdobeUmapiAuthenticator
from tap_adobe_umapi.paginator import AdobeUmapiPaginator
from memoization import cached
from urllib.parse import urljoin
import requests

PAGINATION_INDEX = 0
API_HOST = 'https://usermanagement.adobe.io'


class AdobeUmapiStream(RESTStream):
    """AdobeUmapi stream class."""
    @property
    def url_base(self) -> str:
        host = self.config.get('api_url', API_HOST)
        path = '/v2/usermanagement'
        return urljoin(host, path)

    @property
    @cached
    def authenticator(self) -> AdobeUmapiAuthenticator:
        """Return a new authenticator object."""
        return AdobeUmapiAuthenticator(self, oauth_scopes=['ent_user_sdk'])

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            'x-api-key': str(self.config.get('client_id')),
        }

        if 'user_agent' in self.config:
            headers['User-Agent'] = self.config.get('user_agent')

        return headers

    def get_new_paginator(self) -> AdobeUmapiPaginator:
        """Get a fresh paginator for this API endpoint.
        Returns:
            A paginator instance.
        """
        return AdobeUmapiPaginator(PAGINATION_INDEX)

    def backoff_wait_generator(self) -> Callable[..., Generator[int, Any, None]]:
        def _backoff_from_headers(retriable_api_error) -> int:
            response_headers = retriable_api_error.response.headers
            return int(response_headers.get('Retry-After', 0))

        return self.backoff_runtime(value=_backoff_from_headers)

    def prepare_request(self, context, next_page_token) -> requests.PreparedRequest:
        """Prepare a request object for this stream.
        If partitioning is supported, the `context` object will contain the partition
        definitions. Pagination information can be parsed from `next_page_token` if
        `next_page_token` is not None.
        Args:
            context: Stream partition or context dictionary.
            next_page_token: Token, page number or any request argument to request the
                next page of data.
        Returns:
            Build a request with the stream's URL, path, query parameters,
            HTTP headers and authenticator.
        """
        
        if not context:
            context = {}

        context['page'] = next_page_token or PAGINATION_INDEX

        http_method = self.rest_method
        url: str = self.get_url(context)
        params: dict = self.get_url_params(context, None)
        request_data = self.prepare_request_payload(context, None)
        headers = self.http_headers

        return self.build_prepared_request(
           method=http_method,
           url=url,
           params=params,
           headers=headers,
           json=request_data,
        )
