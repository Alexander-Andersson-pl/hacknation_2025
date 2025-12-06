import random
from typing import Tuple
from rules import token
import re

IBAN_REGEX = r'([a-zA-Z]{2})\d{26}'


class BankAccount:
    def __init__(self):
        pass

    @staticmethod
    def anonymize(word: str) -> Tuple[token.Token, bool]:
        match = re.search(IBAN_REGEX, word)
        if match:
            return BankToken(match.group(1)), True

        return BankToken(""), False


class BankToken(token.Token):
    def __init__(self, country_code: str):
        super().__init__(token.TokenType.BankAccount)
        self.countryCode = country_code

    def label(self):
        return "{bank_account}"

    def generate(self) -> str:
        randInt = random.randint(0, int(1e26))
        return self.countryCode + "{:026d}".format(randInt)
