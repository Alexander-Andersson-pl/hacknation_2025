import unittest
import sys
from typing import List, Any

sys.path.append("src")
from .pesel_rule import PeselRule, PeselToken


class TestCase:
    def __init__(self, input: str, expected: List[Any]) -> None:
        self.input = input
        self.expected = expected


class TestPesel(unittest.TestCase):
    def test_anonymize(self):
        pesel_rule = PeselRule()

        cases: List[TestCase] = [
            TestCase("44051401359", [PeselToken()]),
            TestCase("44051-401359", ["44051-401359"]),
            TestCase("12345678901", ["12345678901"]),
        ]

        for case in cases:
            tokens = case.input.split()
            got = pesel_rule.anonymize(tokens)
            self.assertEqual(got, case.expected)


if __name__ == '__main__':
    unittest.main()
