import pytest
from solver import parse, solve1, solve2

TESTDATA = """2333133121414131402
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
    assert solution == 1928


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 2858
