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
            "This is my cc: 123123123123",
            "This is my cc: {cc_number}"
        ),
    ]

    for case in cases:
        got = ba.anonymize(case.input)
        assert got == case.expected