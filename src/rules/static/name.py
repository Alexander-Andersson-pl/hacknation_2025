from typing import List, Any
from src.rules import token
from enum import Enum
import morfeusz2

class NameType(Enum):
    Unknown = 0
    FirstName = 1
    LastName = 2
    Location = 4

    def __str__(self):
        match self:
            case NameType.Unknown:
                return "unknown"
            case NameType.FirstName:
                return "first_name"
            case NameType.LastName:
                return "last_name"
            case NameType.Location:
                return "location"


class Name:
    def __init__(self, morfeusz: morfeusz2.Morfeusz):
        self.morfeusz = morfeusz
        pass

    def anonymize(self, tokens: List[Any]) -> List[Any]:
        out = []
        for idx in range(len(tokens)):
            word = tokens[idx]

            if not isinstance(word, str):
                out.append(word)
                continue

            analyzed = self.morfeusz.analyse(word)
            results = []
            for a in analyzed:
                if not a[2][2].startswith('subst'):
                    continue

                if 'imię' in a[2][3] and NameType.FirstName not in results:
                    results.append(NameType.FirstName)

                if 'nazwisko' in a[2][3] and NameType.LastName not in results:
                    results.append(NameType.LastName)

                if 'nazwa_geograficzna' in a[2][3] and NameType.Location not in results:
                    results.append(NameType.Location)

            if len(results) == 0:
                out.append(word)
                continue

            out.append(NameToken(results))

        self.normalize_names(out)
        out = self.normalize_street(out)
        out = self.normalize_address(out)

        return out

    def normalize_names(self, tokens):
        for i in range(0, len(tokens) - 1):
            current = tokens[i]
            next = tokens[i + 1]

            if not isinstance(current, NameToken) or not isinstance(next, NameToken):
                continue

            if NameType.FirstName in current.nameTypes and NameType.LastName in next.nameTypes:
                current.nameTypes = [NameType.FirstName]
                next.nameTypes = [NameType.LastName]

    def normalize_street(self, tokens: List[Any]) -> List[Any]:
        normalized = []
        i = -1
        while i < len(tokens) - 1:
            i += 1
            current = tokens[i]
            if not isinstance(current, str):
                normalized.append(current)
                continue

            isStreet = False
            for a in self.morfeusz.analyse(current):
                if a[2][1] == 'ulica' or a[2][1] == 'aleja':
                    isStreet = True
                    break

            if not isStreet:
                normalized.append(current)
                continue

            # eat following names as they are part of street name
            while i < len(tokens) - 1 and isinstance(tokens[i+1], NameToken):
                i+=1
            normalized.append(AddressToken())

            # Check for number after street
            if i >= len(tokens) - 1:
                continue

            next = tokens[i + 1]
            if not isInteger(next):
                continue

            i+=1

        return normalized

    def normalize_address(self, tokens: List[Any]) -> List[Any]:
        normalized = []
        i = -1
        while i < len(tokens) - 1:
            i += 1
            current = tokens[i]
            if not isinstance(current, NameToken) or NameType.Location not in current.nameTypes:
                normalized.append(current)
                continue

            # check next
            if i >= len(tokens) - 2:
                normalized.append(current)
                continue

            next = tokens[i + 1]
            nexter = tokens[i+2] # :)
            if next in ["przy", "na", "niedaleko"] and isinstance(nexter, AddressToken):
                normalized.append(AddressToken())
                i+=2
                continue

            normalized.append(current)

        return normalized

class AddressToken(token.Token):
    def __init__(self):
        super().__init__(token.TokenType.Address)

    def __eq__(self, other):
        return isinstance(other, AddressToken)

    def label(self):
        return "[address]"

    def generate(self) -> str:
        pass


class NameToken(token.Token):
    def __init__(self, nameTypes: List[NameType]):
        super().__init__(token.TokenType.Name)
        self.nameTypes = nameTypes

    def label(self):
        return "[" + "|".join(map(str, self.nameTypes)) + "]"

    def generate(self) -> str:
        pass

    def __eq__(self, other):
        if isinstance(other, NameToken):
            return other.nameType == self.nameType

        return False


def isInteger(x):
    try:
        int(x)
        return True
    except ValueError:
        return False
