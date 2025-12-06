from .bank_account import BankAccount, BankToken
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
        ba = BankAccount()

        cases: List[TestCase] = [
            TestCase("PL", ["PL"]),
            TestCase("123123123", ["123123123"]),
            TestCase(
                "PL12345678901234567890123456",
                [BankToken("PL")],
            ),
            TestCase(
                "PL12345678901234567890123456",
                [BankToken("PL")],
            ),
            TestCase(
            "DE1234567890123456612322",
                [BankToken("DE")],
            )
        ]

        for case in cases:
            tokens = case.input.split()
            got = ba.anonymize(tokens)
            self.assertEqual(got, case.expected)

if __name__ == '__main__':
    unittest.main()