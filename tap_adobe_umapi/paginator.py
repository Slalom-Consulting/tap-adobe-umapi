"""Pagination handling for AdobeUmapiStream."""

from singer_sdk.pagination import BaseAPIPaginator
from requests import Response
from typing import Any, Union


class AdobeUmapiPaginator(BaseAPIPaginator):
    """Paginator class for APIs that use page number."""

    def __init__(self) -> None:
        """Create a new paginator.
        """
        super().__init__(None)

    def get_next(self, response: Response) -> Union[int, None]:
        """Get the next page token.
        Args:
            response: API response object.
        Returns:
            The next page token.
        """
        is_last_page:bool = response.json().get("lastPage", None)
        
        if is_last_page == False:
            current_page = int(response.headers.get("X-Next-Page"))
            return current_page + 1
