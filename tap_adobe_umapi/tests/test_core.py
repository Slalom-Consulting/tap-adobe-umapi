"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_standard_tap_tests

from tap_adobe_umapi.tap import TapAdobeUmapi
from tap_adobe_umapi.tests.mock_api import mock_api

SAMPLE_CONFIG = {
    "client_id": "SampleClientId",
    "client_secret": "SampleClientSecret",
    "technical_account_id": "SampleTechnicalAccountId",
    "private_key": "SamplePrivateKey",
    "organization_id": "SampleOrganizationId",
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    config = SAMPLE_CONFIG
    tests = get_standard_tap_tests(TapAdobeUmapi, config=config)
    for test in tests:
        if test.__name__ in ("_test_stream_connections"):
            config["page"] = 0
            mock_api(test, config)
            continue

        test()


# TODO: Create additional tests as appropriate for your tap.
