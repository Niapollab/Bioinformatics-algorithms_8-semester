from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Sequence
from operator import eq, ne


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


class KnuthMorrisPrattSubstringSearcher(SubstringSearcher):
    def find_substring(self, text: str, sub: str) -> FindResult:
        N = len(text)
        M = len(sub)

        PREFIX_ARR, COMP_COUNT = KnuthMorrisPrattSubstringSearcher.calculate_prefix_arr(sub)
        COUNTER = Counter(COMP_COUNT)

        def match(i: int, j: int) -> tuple[int, int]:
            while i < N and j < M:
                if COUNTER.do(ne, text[i], sub[j]):
                    return i, j

                i += 1
                j += 1

            return i, j

        i, j = 0, 0
        while i < N:
            i, j = match(i, j)

            if j >= M:
                return FindResult(COUNTER.count, i - M)

            if j == 0:
                i += 1
            else:
                j = PREFIX_ARR[j - 1]

        return FindResult(COUNTER.count, None)

    @staticmethod
    def calculate_prefix_arr(sub: str) -> tuple[Sequence[int], int]:
        sub_len = len(sub)
        prefix_arr = [0] * sub_len
        counter = Counter()

        i, j = 1, 0
        while i < sub_len:
            while not (equals := counter.do(eq, sub[i], sub[j])) and (j > 0):
                j = prefix_arr[j - 1]

            if equals:
                j += 1
                prefix_arr[i] = j

            i += 1

        return prefix_arr, counter.count
