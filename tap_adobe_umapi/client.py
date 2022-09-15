"""REST client handling, including AdobeUmapiStream base class."""

import requests
from pathlib import Path

from memoization import cached
from singer_sdk.streams import RESTStream
from tap_adobe_umapi.auth import AdobeUmapiAuthenticator
from tap_adobe_umapi.paginator import AdobeUmapiPaginator, BaseAPIPaginator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class AdobeUmapiStream(RESTStream):
    """AdobeUmapi stream class."""
    
    url_base = "https://usermanagement.adobe.io/v2/usermanagement"

    @property
    @cached
    def authenticator(self) -> AdobeUmapiAuthenticator:
        """Return a new authenticator object."""
        return AdobeUmapiAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""

        headers = {
            "Content-type" : "application/json",
            "Accept" : "application/json",
            "x-api-key": self.config.get("api_key"),
        }

        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")

        return headers

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Get a fresh paginator for this API endpoint.
        Returns:
            A paginator instance.
        """
        return AdobeUmapiPaginator()

    ##TODO: fix backoff issue from Adobe server
    #def backoff_runtime(
    #    self, *, value: Callable[[Any], int]
    #) -> Generator[int, None, None]:
    #    """Optional backoff wait generator that can replace the default `backoff.expo`.
    #    It is based on parsing the thrown exception of the decorated method, making it
    #    possible for response values to be in scope.
    #    Args:
    #        value: a callable which takes as input the decorated
    #            function's thrown exception and determines how
    #            long to wait.
    #    Yields:
    #        The thrown exception
    #    """
    #    exception = yield  # type: ignore[misc]
    #    while True:
    #        exception = yield value(exception)

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

        context["orgId"] = self.config.get("organization_id")
        context["page"] = next_page_token or 0

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
