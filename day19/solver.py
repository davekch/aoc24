#!/usr/bin/env python

from pathlib import Path
from functools import cache
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    upper, lower = raw_data.split("\n\n")
    patterns = tuple([p.strip() for p in upper.split(",")])
    designs = lower.splitlines()
    return patterns, designs


@cache
def count_possibilities(design, patterns):
    if not design:
        return 0
    c = 0
    for pattern in patterns:
        if pattern == design:
            c += 1
        elif design.startswith(pattern):
            c += count_possibilities(design[len(pattern):], patterns)
    return c


@watch.measure_time
def solve1(data):
    patterns, designs = data
    s = 0
    for design in designs:
        if count_possibilities(design, patterns) > 0:
            s += 1
    return s


@watch.measure_time
def solve2(data):
    patterns, designs = data
    s = 0
    for design in designs:
        # no calculation takes place, all results are cached
        count = count_possibilities(design, patterns)
        s += count
    return s


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

