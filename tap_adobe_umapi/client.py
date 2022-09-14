"""REST client handling, including AdobeUmapiStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable, Callable, Generator

from memoization import cached
import backoff
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from tap_adobe_umapi.auth import AdobeUmapiAuthenticator
from tap_adobe_umapi.paginator import AdobeUmapiPaginator, BaseAPIPaginator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class AdobeUmapiStream(RESTStream):
    """AdobeUmapi stream class."""
    
    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get("api_url")

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
        return AdobeUmapiPaginator("X-Next-Page")

    ##TODO: fix backoff issue from Adobe server
    def backoff_wait_generator(self) -> Callable[..., Generator[int, Any, None]]:
        """The wait generator used by the backoff decorator on request failure.
        See for options:
        https://github.com/litl/backoff/blob/master/backoff/_wait_gen.py
        And see for examples: `Code Samples <../code_samples.html#custom-backoff>`_
        Returns:
            The wait generator
        """
        
        return backoff.constant(60)  # type: ignore # ignore 'Returning Any'

#   def backoff_wait_generator(self) -> Callable[..., Generator[int, Any, None]]:
#       def _backoff_from_headers(retriable_api_error):
#           response_headers = retriable_api_error.headers
#           return int(response_headers.get("Retry-After", 0))
#
#       return self.backoff_runtime(value=_backoff_from_headers)

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

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

        
        # response_limit = 400
        # limit of 25 requests per min
        # response will give Retry-After: seconds
        # if that is given, add a wait before continue