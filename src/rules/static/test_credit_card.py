from .credit_card import CreditCard, CreditCardToken
from typing import List, Any
import unittest


class TestCase:
    input: str
    expected: List[Any]

    def __init__(self, input: str, expected: List[Any]) -> None:
        self.input = input
        self.expected = expected

class BankAccountTest(unittest.TestCase):
    def test_anonymize(self):
        ba = CreditCard()

        cases: List[TestCase] = [
            TestCase(
                "1231231231231",
                [CreditCardToken()],
            ),
        ]

        for case in cases:
            tokens = case.input.split()
            got = ba.anonymize(tokens)
            self.assertEqual(got, case.expected)


if __name__ == '__main__':
    unittest.main()