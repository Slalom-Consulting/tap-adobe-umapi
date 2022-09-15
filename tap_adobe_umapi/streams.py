"""Stream type classes for tap-adobe-umapi."""

from pathlib import Path
from tap_adobe_umapi.client import AdobeUmapiStream


SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class UsersStream(AdobeUmapiStream):
    """Define custom stream."""
    name = "users"
    path = "/users/{orgId}/{page}"
    records_jsonpath = "$.users[*]"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "users.json"

class GroupsStream(AdobeUmapiStream):
    """Define custom stream."""
    name = "groups"
    path = "/groups/{orgId}/{page}"
    records_jsonpath = "$.groups[*]"
    primary_keys = ["groupId"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "groups.json"
    