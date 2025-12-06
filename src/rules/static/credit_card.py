import random
import re
from typing import List, Any
from src.rules import token

CCNUMBER_REGEX = r"\d{13,19}"


class CreditCard:
    def __init__(self):
        pass

    @staticmethod
    def anonymize(tokens: List[Any]) -> List[Any]:
        out = []
        for idx in range(len(tokens)):
            word = tokens[idx]

            if not isinstance(word, str):
                out.append(word)
                continue


            match = re.search(CCNUMBER_REGEX, word)
            if match:
                out.append(CreditCardToken())

        return out

class CreditCardToken(token.Token):
    def __init__(self):
        super().__init__(token.TokenType.CreditCard)

    def label(self):
        return "[cc_number]"

    def generate(self) -> str:
        randInt = random.randint(0, int(1e16))
        return self.countryCode + "{:016d}".format(randInt)

    def __eq__(self, other):
        if isinstance(other, CreditCardToken):
            return other.label() == self.label()

        return False

    def __str__(self):
        return self.label()
