import pytest
from solver import parse, solve1, solve2

TESTDATA = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
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
    assert solution == 36


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 81
