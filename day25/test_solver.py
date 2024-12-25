import pytest
import numpy as np
from solver import parse, solve1, solve2

TESTDATA = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""

@pytest.fixture
def parsed_data():
    return parse(TESTDATA)


def test_parse():
    data = parse(TESTDATA)
    keys, locks = data
    print(keys)
    print(locks)
    expected_keys = [
        np.array([5,0,2,1,3]),
        np.array([4,3,4,0,2]),
        np.array([3,0,2,0,1]),
    ]
    assert np.all([np.all(key == expected) for key, expected in zip(keys, expected_keys)])
    expected_locks = [
        np.array([0,5,3,4,3]),
        np.array([1,2,0,5,3]),
    ]
    assert np.all([np.all(lock == expected) for lock, expected in zip(locks, expected_locks)])


# PART 1
def test_solve1(parsed_data):
    solution = solve1(parsed_data)
    assert solution == 3


# PART 2
def test_solve2(parsed_data):
    solution = solve2(parsed_data)
    # asserts go here
