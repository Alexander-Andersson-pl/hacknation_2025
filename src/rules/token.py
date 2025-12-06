from enum import Enum
from abc import ABC, abstractmethod


class TokenType(Enum):
    Unmatched = 0
    Email = 1
    BankAccount = 2
    CreditCard = 3
    Pesel = 4


class Token(ABC):
    def __init__(self, type: TokenType):
        self.type = type
        pass

    @abstractmethod
    def label(self):
        pass

    @abstractmethod
    def generate(self) -> str:
        pass
