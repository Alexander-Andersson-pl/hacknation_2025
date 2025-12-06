from typing import List, Any
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
    def anonymize(tokens: List[Any]) -> List[Any]:
        out = []
        for idx in range(len(tokens)):
            word = tokens[idx]

            if not isinstance(word, str):
                out.append(word)
                continue

            analyzed = morf.analyse(word)
            handled = False
            for a in analyzed:
                if not a[2][2].startswith('subst'):
                    continue

                if 'imie' in a[2][3] or 'nazwisko' in a[2][3]:
                    handled = True
                    out.append(NameToken(NameType.Personal))

                if 'nazwa_geograficzna' in a[2][3]:
                    handled = True
                    out.append(NameToken(NameType.Location))

            if not handled:
                out.append(word)

        # Unify 2 neighbouring tokens
        filtered = []
        for o in out:
            if len(filtered) == 0:
                filtered.append(o)
                continue

            if o == filtered[-1]:
                continue

            filtered.append(o)

        return filtered

class NameToken(token.Token):
    def __init__(self, nameType: NameType):
        super().__init__(token.TokenType.Name)
        self.nameType = nameType

    def label(self):
        match self.nameType:
            case NameType.Personal:
                return "[personal_name]"
            case NameType.Location:
                return "[location_name]"


    def generate(self) -> str:
        pass

    def __eq__(self, other):
        if isinstance(other, NameToken):
            return other.nameType == self.nameType

        return False