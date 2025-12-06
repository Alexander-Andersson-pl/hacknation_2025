import re
import random
from typing import Tuple
from rules import token

EMAIL_REGEX = re.compile(
    r"(?P<email>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
    flags=re.IGNORECASE,
)


class Email:
    @staticmethod
    def anonymize(word: str) -> Tuple[token.Token, bool]:
        match = re.search(EMAIL_REGEX, word)
        if match:
            return EmailToken(), True
        return EmailToken(), False


class EmailToken(token.Token):
    def __init__(self):
        super().__init__(token.TokenType.Email)

    def label(self):
        return "{email}"

    def generate(self) -> str:
        prefix = "user" + str(random.randint(1000, 9999))
        domain = "example.com"
        return f"{prefix}@{domain}"
