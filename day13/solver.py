#!/usr/bin/env python

from pathlib import Path
from fractions import Fraction
from aoc import utils


watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    machines = []
    for block in raw_data.split("\n\n"):
        lines = block.splitlines()
        xa, ya = utils.ints(lines[0])
        xb, yb = utils.ints(lines[1])
        xp, yp = utils.ints(lines[2])
        machines.append(((xa, ya), (xb, yb), (xp, yp)))
    return machines


def solve(xa, ya, xb, yb, xp, yp):
    b = Fraction(yp - Fraction(xp * ya, xa), yb - Fraction(xb * ya, xa))
    if b.denominator != 1:
        return None, None
    a = Fraction(xp - b * xb, xa)
    if a.denominator != 1:
        return None, None
    return a.numerator, b.numerator


@watch.measure_time
def solve1(data):
    tokens = 0
    for (xa, ya), (xb, yb), (xp, yp) in data:
        a, b = solve(xa, ya, xb, yb, xp, yp)
        if a is None:
            continue
        tokens += a * 3 + b
    return tokens


@watch.measure_time
def solve2(data):
    tokens = 0
    offset = 10000000000000
    for (xa, ya), (xb, yb), (xp, yp) in data:
        a, b = solve(xa, ya, xb, yb, xp + offset, yp + offset)
        if a is None:
            continue
        tokens += a * 3 + b
    return tokens
    


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

