from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable, Iterable


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
