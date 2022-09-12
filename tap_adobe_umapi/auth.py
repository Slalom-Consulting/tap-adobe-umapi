"""AdobeUmapi Authentication."""


from singer_sdk.authenticators import OAuthJWTAuthenticator


class AdobeUmapiAuthenticator(OAuthJWTAuthenticator):
    """Authenticator class for AdobeUmapi."""

    @classmethod
    def create_for_stream(cls, stream) -> "AdobeUmapiAuthenticator":
        return cls(
            stream=stream,
            auth_endpoint="TODO: OAuth Endpoint URL",
            oauth_scopes="TODO: OAuth Scopes",
        )

