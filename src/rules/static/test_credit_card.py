from .credit_card import CreditCard, CreditCardToken
from typing import List
import unittest


class TestCase:
    input: str
    expected_ok: bool

    def __init__(self, input: str, expected_ok: bool) -> None:
        self.input = input
        self.expected_ok = expected_ok

class BankAccountTest(unittest.TestCase):
    def test_anonymize(self):
        ba = CreditCard()

        cases: List[TestCase] = [
            TestCase(
                "1231231231231",
                True,
            ),
        ]

        for case in cases:
            _, ok = ba.anonymize(case.input)
            self.assertEqual(ok, case.expected_ok)


if __name__ == '__main__':
    unittest.main()