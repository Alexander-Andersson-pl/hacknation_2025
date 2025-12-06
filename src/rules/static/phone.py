import phonenumbers
from typing import List, Any
from rules import token

DEFAULT_REGION = "PL"


class Phone:
    @staticmethod
    def anonymize(tokens: List[Any]) -> List[Any]:
        out = []
        for idx in range(len(tokens)):
            word = tokens[idx]

            if not isinstance(word, str):
                out.append(word)
                continue

            matched = False
            for match in phonenumbers.PhoneNumberMatcher(word, DEFAULT_REGION):
                num_obj = match.number
                if phonenumbers.is_valid_number(num_obj):
                    out.append(PhoneToken())
                    matched = True
                    break
            if not matched:
                out.append(word)

        return out


class PhoneToken(token.Token):
    def __init__(self):
        super().__init__(token.TokenType.Phone)

    def label(self) -> str:
        return "{phone}"

    def generate(self) -> str:
        import random

        first = random.choice("456789")
        rest = "".join(str(random.randint(0, 9)) for _ in range(8))
        return first + rest

    def __eq__(self, other):
        return isinstance(other, PhoneToken)
