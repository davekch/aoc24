#!/usr/bin/env python

from pathlib import Path
from aoc import utils
from aoc.geometry import Vec, Direction
import time
from rich.console import Console

console = Console()
watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    grid = utils.str_to_grid_dict(raw_data)
    pos = Vec(*utils.key_of_value(grid, "^"))
    grid = {Vec(*k): v if v != "^" else "." for k, v in grid.items()}
    return pos, grid


DIRECTIONS = [Direction.N, Direction.E, Direction.S, Direction.W]
path = set()


@watch.measure_time
def solve1(data):
    global path
    pos, grid = data
    minx, maxx, miny, maxy = utils.corners(grid)
    facing = Direction.N
    while minx <= pos.x <= maxx and miny <= pos.y <= maxy:
        while grid.get(pos+facing, ".") != "#":
            path.add(pos)
            pos += facing
            if not (minx <= pos.x <= maxx and miny <= pos.y <= maxy):
                break
            # print(utils.dictgrid_to_str(grid | {s: "X" for s in seen} | {pos: "O"}, keybuilder=Vec))
            # time.sleep(0.01)
        facing = DIRECTIONS[(DIRECTIONS.index(facing) + 1) % 4]
    return len(path)


def check_loop(grid, pos, facing):
    seen = set()
    while (pos, facing) not in seen:
        seen.add((pos, facing))
        if facing == Direction.N:
            in_sight = [o for o in grid if o.x == pos.x and o.y < pos.y]
            obstacle = max(in_sight, key=lambda p: p.y, default=None)
        elif facing == Direction.E:
            in_sight = [o for o in grid if o.y == pos.y and o.x > pos.x]
            obstacle = min(in_sight, key=lambda p: p.x, default=None)
        elif facing == Direction.S:
            in_sight = [o for o in grid if o.x == pos.x and o.y > pos.y]
            obstacle = min(in_sight, key=lambda p: p.y, default=None)
        elif facing == Direction.W:
            in_sight = [o for o in grid if o.y == pos.y and o.x < pos.x]
            obstacle = max(in_sight, key=lambda p: p.x, default=None)
        if not obstacle:
            # we're going to leave the map
            return False
        pos = obstacle - facing
        facing = DIRECTIONS[(DIRECTIONS.index(facing) + 1) % 4]
    return True


@watch.measure_time
def solve2(data):
    global path
    pos, grid = data
    minx, maxx, miny, maxy = utils.corners(grid)
    # make grid sparse
    grid = {k: v for k, v in grid.items() if v != "."}
    obstacles = set()
    for x, y in path:
        if Vec(x, y) == pos or Vec(x, y) in grid:
            continue
        # put an obstacle at x, y
        ogrid = grid | {Vec(x, y): "#"}
        if check_loop(ogrid, pos, Direction.N):
            obstacles.add(Vec(x, y))
    # print(utils.dictgrid_to_str(grid | {o: "O" for o in obstacles}, empty=".", keybuilder=Vec))
    return len(obstacles)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

