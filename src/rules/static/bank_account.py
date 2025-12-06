import random
from typing import Tuple
import schwifty
from schwifty import exceptions
from src.rules import token


class BankAccount:
    def __init__(self):
        pass

    @staticmethod
    def anonymize(word: str) -> Tuple[token.Token, bool]:
        try:
            iban = schwifty.IBAN(word)
            if iban.validate():
                return BankToken(iban.country_code), True
        except (exceptions.InvalidLength, exceptions.InvalidCountryCode, exceptions.InvalidBankCode,
                exceptions.InvalidChecksumDigits):
            # Treat slightly invalid IBANs as sensitive information
            country_code = "PL"
            if len(word) > 2:
                country_code = word[:2]
            return BankToken(country_code), True
        except exceptions.SchwiftyException as X:
            return BankToken(""), False

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

    def __eq__(self, other):
        return self.countryCode == other.countryCode

    def __str__(self):
        return f"BankAccount({self.countryCode})"
