from abc import ABC, abstractmethod
from dataclasses import dataclass
from operator import eq, ne
from typing import Any, Callable, Sequence, Iterable


@dataclass
class FindResult:
    comp_count: int
    pos: int | None = None


class SubstringSearcher(ABC):
    @abstractmethod
    def enumerate_substrings(self, text: str, sub: str) -> Iterable[FindResult]:
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
    def enumerate_substrings(self, text: str, sub: str) -> Iterable[FindResult]:
        text_len, sub_len = len(text), len(sub)

        if not sub:
            for i in range(text_len):
                yield FindResult(0, i)
            return

        counter = Counter()

        def compare(index: int) -> int:
            i = 0

            while i < sub_len and i < text_len:
                if counter.do(ne, text[i + index], sub[i]):
                    return i

                i += 1

            return i

        i = 0

        while i < text_len - sub_len + 1:
            j = compare(i)

            if j >= sub_len:
                yield FindResult(counter.count, i)

            i += 1


class KnuthMorrisPrattSubstringSearcher(SubstringSearcher):
    def enumerate_substrings(self, text: str, sub: str) -> Iterable[FindResult]:
        text_len = len(text)
        sub_len = len(sub)

        if not sub:
            for i in range(text_len):
                yield FindResult(0, i)
            return

        prefix_arr, comp_count = KnuthMorrisPrattSubstringSearcher.calculate_prefix_arr(sub)
        counter = Counter(comp_count)

        def match(i: int, j: int) -> tuple[int, int]:
            while i < text_len and j < sub_len:
                if counter.do(ne, text[i], sub[j]):
                    return i, j

                i += 1
                j += 1

            return i, j

        i, j = 0, 0
        while i < text_len - sub_len + j + 1:
            i, j = match(i, j)

            if j >= sub_len:
                yield FindResult(counter.count, i - sub_len)

            if j == 0:
                i += 1
            else:
                j = prefix_arr[j - 1]

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
