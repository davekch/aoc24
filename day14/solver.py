#!/usr/bin/env python

from pathlib import Path
from collections import Counter
import math
from scipy.stats import kstest, uniform
from aoc import utils
from aoc.geometry import Vec

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    robots = []
    for line in raw_data.splitlines():
        x, y, vx, vy = utils.ints(line)
        robots.append((Vec(x, y), Vec(vx, vy)))
    return robots


def count_quadrants(positions: Counter, w: int, h: int):
    up = h // 2  # where upper half ends
    lo = h // 2 + (h % 2)  # where lower half starts
    le = w // 2  # where left half ends
    ri = w // 2 + (w % 2)  # where right half starts
    # print(up, lo, le, ri)
    uple = sum(c for p, c in positions.items() if 0 <= p[0] < le and 0 <= p[1] < up)
    upri = sum(c for p, c in positions.items() if ri <= p[0] <= w and 0 <= p[1] < up)
    lole = sum(c for p, c in positions.items() if 0 <= p[0] < le and lo <= p[1] <= h)
    lori = sum(c for p, c in positions.items() if ri <= p[0] <= w and lo <= p[1] <= h)
    return uple, upri, lole, lori



@watch.measure_time
def solve1(data, w=101, h=103):
    new_positions = Counter()
    for pos, vel in data:
        new_pos = pos + 100 * vel
        wrapped = (new_pos.x % w, new_pos.y % h)
        new_positions[wrapped] += 1
    # print(utils.dictgrid_to_str(new_positions, empty="."))
    quadrants = count_quadrants(new_positions, w, h)
    # print(quadrants)
    return math.prod(quadrants)


@watch.measure_time
def solve2(data, w=101, h=103):
    robots = data
    t = 0
    px = py = 1
    expect_x_uniform = uniform(loc=0, scale=w).cdf
    expect_y_uniform = uniform(loc=0, scale=h).cdf
    while px > 1e-40 or py > 1e-40:
        t += 1
        new_robots = []
        for pos, vel in robots:
            new_pos = pos + vel
            wrapped = Vec(new_pos.x % w, new_pos.y % h)
            new_robots.append((wrapped, vel))
        robots = new_robots
        x_normal = kstest([p.x for p,_ in robots], expect_x_uniform)
        y_normal = kstest([p.y for p,_ in robots], expect_y_uniform)
        px = x_normal.pvalue
        py = y_normal.pvalue
    # print(x_normal.pvalue, y_normal.pvalue)
    # print(t)
    print(
        utils.dictgrid_to_str(
            Counter([p for p,_ in robots]),
            # empty=".",
            keybuilder=Vec
        )
    )
    return t


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

