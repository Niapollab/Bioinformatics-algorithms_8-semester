from abc import ABC, abstractmethod
from dataclasses import dataclass
from operator import eq, ne
from typing import Any, Callable, Sequence, Iterable


@dataclass(frozen=True, eq=True)
class FindResult:
    comp_count: int
    pos: int | None = None


class SubstringSearcher(ABC):
    @abstractmethod
    def enumerate_substrings(self, text: str, sub: str) -> Iterable[FindResult]:
        pass


class EditorialDistanceCalculator(ABC):
    @abstractmethod
    def get_editorial_distance(self, first: str, second: str) -> int:
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
    _disable_count_in_prefix_array: bool

    def __init__(self, disable_count_in_prefix_array: bool = True) -> None:
        self._disable_count_in_prefix_array = disable_count_in_prefix_array

    def enumerate_substrings(self, text: str, sub: str) -> Iterable[FindResult]:
        text_len = len(text)
        sub_len = len(sub)

        if not sub:
            for i in range(text_len):
                yield FindResult(0, i)
            return

        prefix_arr, comp_count = KnuthMorrisPrattSubstringSearcher.calculate_prefix_arr(sub)
        counter = Counter(0 if self._disable_count_in_prefix_array else comp_count)

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


class WagnerFischerEditorialDistanceCalculator(EditorialDistanceCalculator):
    def get_editorial_distance(self, first: str, second: str) -> int:
        first_len = len(first) + 1
        second_len = len(second) + 1

        distance_matrix = [[0] * second_len for _ in range(first_len)]

        for i in range(first_len):
            distance_matrix[i][0] = i

        for j in range(second_len):
            distance_matrix[0][j] = j

        for j in range(1, second_len):
            for i in range(1, first_len):
                distance_matrix[i][j] = distance_matrix[i - 1][j - 1] \
                    if first[i - 1] == second[j - 1] \
                    else min(distance_matrix[i - 1][j] + 1, distance_matrix[i][j - 1] + 1, distance_matrix[i - 1][j - 1] + 1)

        return distance_matrix[first_len - 1][second_len - 1]
