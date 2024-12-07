#!/usr/bin/env python

from pathlib import Path
from aoc import utils
from operator import add, mul

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    equations = []
    for line in raw_data.splitlines():
        nums = utils.ints(line)
        equations.append((nums[0], nums[1:]))
    return equations


def check(test, nums, operators):
    def _check(test, nums, acc):
        if not nums:
            return test == acc
        if acc > test:
            return False
        return any(_check(test, nums[1:], op(acc, nums[0])) for op in operators)

    return _check(test, nums[1:], nums[0])


@watch.measure_time
def solve1(data):
    s = 0
    for test, nums in data:
        if check(test, nums, [add, mul]):
            s += test
    return s


def combine_digits(a, b):
    return int(str(a) + str(b))


@watch.measure_time
def solve2(data):
    s = 0
    for test, nums in data:
        if check(test, nums, [add, mul, combine_digits]):
            s += test
    return s


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

