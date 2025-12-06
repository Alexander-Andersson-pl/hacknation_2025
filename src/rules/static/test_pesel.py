import unittest

import sys
from typing import List

sys.path.append("src")

from .pesel_rule import PeselRule


class TestCase:
    def __init__(self, input: str, valid: bool) -> None:
        self.input = input
        self.valid = valid

class TestPesel(unittest.TestCase):
    def test_anonymize(self):
        pesel_rule = PeselRule()

        cases: List[TestCase] = [
            TestCase("44051401359", True),
            TestCase("44051-401359", False),
            TestCase("12345678901", False),
        ]

        for case in cases:
            token, ok = pesel_rule.anonymize(case.input)
            self.assertEqual(ok, case.valid)

if __name__ == '__main__':
    unittest.main()