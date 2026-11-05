"""Check requirements with unittest. Try: remove the input check, then repair it."""

import unittest


def quote_transport(container_count: int, usd_per_container: float) -> float:
    if container_count <= 0 or usd_per_container <= 0:
        raise ValueError("Count and rate must be positive.")
    return container_count * usd_per_container


class QuoteTests(unittest.TestCase):
    def test_three_container_quote(self):
        self.assertEqual(quote_transport(3, 120.0), 360.0)

    def test_zero_container_booking_is_rejected(self):
        with self.assertRaises(ValueError):
            quote_transport(0, 120.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

