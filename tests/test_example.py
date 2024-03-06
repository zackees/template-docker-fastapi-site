"""
Example test.
"""

import unittest

from mediabiasscorer.version import VERSION


class ExampleTester(unittest.TestCase):
    """Example tester."""

    def test_example(self) -> None:
        """Example tester."""
        self.assertEqual(VERSION, "1.0.0")


if __name__ == "__main__":
    unittest.main()
