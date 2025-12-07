from abc import ABC, abstractmethod
from typing import Tuple
from src.rules.token import Token


class StaticRule(ABC):
    @abstractmethod
    def anonymize(self, word: str) -> Tuple[Token, bool]:
        pass
