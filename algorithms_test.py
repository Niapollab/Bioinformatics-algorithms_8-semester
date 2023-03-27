import pytest
from algorithms import WagnerFischerEditorialDistanceCalculator, EditorialDistanceCalculator, SubstringSearcher, SimpleSubstringSearcher, KnuthMorrisPrattSubstringSearcher
from itertools import product


SUBSTRING_SEARCHERS = [
    SimpleSubstringSearcher(),
    KnuthMorrisPrattSubstringSearcher()
]


EDITORIAL_DISTANCE_CALCULATORS = [
    WagnerFischerEditorialDistanceCalculator()
]


SUBSTRING_SEARCHER_CASES = [
    ('', '', []),
    ('1234', '', [0, 1, 2, 3]),
    ('', '1234', []),
    ('1234', '1234', [0]),
    ('1234', '1235', []),
    ('ab', 'abc', []),
    ('abab', 'ab', [0, 2]),
    ('ab__ab', 'ab', [0, 4]),
    ('ac__ab', 'ab', [4]),
    ('abcdabca', 'abca', [4]),
    ('aabaabbaab', 'abba', [4])
]


EDITORIAL_DISTANCE_CASES = [
    ('', '', 0),
    ('1234', '', 4),
    ('', '1234', 4),
    ('1234', '1234', 0),
    ('1234', '1235', 1),
    ('ab', 'abc', 1),
    ('abab', 'ab', 2),
    ('ab__ab', 'ab', 4),
    ('ac__ab', 'ab', 4),
    ('abcdabca', 'abca', 4),
    ('aabaabbaab', 'abba', 6)
]


@pytest.mark.parametrize("searcher,text,sub,expected_pos", [pytest.param(p[0], *p[1]) for p in product(SUBSTRING_SEARCHERS, SUBSTRING_SEARCHER_CASES)])
def test_substring_find(searcher: SubstringSearcher, text: str, sub: str, expected_pos: int | None) -> None:
    assert [r.pos for r in searcher.enumerate_substrings(text, sub)] == expected_pos


@pytest.mark.parametrize("calculator,first,second,expected_distance", [pytest.param(p[0], *p[1]) for p in product(EDITORIAL_DISTANCE_CALCULATORS, EDITORIAL_DISTANCE_CASES)])
def test_distance_calculator(calculator: EditorialDistanceCalculator, first: str, second: str, expected_distance: int) -> None:
    assert calculator.get_editorial_distance(first, second) == expected_distance
