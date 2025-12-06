import re
import random
from typing import List, Any
from rules import token

EMAIL_REGEX = re.compile(
    r"(?P<email>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
    flags=re.IGNORECASE,
)


class Email:
    @staticmethod
    def anonymize(tokens: List[Any]) -> List[Any]:
        out = []
        for idx in range(len(tokens)):
            word = tokens[idx]

            if not isinstance(word, str):
                out.append(word)
                continue

            match = re.search(EMAIL_REGEX, word)
            if not match:
                out.append(word)

            out.append(EmailToken())

        return out

class EmailToken(token.Token):
    def __init__(self):
        super().__init__(token.TokenType.Email)

    def label(self):
        return "[email]"

    def generate(self) -> str:
        prefix = "user" + str(random.randint(1000, 9999))
        domain = "example.com"
        return f"{prefix}@{domain}"

    def __eq__(self, other):
        return isinstance(other, EmailToken)