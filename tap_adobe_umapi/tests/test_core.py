"""Tests standard tap features using the built-in SDK tests library."""

import datetime
from singer_sdk.testing import get_standard_tap_tests
from tap_adobe_umapi.tap import TapAdobeUmapi
import json

with open('.secrets/config.json', 'r') as f:
    SAMPLE_CONFIG = json.load(f)


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(
        TapAdobeUmapi,
        config=SAMPLE_CONFIG
    )
    for test in tests:
        test()


# TODO: Create additional tests as appropriate for your tap.
