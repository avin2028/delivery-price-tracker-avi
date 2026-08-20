import json
import unittest
from unittest.mock import patch

import delivery_price_tracker


class _MockResponse:
    def __init__(self, payload: dict):
        self._raw = json.dumps(payload).encode("utf-8")

    def read(self):
        return self._raw

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FetchPriceTests(unittest.TestCase):
    def test_fetch_price_returns_float_price(self):
        with patch(
            "delivery_price_tracker.urllib.request.urlopen",
            return_value=_MockResponse({"price": "12.5"}),
        ):
            self.assertEqual(delivery_price_tracker.fetch_price("http://example", 1), 12.5)

    def test_fetch_price_requires_price_field(self):
        with patch(
            "delivery_price_tracker.urllib.request.urlopen",
            return_value=_MockResponse({"amount": 20}),
        ):
            with self.assertRaises(ValueError):
                delivery_price_tracker.fetch_price("http://example", 1)


if __name__ == "__main__":
    unittest.main()
