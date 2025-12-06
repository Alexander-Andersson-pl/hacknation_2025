import phonenumbers
from typing import Tuple
from rules import token


DEFAULT_REGION = "PL"


class Phone:
    @staticmethod
    def anonymize(text: str) -> Tuple[token.Token, bool]:
        for match in phonenumbers.PhoneNumberMatcher(text, DEFAULT_REGION):
            num_obj = match.number
            if phonenumbers.is_valid_number(num_obj):
                return PhoneToken(), True

        return PhoneToken(), False


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
