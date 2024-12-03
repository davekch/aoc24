#!/usr/bin/env python

from pathlib import Path
import re
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data


@watch.measure_time
def solve1(data):
    s = 0
    for a, b in re.findall(r"mul\((\d+),(\d+)\)", data):
        s += int(a) * int(b)
    return s


@watch.measure_time
def solve2(data):
    dos = data.split("do()")  # every item in dos started with do()
    to_do = [d.split("don't()")[0] for d in dos]  # remove everything after don't()
    s = 0
    for d in to_do:
        for a, b in re.findall(r"mul\((\d+),(\d+)\)", d):
            s += int(a) * int(b)
    return s


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

