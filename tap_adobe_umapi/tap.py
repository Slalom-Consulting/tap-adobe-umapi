"""AdobeUmapi tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_adobe_umapi.streams import GroupsStream, UsersStream

STREAM_TYPES = [UsersStream, GroupsStream]


class TapAdobeUmapi(Tap):
    """AdobeUmapi tap class."""

    name = "tap-adobe-umapi"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            description="The Client ID for the service account (JWT).",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,
            description="The Client Secret for the service account (JWT).",
        ),
        th.Property(
            "technical_account_id",
            th.StringType,
            required=True,
            description="The Technical Account ID for the service account (JWT).",
        ),
        th.Property(
            "private_key",
            th.StringType,
            required=True,
            secret=True,
            description="The Private Key for the service account (JWT).",
        ),
        th.Property(
            "organization_id",
            th.StringType,
            required=True,
            description="The unique identifier for an organization.",
        ),
        th.Property(
            "auth_expiration",
            th.NumberType,
            description=(
                "Expiraton in seconds for JWT exchange "
                "(Max: 86400, Recomended as small as possible)."
            ),
            default=300,
        ),
        th.Property(
            "user_agent", th.StringType, description="User agent to present to the API."
        ),
        th.Property(
            "api_url",
            th.StringType,
            description="Override the Adobe User Management API base URL.",
        ),
        th.Property(
            "auth_url",
            th.StringType,
            description="Override the Adobe authentication API base URL.",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapAdobeUmapi.cli()
