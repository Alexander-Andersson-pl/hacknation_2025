import unittest

import sys
from typing import List

sys.path.append("src")

from .phone import Phone


class TestCase:
    def __init__(self, input: str, valid: bool) -> None:
        self.input = input
        self.valid = valid


class TestPhone(unittest.TestCase):
    def test_anonymize(self):
        phone_rule = Phone()

        cases: List[TestCase] = [
            TestCase("48123123123", True),
            TestCase("+375291231231", True),
            TestCase("123123123", True),
        ]

        for case in cases:
            token, ok = phone_rule.anonymize(case.input)
            self.assertEqual(ok, case.valid)


if __name__ == "__main__":
    unittest.main()
