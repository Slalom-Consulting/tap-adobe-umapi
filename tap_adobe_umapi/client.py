"""REST client handling, including AdobeUmapiStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_adobe_umapi.auth import AdobeUmapiAuthenticator


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class AdobeUmapiStream(RESTStream):
    """AdobeUmapi stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get("api_url")

    records_jsonpath = "$[*]"  # Or override `parse_response`.

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


#    def get_next_page_token(
#        self, response: requests.Response, previous_token: Optional[int]
#    ) -> Optional[Any]:
#        """Return a token for identifying next page or None if no more pages."""
#        
#        if previous_token:
#            last_page: bool = response.json().get("lastPage")
#
#            if not last_page:
#                next_page_token = 1 + previous_token
#
#        else:
#            next_page_token = 0
#
#        return next_page_token


    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

        
        # response_limit = 400
        # limit of 25 requests per min
        # response will give Retry-After: seconds
        # if that is given, add a wait before continue