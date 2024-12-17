import pytest
from solver import parse, solve1, solve2

TESTDATA = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
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
    assert solution == "4,6,3,5,6,3,5,2,1,0"


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 117440
