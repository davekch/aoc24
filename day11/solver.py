#!/usr/bin/env python

from pathlib import Path
from functools import cache
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return utils.ints(raw_data.strip())


@cache
def apply_n(number: int, n: int) -> int:
    """calculate into how many numbers `number` turns after `n` steps"""
    if n == 0:
        return 1
    if number == 0:
        return apply_n(1, n-1)
    elif (l := len(sn := str(number))) % 2 == 0:
        return apply_n(int(sn[:l//2]), n-1) + apply_n(int(sn[l//2:]), n-1)
    else:
        return apply_n(number * 2024, n-1)


@watch.measure_time
def solve1(data):
    s = 0
    for number in data:
        s += apply_n(number, 25)
    return s


@watch.measure_time
def solve2(data):
    s = 0
    for number in data:
        # print(number)
        s += apply_n(number, 75)
    return s


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()
