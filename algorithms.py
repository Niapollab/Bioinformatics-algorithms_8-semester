from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class FindResult:
    comp_count: int
    pos: int | None = None


class SubstringSearcher(ABC):
    @abstractmethod
    def find_substring(self, text: str, sub: str) -> FindResult:
        pass
