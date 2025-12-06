import re
from typing import List, Tuple

# Matches common email formats; avoids matching trailing punctuation.
EMAIL_REGEX = re.compile(
    r"(?P<email>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})",
    flags=re.IGNORECASE,
)

TOKEN = "{email}"


def anonymize(text: str) -> Tuple[str, List[str]]:
    """
    Replace email addresses with a placeholder token.

    Returns the anonymized text and a list of matched emails (for optional logging).
    """
    matches: List[str] = []

    def _sub(match: re.Match) -> str:
        email = match.group("email")
        matches.append(email)
        return TOKEN

    new_text = EMAIL_REGEX.sub(_sub, text)
    return new_text, matches
