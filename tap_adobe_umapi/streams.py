"""Stream type classes for tap-adobe-umapi."""

from pathlib import Path

from tap_adobe_umapi.client import AdobeUmapiStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class UsersStream(AdobeUmapiStream):
    """Define custom stream."""

    name = "users"
    path = "/users/{organization_id}/{page}"
    records_jsonpath = "$.users[*]"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR.joinpath("users.json")


class GroupsStream(AdobeUmapiStream):
    """Define custom stream."""

    name = "groups"
    path = "/groups/{organization_id}/{page}"
    records_jsonpath = "$.groups[*]"
    primary_keys = ["groupId"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR.joinpath("groups.json")
