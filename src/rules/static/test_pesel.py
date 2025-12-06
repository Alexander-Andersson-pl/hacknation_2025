import sys
from typing import List

sys.path.append("src")

from pesel_rule import PeselRule


class TestCase:
    def __init__(self, input: str, valid: bool) -> None:
        self.input = input
        self.valid = valid


def test_pesel_anonymize():
    pesel_rule = PeselRule()

    cases: List[TestCase] = [
        TestCase("PESEL: 44051401359", True),
        TestCase("Z myślnikiem 44051-401359", True),
        TestCase("Zły numer 12345678901", False),
    ]

    for case in cases:
        token, ok = pesel_rule.anonymize(case.input)
        assert ok == case.valid
        if ok:
            assert token.label() == "{pesel}"
        else:
            assert token.label() == "{pesel}"
