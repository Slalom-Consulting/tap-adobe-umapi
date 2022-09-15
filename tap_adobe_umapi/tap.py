"""AdobeUmapi tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_adobe_umapi.streams import (
    UsersStream,
    GroupsStream
)

STREAM_TYPES = [
    UsersStream,
    GroupsStream
]


class TapAdobeUmapi(Tap):
    """AdobeUmapi tap class."""
    name = "tap-adobe-umapi"

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
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
