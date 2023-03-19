import pytest
from algorithms import SubstringSearcher, SimpleSubstringSearcher, KnuthMorrisPrattSubstringSearcher
from itertools import product


SUBSTRING_SEARCHERS = [
    SimpleSubstringSearcher(),
    KnuthMorrisPrattSubstringSearcher()
]


CASES = [
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


@pytest.mark.parametrize("searcher,text,sub,expected_pos", [pytest.param(p[0], *p[1]) for p in product(SUBSTRING_SEARCHERS, CASES)])
def test_substring_find(searcher: SubstringSearcher, text: str, sub: str, expected_pos: int | None) -> None:
    assert [r.pos for r in searcher.enumerate_substrings(text, sub)] == expected_pos
