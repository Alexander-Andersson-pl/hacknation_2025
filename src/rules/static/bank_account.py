import random
from typing import List, Any
import schwifty
from schwifty import exceptions
from src.rules import token


class BankAccount:
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

            try:
                iban = schwifty.IBAN(tokens[idx])
                if iban.validate():
                    out.append(BankToken(iban.country_code))
            except (exceptions.InvalidLength, exceptions.InvalidCountryCode, exceptions.InvalidBankCode,
                    exceptions.InvalidChecksumDigits):
                # Treat slightly invalid IBANs as sensitive information
                country_code = "PL"
                if len(word) > 2:
                    country_code = word[:2]
                out.append(BankToken(country_code))
            except exceptions.SchwiftyException as X:
                out.append(word)
        return out

class BankToken(token.Token):
    def __init__(self, country_code: str):
        super().__init__(token.TokenType.BankAccount)
        self.countryCode = country_code

    def label(self):
        return "[bank_account]"

    def generate(self) -> str:
        randInt = random.randint(0, int(1e26))
        return self.countryCode + "{:026d}".format(randInt)

    def __eq__(self, other):
        if isinstance(other, BankToken):
            return self.countryCode == other.countryCode

        return False


    def __str__(self):
        return f"BankAccount({self.countryCode})"
