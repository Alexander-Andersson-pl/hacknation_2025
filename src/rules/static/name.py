import random
from typing import Tuple
import schwifty
from schwifty import exceptions
from src.rules import token
from enum import Enum
import morfeusz2

morf = morfeusz2.Morfeusz()
input = u"Rozmawiałem na giełdzie."


class NameType(Enum):
    Personal = 1
    Location = 3


class Name:
    def __init__(self, morfeusz: morfeusz2.Morfeusz):
        self.morfeusz = morfeusz
        pass

    @staticmethod
    def anonymize(word: str) -> Tuple[token.Token, bool]:
        analyzed = morf.analyse(word)
        for a in analyzed:
            if not a[2][2].startswith('subst'):
                continue

            if 'imie' in a[2][3] or 'nazwisko' in a[2][3]:
                return NameToken(NameType.Personal), True

            if 'nazwa_geograficzna' in a[2][3]:
                return NameToken(NameType.Location), True

        return NameToken(""), False


class NameToken(token.Token):
    def __init__(self, nameType: NameType):
        super().__init__(token.TokenType.Name)
        self.nameType = nameType

    def label(self):
        match self.nameType:
            case NameType.FirstName:
                return "{firstname}"
            case NameType.LastName:
                return "{lastname}"
            case NameType.Location:
                return "{location}"

    def generate(self) -> str:
        pass

    def __eq__(self, other):
        return self.nameType == other.nameType