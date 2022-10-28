"""REST client handling, including AdobeUmapiStream base class."""

import requests
from memoization import cached
from singer_sdk.streams import RESTStream
from tap_adobe_umapi.auth import AdobeUmapiAuthenticator
from tap_adobe_umapi.paginator import AdobeUmapiPaginator


class AdobeUmapiStream(RESTStream):
    """AdobeUmapi stream class."""
    @property
    def url_base(self) -> str:
        return self.config['api_url']
    
    extra_retry_statuses = [429]

    @property
    @cached
    def authenticator(self) -> AdobeUmapiAuthenticator:
        """Return a new authenticator object."""
        return AdobeUmapiAuthenticator(self, oauth_scopes=["ent_user_sdk"])

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "x-api-key": self.config["api_key"],
        }

        if "user_agent" in self.config:
            headers["User-Agent"] = self.config["user_agent"]

        return headers

    def get_new_paginator(self) -> AdobeUmapiPaginator:
        """Get a fresh paginator for this API endpoint.
        Returns:
            A paginator instance.
        """
        return AdobeUmapiPaginator()

    def backoff_wait_generator(self):
        def get_wait_time_from_response(exception):
            advice = int(exception.response.headers.get("Retry-After", 0))
            return advice

        return self.backoff_runtime(value=get_wait_time_from_response)

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

        context["orgId"] = self.config["organization_id"]
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
