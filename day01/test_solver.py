import pytest
from solver import parse, solve1, solve2

TESTDATA = """3   4
4   3
2   5
1   3
3   9
3   3
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 11


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 31
