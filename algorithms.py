from abc import ABC, abstractmethod
from dataclasses import dataclass
from operator import ne
from typing import Any, Callable


@dataclass
class FindResult:
    comp_count: int
    pos: int | None = None


class SubstringSearcher(ABC):
    @abstractmethod
    def find_substring(self, text: str, sub: str) -> FindResult:
        pass


class Counter:
    _count: int

    def __init__(self, start_count: int = 0) -> None:
        self._count = start_count

    def do(self, callable: Callable[..., Any], *args: Any) -> Any:
        self._count += 1
        return callable(*args)

    @property
    def count(self) -> int:
        return self._count


class SimpleSubstringSearcher(SubstringSearcher):
    def find_substring(self, text: str, sub: str) -> FindResult:
        text_len, sub_len = len(text), len(sub)
        counter = Counter()

        def compare(index: int) -> int:
            i = 0

            while i < sub_len and i < text_len:
                if counter.do(ne, text[i + index], sub[i]):
                    return i

                i += 1

            return i

        i = 0

        while i < text_len:
            j = compare(i)

            if j >= sub_len:
                return FindResult(counter.count, i)

            i += 1

        return FindResult(counter.count, None)
