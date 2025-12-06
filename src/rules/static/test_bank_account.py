from bank_account import BankAccount
from typing import List

class TestCase:
    input: str
    expected: str

    def __init__(self, input: str, expected: str) -> None:
        self.input = input
        self.expected = expected

def test_bank_account_anonymize():
    ba = BankAccount()

    cases: List[TestCase] = [
        TestCase(
            "This is my bank account: PL12345678901234567890123456",
            "This is my bank account: {bank_account}"
        ),
        TestCase(
            "PL12345678901234567890123456",
            "{bank_account}"
        ),
        TestCase(
        "DE12345678901234566",
            "{bank_account}"
        )
    ]

    for case in cases:
        got = ba.anonymize(case.input)
        assert got == case.expected