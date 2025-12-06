from typing import Tuple

from pesel import Pesel
from src.rules import token


class PeselRule:
    @staticmethod
    def anonymize(word: str) -> Tuple[token.Token, bool]:
        if len(word) != 11 or not word.isdigit():
            return PeselToken(), False

        try:
            _ = Pesel(word)
        except Exception:
            return PeselToken(), False

        return PeselToken(), True


class PeselToken(token.Token):
    def __init__(self):
        super().__init__(token.TokenType.Pesel)

    def label(self) -> str:
        return "{pesel}"

    def generate(self) -> str:
        return Pesel.generate()
