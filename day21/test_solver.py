import pytest
from solver import parse, solve1, solve2

TESTDATA = """029A
980A
179A
456A
379A
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
    assert solution == 126384


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    # asserts go here
