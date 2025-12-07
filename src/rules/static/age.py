from typing import List, Any
from rules import token
import morfeusz2
import random


class Age:
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
            isAgeCounter = False
            for a in analyzed:
                if 'rok' in a[2][1] or 'miesiąc' in a[2][1]:
                    isAgeCounter = True
                    break

            if not isAgeCounter or idx < 2:
                out.append(word)
                continue

            if not isinstance(tokens[idx - 1], str) or not isinstance(tokens[idx -2], str) or not isInteger(tokens[idx - 1]):
                out.append(word)
                continue


            analyzed = self.morfeusz.analyse(tokens[idx - 2])
            isHave = False
            for a in analyzed:
                if 'mieć' in a[2]:
                    isHave = True
                    break

            if not isHave:
                out.append(word)
                continue

            # last 3 elements are 'have' + 'number' + 'ageCounterNoun'
            out.pop()
            out.append(AgeToken())

        return out


class AgeToken(token.Token):
    def __init__(self):
        super().__init__(token.TokenType.Age)

    def __eq__(self, other):
        return isinstance(other, AgeToken)

    def label(self):
        return "[age]"

    def generate(self) -> str:
        count = random.randint(20, 30)
        if count % 10 > 1 and count % 10 < 5:
            return str(count)+" lata"
        return str(count)+" lat"


def isInteger(x):
    try:
        int(x)
        return True
    except ValueError:
        return False
