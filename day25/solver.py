#!/usr/bin/env python

from pathlib import Path
import numpy as np
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    keys = []
    locks = []
    for block in raw_data.split("\n\n"):
        block = np.array([np.array(list(line)) for line in block.splitlines()])
        heights = np.sum(block.T == "#", axis=1) - 1
        if np.all(block[0] == "."):
            keys.append(heights)
        else:
            locks.append(heights)
    return keys, locks


@watch.measure_time
def solve1(data):
    keys, locks = data
    result = 0
    for key in keys:
        for lock in locks:
            if np.all(key + lock <= 5):
                result += 1
    return result


@watch.measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

