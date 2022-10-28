"""AdobeUmapi Authentication."""

from typing import Any, Union
from singer_sdk.authenticators import OAuthJWTAuthenticator
import jwt
import time

IMS_HOST = 'https://ims-na1.adobelogin.com'


class AdobeUmapiAuthenticator(OAuthJWTAuthenticator):
    """Authenticator class for AdobeUmapi."""
    @property
    def auth_endpoint(self) -> str:
        return f'{IMS_HOST}/ims/exchange/jwt'

    @property
    def oauth_request_body(self) -> dict:
        expiration = self.config.get('auth_expiration')
        expiration_max = 60*60*24

        if expiration > expiration_max:
            expiration = expiration_max

        payload = {
            'exp': int(time.time()) + expiration,
            'iss': self.config.get('organization_id'),
            'sub': self.config.get('technical_account_id'),
            'aud': f'{IMS_HOST}/c/{self.client_id}'
        }

        for scope in self.oauth_scopes:
            scope_uri = f'{IMS_HOST}/s/{scope}'
            payload[scope_uri] = True

        return payload

    @property
    def oauth_request_payload(self) -> dict:
        private_key: Union[bytes, Any] = bytes(self.private_key, 'UTF-8')
        private_key_string: Union[str, Any] = private_key.decode('UTF-8')
        
        return {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'jwt_token': jwt.encode(
                self.oauth_request_body, private_key_string, 'RS256'
            ),
        }
