from typing import List, Any

from pesel import Pesel
from src.rules import token


class PeselRule:
    @staticmethod
    def anonymize(tokens: List[Any]) -> List[Any]:
        out = []
        for idx in range(len(tokens)):
            word = tokens[idx]

            if not isinstance(word, str) or len(word) != 11 or not word.isdigit():
                out.append(word)
                continue

            out.append(PeselToken())

        return out

class PeselToken(token.Token):
    def __init__(self):
        super().__init__(token.TokenType.Pesel)

    def label(self) -> str:
        return "[pesel]"

    def generate(self) -> str:
        return Pesel.generate()

    def __eq__(self, other) -> bool:
        return isinstance(other, PeselToken)

