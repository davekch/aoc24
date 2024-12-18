import pytest
from solver import parse, solve1, solve2

TESTDATA = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    # asserts go here


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data, size=6, steps=12)
    assert solution == 22


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data, size=6, steps=12)
    assert solution == "6,1"
