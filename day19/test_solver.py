import pytest
from solver import parse, solve1, solve2

TESTDATA = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
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
    assert solution == 6


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    assert solution == 16
