import unittest
from src.rules.static import name
from typing import List, Any
import morfeusz2


class TestCase:
    input: str
    expected: List[Any]

    def __init__(self, input: str, expected: List[Any]) -> None:
        self.input = input
        self.expected = expected


class TestName(unittest.TestCase):
    def test_name_anonymize(self):
        morf = morfeusz2.Morfeusz()
        ba = name.Name(morf)

        cases: List[TestCase] = [
            TestCase(
                "Karol",
                [name.NameToken(name.NameType.Personal)],
            ),
            TestCase(
                "Janem",
                [name.NameToken(name.NameType.Personal)]
            ),
            TestCase(
                "Janem Karolem",
                [name.NameToken(name.NameType.Personal)],
            ),
        ]

        for case in cases:
            tokens = case.input.split()
            got = ba.anonymize(tokens)
            self.assertEqual(got, case.expected)


if __name__ == '__main__':
    unittest.main()
