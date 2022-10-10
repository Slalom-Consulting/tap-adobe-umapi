"""AdobeUmapi Authentication."""

from singer_sdk.authenticators import OAuthJWTAuthenticator
import time
import jwt
from typing import Any, Union

class AdobeUmapiAuthenticator(OAuthJWTAuthenticator):
    """Authenticator class for AdobeUmapi."""

    ims_host = "https://ims-na1.adobelogin.com"

    @property
    def auth_endpoint(self) -> str:
        return f'{self.ims_host}/ims/exchange/jwt'

    @property
    def jwt(self) -> str:
        """Return JSON WEB Token for Adobe Developer Console OAuth requests

        Returns:
            JSON WEB Token for OAuth.
        """

        private_key: Union[bytes, Any] = bytes(self.private_key, "UTF-8")
        private_key_string: Union[str, Any] = private_key.decode("UTF-8")
        api_key = self.config.get("api_key")
        expiration = self.config.get("jwt_expiration")
        expiration_max = 60*60*24

        if expiration > expiration_max:
            expiration = expiration_max

        payload = {
            "exp": int(time.time()) + expiration,
            "iss": self.config.get("organization_id"),
            "sub": self.config.get("technical_account_id"),
            "aud": f'{self.ims_host}/c/{api_key}'
        }

        for scope in self.oauth_scopes:
            scope_uri = f'{self.ims_host}/s/{scope}'
            payload[scope_uri] = True

        return jwt.encode(payload, private_key_string, "RS256")

    @property
    def oauth_request_payload(self) -> dict:
        """Return request payload for OAuth request.

        Returns:
            Payload object for OAuth.
        """

        return {
            "client_id": self.config.get("api_key"),
            "client_secret": self.client_secret,
            "jwt_token": self.jwt
        }
