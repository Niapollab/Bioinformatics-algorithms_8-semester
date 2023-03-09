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


class SimpleSubstringSearcher(SubstringSearcher):
    def find_substring(self, text: str, sub: str) -> FindResult:
        def compare(index: int, text_len: int, sub_len: int) -> int:
            i = 0

            while i < sub_len and i < text_len:
                if text[i + index] != sub[i]:
                    return i

                i += 1

            return i

        i, comp_count = 0, 0
        text_len, sub_len = len(text), len(sub)

        while i < text_len:
            j = compare(i, text_len, sub_len)
            comp_count += j + 1

            if j >= sub_len:
                return FindResult(comp_count - 1, i)

            i += 1

        return FindResult(comp_count, None)
