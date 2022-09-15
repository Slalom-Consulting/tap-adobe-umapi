from singer_sdk.pagination import BaseAPIPaginator
from requests import Response
from typing import Any, Union

##TODO: test for correct next page number
class AdobeUmapiPaginator(BaseAPIPaginator):
    """Paginator class for APIs that use page number."""

    def __init__(
        self,
        #jsonpath: str,
        key: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Create a new paginator.
        Args:
            jsonpath: A JSONPath expression.
            args: Paginator positional arguments for base class.
            kwargs: Paginator keyword arguments for base class.
        """
        super().__init__(None, *args, **kwargs)
        #self._jsonpath = jsonpath

    def get_next(self, response: Response) -> Union[int, None]:
        """Get the next page token.
        Args:
            response: API response object.
        Returns:
            The next page token.
        """
        #all_matches = extract_jsonpath(self._jsonpath, response.json())
        #return next(all_matches, None)
        is_last_page:bool = response.json().get("lastPage", None)
        
        if is_last_page == False:
            current_page = int(response.headers.get(self._key))
            return current_page + 1

