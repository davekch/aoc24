#!/usr/bin/env python

from pathlib import Path
from aoc import utils
from aoc.geometry import Vec, Direction

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return {Vec(*p): c for p, c in utils.str_to_grid_dict(raw_data).items()}


def count_xmas(grid, index):
    if grid[index] not in "XS":
        return 0
    words_in_directions = {
        Direction.E: grid[index],
        Direction.SE: grid[index],
        Direction.S: grid[index],
        Direction.SW: grid[index],
    }
    for k in range(1, 4):
        for dir in words_in_directions:
            words_in_directions[dir] += grid.get(index + k * dir, "")
    wordsl = list(words_in_directions.values())
    return wordsl.count("XMAS") + wordsl.count("SAMX")


@watch.measure_time
def solve1(data):
    s = 0
    for p in data:
        s += count_xmas(data, p)
    return s


def check_xmas(grid, index):
    if grid[index] != "A":
        return False
    diag1 = grid.get(index + Direction.SW, "") + "A" + grid.get(index + Direction.NE, "")
    if diag1 not in ["MAS", "SAM"]:
        return False
    diag2 = grid.get(index + Direction.NW, "") + "A" + grid.get(index + Direction.SE, "")
    if diag2 not in ["MAS", "SAM"]:
        return False
    return True


@watch.measure_time
def solve2(data):
    s = 0
    for p in data:
        if check_xmas(data, p):
            s += 1
    return s


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

