"""AdobeUmapi Authentication."""

from singer_sdk.authenticators import OAuthJWTAuthenticator
import time
import jwt
from typing import Any, Union, List

class AdobeUmapiAuthenticator(OAuthJWTAuthenticator):
    """Authenticator class for AdobeUmapi."""

    @property
    def ims_host(self) -> str:
        return self.config.get('ims_host')

    @property
    def auth_endpoint(self) -> str:
        endpoint = "/ims/exchange/jwt"
        return f'{self.ims_host}{endpoint}'

    @property
    def oauth_scopes(self) -> List[str]:
        return ["ent_user_sdk"]

    @property
    def oauth_request_body(self) -> dict:
        """Return request body for OAuth request.

        Returns:
            Request body mapping for OAuth.
        """
        api_key = self.config.get("api_key")

        payload = {
            "exp": int(time.time()) + 60*60*24,
            "iss": self.config.get("organization_id"),
            "sub": self.config.get("technical_account_id"),
            "aud": f'{self.ims_host}/c/{api_key}'
        }

        for scope in self.oauth_scopes:
            scope_uri = f'{self.ims_host}/s/{scope}'
            payload[scope_uri] = True

        return payload

    @property
    def oauth_request_payload(self) -> dict:
        """Return request payload for OAuth request.

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
