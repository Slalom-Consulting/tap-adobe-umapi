"""Tests standard tap features using the built-in SDK tests library."""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from singer_sdk.testing import get_standard_tap_tests

from tap_adobe_umapi.tap import TapAdobeUmapi
from tap_adobe_umapi.tests.mock_api import mock_api


def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    return private_pem.decode("ascii")


SAMPLE_CONFIG = {
    "client_id": "SampleClientId",
    "client_secret": "SampleClientSecret",
    "technical_account_id": "SampleTechnicalAccountId",
    "private_key": generate_private_key(),
    "organization_id": "SampleOrganizationId",
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG
    config["page"] = "0"
    tests = get_standard_tap_tests(TapAdobeUmapi, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            mock_api(test, config)
            continue

        test()
