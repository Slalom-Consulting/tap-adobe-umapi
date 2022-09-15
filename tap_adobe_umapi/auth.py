"""AdobeUmapi Authentication."""

from singer_sdk.authenticators import OAuthJWTAuthenticator
import time
import jwt
from typing import Any, Union

class AdobeUmapiAuthenticator(OAuthJWTAuthenticator):
    """Authenticator class for AdobeUmapi."""

    ims_host = "https://ims-na1.adobelogin.com"

    @property
    def oauth_request_body(self) -> dict:
        """Return request body for OAuth request.

        Returns:
            Request body mapping for OAuth.
        """

        ims_host = self.ims_host
        api_key = self.config.get("api_key")

        payload = {
            "exp": int(time.time()) + 60*60*24,
            "iss": self.config.get("organization_id"),
            "sub": self.config.get("technical_account_id"),
            "aud": f'{ims_host}/c/{api_key}'
        }

        for scope in self.oauth_scopes:
            scope_uri = f'{ims_host}/s/{scope}'
            payload[scope_uri] = True

        return payload

    @property
    def oauth_request_payload(self) -> dict:
        """Return request paytload for OAuth request.

        Returns:
            Payload object for OAuth.

        Raises:
            ValueError: If the private key is not set.
        """
        if not self.private_key:
            raise ValueError("Missing 'private_key' property for OAuth payload.")

        private_key: Union[bytes, Any] = bytes(self.private_key, "UTF-8")
        private_key_string: Union[str, Any] = private_key.decode("UTF-8")

        return {
            "client_id": self.config.get("api_key"),
            "client_secret": self.client_secret,
            "jwt_token": jwt.encode(
                self.oauth_request_body, private_key_string, "RS256"
            )
        }

    @classmethod
    def create_for_stream(cls, stream) -> "AdobeUmapiAuthenticator":
        return cls(
            stream=stream,
            auth_endpoint = f'{cls.ims_host}/ims/exchange/jwt',
            oauth_scopes = ["ent_user_sdk"]
        )
