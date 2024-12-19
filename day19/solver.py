#!/usr/bin/env python

from pathlib import Path
from functools import cache
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    upper, lower = raw_data.split("\n\n")
    patterns = [p.strip() for p in upper.split(",")]
    designs = lower.splitlines()
    return patterns, designs


def possible(design, patterns):
    possibilities = [""]
    for c in design:
        # if we fully consumed a possible pattern, start over
        if "" in possibilities:
            while "" in possibilities:
                possibilities.remove("")
            possibilities += [p for p in patterns if p[0] == c]
        
        # print(f"{c}: {possibilities}")
        # consume one character of all possibilities
        possibilities = [p[1:] for p in possibilities if p[0] == c]
        if not possibilities:
            return False
    return "" in possibilities


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
        if possible(design, patterns):
            s += 1
            # print(f"possible: {design}")
    return s


@watch.measure_time
def solve2(data):
    patterns, designs = data
    patterns = tuple(patterns)
    s = 0
    for design in designs:
        # print(f"check {design}")
        count = count_possibilities(design, patterns)
        # print(count)
        s += count
    return s


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

