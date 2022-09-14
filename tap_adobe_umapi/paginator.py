from singer_sdk.pagination import SimpleHeaderPaginator, BaseAPIPaginator
from requests import Response

class AdobeUmapiPaginator(SimpleHeaderPaginator):
    """Paginator class for APIs that use page number."""

    def has_more(self, response: Response) -> bool:
        """Override this method to check if the endpoint has any pages left.
        Args:
            response: API response object.
        Returns:
            Boolean flag used to indicate if the endpoint has more pages.
        """
        return False #response.json().get("lastPage", False)
        

    def get_next(self, response: Response) -> int:
        """Get the next page token.
        Args:
            response: API response object.
        Returns:
            The next page token.
        """
        if self.has_more:
            next_page = response.headers.get(self._key) + 1
            print(next_page)
        
        return next_page
