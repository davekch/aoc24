#!/usr/bin/env python

from pathlib import Path
from collections import defaultdict
from itertools import combinations
from aoc import utils
from aoc.geometry import Vec

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    grid = utils.str_to_grid_dict(raw_data)
    _, maxx, _, maxy = utils.corners(grid)
    antennas = defaultdict(list)
    for p, a in grid.items():
        if a != ".":
            antennas[a].append(Vec(*p))
    return antennas, (maxx, maxy)


def find_andtinodes(positions: list[Vec]) -> set[Vec]:
    antinodes = set()
    for p1, p2 in combinations(positions, 2):
        # the two points outside always exist
        delta = p1 - p2
        antinodes.add(p1 + delta)
        antinodes.add(p2 - delta)
        # # check if there are also points in between the antennas
        # # this is the case if there is a point at 1/3 of the
        # # distance between the antennas
        # # CURIOUS: this apparently never happens
        # if all((x/3).is_integer() for x in delta):
        #     delta3 = Vec(*[x//3 for x in delta])
        #     antinodes.add(p1 - delta)
        #     antinodes.add(p1 - 2 * delta)
    return antinodes


@watch.measure_time
def solve1(data):
    antennas, (maxx, maxy) = data
    antinodes = set()
    for positions in antennas.values():
        antinodes |= find_andtinodes(positions)
    
    # print(utils.dictgrid_to_str(
    #     {Vec(x, y): "." for x in range(maxx) for y in range(maxy)}
    #     | {p: a for a, points in antennas.items() for p in points}
    #     | {n: "#" for n in antinodes},
    #     keybuilder=Vec
    # ))

    return len({p for p in antinodes if 0 <= p.x <= maxx and 0 <= p.y <= maxy})


def in_bounds(point, maxx, maxy):
    return 0 <= point.x <= maxx and 0 <= point.y <= maxy


def find_andtinodes_p2(positions: list[Vec], bounds: tuple[int, int]) -> set[Vec]:
    antinodes = set()
    maxx, maxy = bounds
    for p1, p2 in combinations(positions, 2):
        delta = p1 - p2
        k = 0
        while in_bounds(a1 := p1 + k * delta, maxx, maxy):
            antinodes.add(a1)
            k += 1
        k = 0
        while in_bounds(a2 := p2 - k * delta, maxx, maxy):
            antinodes.add(a2)
            k += 1
    return antinodes


@watch.measure_time
def solve2(data):
    antennas, bounds = data
    antinodes = set()
    for positions in antennas.values():
        antinodes |= find_andtinodes_p2(positions, bounds)

    return len({p for p in antinodes if in_bounds(p, *bounds)})


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

