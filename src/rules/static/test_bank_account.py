from .bank_account import BankAccount, BankToken
from typing import List
import unittest

class TestCase:
    input: str
    expected: BankToken

    def __init__(self, input: str, expected: BankToken) -> None:
        self.input = input
        self.expected = expected

class BankAccountTest(unittest.TestCase):
    def test_anonymize(self):
        ba = BankAccount()

        cases: List[TestCase] = [
            TestCase("PL", BankToken("")),
            TestCase("123123123", BankToken("")),
            TestCase(
                "PL12345678901234567890123456",
                BankToken("PL"),
            ),
            TestCase(
                "PL12345678901234567890123456",
                BankToken("PL"),
            ),
            TestCase(
            "DE1234567890123456612322",
                BankToken("DE"),
            )
        ]

        for case in cases:
            got, ok = ba.anonymize(case.input)
            self.assertEqual(got, case.expected)

if __name__ == '__main__':
    unittest.main()