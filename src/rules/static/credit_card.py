import random
import re
from typing import Tuple
from rules import token

CCNUMBER_REGEX = r"\d{13,19}"


class CreditCard:
    def __init__(self):
        pass

    @staticmethod
    def anonymize(word: str) -> Tuple[token.Token, bool]:
        match = re.search(CCNUMBER_REGEX, word)
        if match:
            return token.Token(match.group(0)), True
        return token.Token(word), False

class CreditCardToken(token.Token):
    def __init__(self):
        super().__init__(token.TokenType.CreditCard)

    def label(self):
        return "{cc_number}"

    def generate(self) -> str:
        randInt = random.randint(0, int(1e16))
        return self.countryCode + "{:016d}".format(randInt)
