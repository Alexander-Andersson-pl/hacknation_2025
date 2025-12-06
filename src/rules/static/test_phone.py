import unittest

import sys
from typing import List, Any

sys.path.append("src")

from .phone import Phone, PhoneToken


class TestCase:
    def __init__(self, input: str, expected: List[Any]) -> None:
        self.input = input
        self.expected = expected


class TestPhone(unittest.TestCase):
    def test_anonymize(self):
        phone_rule = Phone()

        cases: List[TestCase] = [
            TestCase("48123123123", [PhoneToken()]),
            TestCase("+375291231231", [PhoneToken()]),
            TestCase("123123123", [PhoneToken()]),
        ]

        for case in cases:
            tokens = case.input.split()
            got = phone_rule.anonymize(tokens)
            self.assertEqual(got, case.expected)


if __name__ == "__main__":
    unittest.main()
