"""AdobeUmapi tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers
# TODO: Import your custom stream types here:
from tap_adobe_umapi.streams import (
    AdobeUmapiStream,
    UsersStream,
)
# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    UsersStream,

]


class TapAdobeUmapi(Tap):
    """AdobeUmapi tap class."""
    name = "tap-adobe-umapi"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "organization_id",
            th.StringType,
            required=True,
            description=""
        ),
        th.Property(
            "technical_account_id",
            th.StringType,
            required=True,
            description=""
        ),
        th.Property(
            "api_key",
            th.StringType,
            required=True,
            description=""
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            description=""
        ),
        th.Property(
            "private_key",
            th.StringType,
            required=True,
            description=""
        ),
        th.Property(
            "api_url",
            th.StringType,
            default="https://usermanagement.adobe.io/v2/usermanagement",
            description="The url for the API service"
        ),
        th.Property(
            "ims_host",
            th.StringType,
            default="https://ims-na1.adobelogin.com",
            description="The url for the API service"
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
