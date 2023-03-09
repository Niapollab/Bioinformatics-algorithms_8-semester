import pytest
from algorithms import SubstringSearcher
from itertools import product


SUBSTRING_SEARCHERS = [
]


CASES = [
    ('', '', None),
    ('1234', '', 0),
    ('', '1234', None),
    ('1234', '1234', 0),
    ('1234', '1235', None),
    ('ab', 'abc', None),
    ('abab', 'ab', 0),
    ('ab__ab', 'ab', 0),
    ('ac__ab', 'ab', 4)
]


@pytest.mark.parametrize("searcher,text,sub,expected_pos", [pytest.param(p[0], *p[1]) for p in product(SUBSTRING_SEARCHERS, CASES)])
def test_substring_find(searcher: SubstringSearcher, text: str, sub: str, expected_pos: int | None) -> None:
    assert searcher.find_substring(text, sub).pos == expected_pos
