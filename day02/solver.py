#!/usr/bin/env python

from pathlib import Path
import numpy as np
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    levels = []
    for line in raw_data.splitlines():
        levels.append(np.array(utils.ints(line)))
    return levels


def safe(level: np.array) -> bool:
    diffs = np.diff(level)
    if np.all(np.abs(diffs) > 0) and np.all(np.abs(diffs) < 4):
        if np.all(diffs > 0) or np.all(diffs < 0):
            return True
    return False


@watch.measure_time
def solve1(data):
    c = 0
    for level in data:
        if safe(level):
            c += 1
    return c


def dampen(level):
    for i in range(len(level)):
        yield np.concatenate((level[:i], level[i+1:]))


@watch.measure_time
def solve2(data):
    c = 0
    for level in data:
        for mlevel in dampen(level):
            if safe(mlevel):
                c += 1
                break
    return c



if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

