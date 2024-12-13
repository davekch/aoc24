#!/usr/bin/env python

from pathlib import Path
import numpy as np
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


def almost_integer(x, eps=10e-15):
    return abs(x - round(x)) < abs(eps)


@watch.measure_time
def solve1(data):
    tokens = 0
    for (xa, ya), (xb, yb), (xp, yp) in data:
        # a, b = np.linalg.solve([[xa, xb], [ya, yb]], [xp, yp])
        # # print(a, b)
        # if not almost_integer(a) or not almost_integer(b): # or a > 100 or b > 100:
        #     continue
        # a, b = round(a), round(b)
        # if np.linalg.det([[xa, xb], [ya, yb]]) < 10e-15:
        #     mini = 10000000000000
        #     for z in range(-min(a, b), 101-max(a, b)):
        #         if (a + z) * 3 + b + z < mini:
        #             a = a + z
        #             b = b + z
        #             mini = a * 3 + b

        # assert a * xa + b * xb == xp
        # assert a * ya + b * yb == yp
        # tokens += a * 3 + b

        # just brute force
        mini = 10000000000000000000
        a = b = 0
        for aa in range(101):
            for bb in range(101):
                if aa * xa + bb * xb == xp and aa * ya + bb * yb == yp:
                    # print("ye")
                    if aa * 3 + bb < mini:
                        a = aa
                        b = bb
                        mini = a * 3 + b
        tokens += a * 3 + b

    return int(tokens)


@watch.measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

