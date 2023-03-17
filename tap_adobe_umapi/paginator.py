"""Pagination handling for AdobeUmapiStream."""

from requests import Response
from singer_sdk.pagination import BasePageNumberPaginator


class AdobeUmapiPaginator(BasePageNumberPaginator):
    """Paginator class for APIs that use page number."""

    def has_more(self, response: Response) -> bool:
        is_last_page: bool = response.json().get("lastPage") or True
        return not is_last_page
