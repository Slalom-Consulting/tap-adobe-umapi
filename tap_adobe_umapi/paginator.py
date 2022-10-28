"""Pagination handling for AdobeUmapiStream."""

from singer_sdk.pagination import BasePageNumberPaginator
from requests import Response


class AdobeUmapiPaginator(BasePageNumberPaginator):
    """Paginator class for APIs that use page number."""
    def has_more(self, response: Response) -> bool:
        return response.json().get('lastPage', True) == False
