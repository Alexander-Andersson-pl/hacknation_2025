from typing import List, Any
from src.rules import token
from enum import Enum
import morfeusz2

morf = morfeusz2.Morfeusz()
input = u"Rozmawiałem na giełdzie."


class NameType(Enum):
    Unknown = 0
    FirstName = 1
    LastName = 2
    BothNames = 3
    Location = 4


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
            result = NameType.Unknown
            for a in analyzed:
                if not a[2][2].startswith('subst'):
                    continue

                if 'imię' in a[2][3]:
                    if result == NameType.LastName or result == NameType.BothNames :
                        result = NameType.BothNames
                        continue
                    result = NameType.FirstName
                    continue

                if 'nazwisko' in a[2][3]:
                    if result == NameType.FirstName or result == NameType.BothNames :
                        result = NameType.BothNames
                        continue
                    result = NameType.LastName
                    continue

                if 'nazwa_geograficzna' in a[2][3]:
                    result = NameType.Location

            if result == NameType.Unknown:
                out.append(word)
                continue

            out.append(NameToken(result))

        # Unify 2 neighbouring tokens
        filtered = []
        for o in out:
            if len(filtered) == 0:
                filtered.append(o)
                continue

            if isinstance(o, NameToken) and isinstance(filtered[-1], NameToken):
                if o.nameType == NameType.Location or filtered[-1].nameType == NameType.Location:
                    filtered.append(o)
                    continue

                if filtered[-1].nameType == NameType.BothNames:
                    filtered[-1].nameType = NameType.FirstName
                    continue

            filtered.append(o)

        # Check last element
        if len(filtered) == 0:
            return []

        if len(filtered) == 1 and isinstance(filtered[-1], NameToken):
            if filtered[-1].nameType == NameType.BothNames:
                filtered[-1].nameType = NameType.FirstName
            return filtered

        if isinstance(filtered[-1], NameToken) and isinstance(filtered[-2], NameToken) and filtered[-1].nameType == NameType.BothNames:
            if filtered[-2].nameType == NameType.FirstName:
                filtered[-1].nameType = NameType.LastName
            else:
                filtered[-1].nameType = NameType.FirstName

        return filtered




class NameToken(token.Token):
    def __init__(self, nameType: NameType):
        super().__init__(token.TokenType.Name)
        self.nameType = nameType

    def label(self):
        match self.nameType:
            case NameType.FirstName:
                return "[first_name]"
            case NameType.LastName:
                return "[last_name]"
            case NameType.BothNames:
                return "[name]"
            case NameType.Location:
                return "[location_name]"

    def generate(self) -> str:
        pass

    def __eq__(self, other):
        if isinstance(other, NameToken):
            return other.nameType == self.nameType

        return False
