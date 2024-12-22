#!/usr/bin/env python

from pathlib import Path
import math
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return list(map(int, raw_data.splitlines()))


def next_secret(secret: int) -> int:
    # first step
    next_secret = (secret * 64) ^ secret
    next_secret = next_secret % 16777216
    # second step
    next_secret = math.floor(next_secret / 32) ^ next_secret
    next_secret = next_secret % 16777216
    # third step
    next_secret = (next_secret * 2048) ^ next_secret
    return next_secret % 16777216


@watch.measure_time
def solve1(data):
    s = 0
    for num in data:
        for _ in range(2000):
            num = next_secret(num)
        s += num
    return s


@watch.measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

