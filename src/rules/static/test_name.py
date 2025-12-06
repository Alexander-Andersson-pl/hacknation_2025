import unittest

from src.rules.static import name
# from .name import Name, NameToken
from typing import List
import morfeusz2

class TestCase:
    input: str
    expected: name.NameToken

    def __init__(self, input: str, expected: name.NameToken) -> None:
        self.input = input
        self.expected = expected

class TestName(unittest.TestCase):
    def test_name_anonymize(self):
        morf = morfeusz2.Morfeusz()
        ba = name.Name(morf)

        cases: List[TestCase] = [
            TestCase(
                "Karol",
                name.NameToken(name.NameType.Personal),
            ),
            TestCase(
                "Janem",
                name.NameToken(name.NameType.Personal)
            ),
        ]

        for case in cases:
            got, ok = ba.anonymize(case.input)
            self.assertTrue(ok)
            self.assertEqual(got, case.expected)

if __name__ == '__main__':
    unittest.main()