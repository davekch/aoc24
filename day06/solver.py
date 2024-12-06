#!/usr/bin/env python

from pathlib import Path
from aoc import utils
from aoc.geometry import Vec, Direction
import time
from rich.console import Console
from copy import deepcopy, copy
from tqdm import tqdm

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


def next_position(grid, pos, direction):
    next_direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]
    if next_direction == Direction.N:
        in_sight = [o for o in grid if o.x == pos.x and o.y < pos.y]
        next_obstacle = max(in_sight, key=lambda p: p.y, default=None)
    elif next_direction == Direction.E:
        in_sight = [o for o in grid if o.y == pos.y and o.x > pos.x]
        next_obstacle = min(in_sight, key=lambda p: p.x, default=None)
    elif next_direction == Direction.S:
        in_sight = [o for o in grid if o.x == pos.x and o.y > pos.y]
        next_obstacle = min(in_sight, key=lambda p: p.y, default=None)
    elif next_direction == Direction.W:
        in_sight = [o for o in grid if o.y == pos.y and o.x < pos.x]
        next_obstacle = max(in_sight, key=lambda p: p.x, default=None)
    
    if next_obstacle:
        return next_obstacle - next_direction, next_direction
    return None, None


def grid_to_graph(grid, start_pos, start_dir) -> dict[tuple[Vec, Direction], tuple[Vec, Direction]]:
    graph = {(start_pos, start_dir): next_position(grid, start_pos, DIRECTIONS[(DIRECTIONS.index(start_dir) - 1) % 4])}
    for obstacle in grid:
        # we will have to make a turn in all 4 adjacent points
        for direction in DIRECTIONS:
            pos = obstacle - direction  # guard would be at obstacle - direction, facing direction
            if pos not in grid:
                next_pos, next_direction = next_position(grid, pos, direction)
                graph[(pos, direction)] = (next_pos, next_direction)
    return graph
    

def next_node(graph, pos, direction, flip=1):
    if direction == Direction.N:
        in_sight = [(n, d) for n, d in graph if d == direction and n.x == pos.x and n.y < pos.y]
        next_node = max(in_sight, key=lambda p: p[0].y, default=None)
    elif direction == Direction.E:
        in_sight = [(n, d) for n, d in graph if d == direction and n.y == pos.y and n.x > pos.x]
        next_node = min(in_sight, key=lambda p: p[0].x, default=None)
    elif direction == Direction.S:
        in_sight = [(n, d) for n, d in graph if d == direction and n.x == pos.x and n.y > pos.y]
        next_node = min(in_sight, key=lambda p: p[0].y, default=None)
    elif direction == Direction.W:
        in_sight = [(n, d) for n, d in graph if d == direction and n.y == pos.y and n.x < pos.x]
        next_node = max(in_sight, key=lambda p: p[0].x, default=None)
    
    if next_node:
        return next_node
    return None, None


def insert(graph, grid, new_obstacle):
    new_graph = copy(graph)
    # adjust adjacent obstacles
    for direction in DIRECTIONS:
        pos = new_obstacle - direction
        if pos not in grid:
            # get the the node that (pos, direction) points to
            new_direction = DIRECTIONS[(DIRECTIONS.index(direction) + 1) % 4]
            if new_direction == Direction.N:
                in_sight = [(n, d) for n, d in graph if d == new_direction and n.x == pos.x and n.y < pos.y]
                next_node = max(in_sight, key=lambda p: p[0].y, default=None)
            elif new_direction == Direction.E:
                in_sight = [(n, d) for n, d in graph if d == new_direction and n.y == pos.y and n.x > pos.x]
                next_node = min(in_sight, key=lambda p: p[0].x, default=None)
            elif new_direction == Direction.S:
                in_sight = [(n, d) for n, d in graph if d == new_direction and n.x == pos.x and n.y > pos.y]
                next_node = min(in_sight, key=lambda p: p[0].y, default=None)
            elif new_direction == Direction.W:
                in_sight = [(n, d) for n, d in graph if d == new_direction and n.y == pos.y and n.x < pos.x]
                next_node = max(in_sight, key=lambda p: p[0].x, default=None)

            if next_node:
                new_graph[(pos, direction)] = next_node

            # get node that points to (pos, direction)
            prev_direction = DIRECTIONS[(DIRECTIONS.index(direction) - 1) % 4]
            # print(f"{prev_direction} -> {direction}")
            if direction == Direction.N:
                in_sight = [(n, d) for n, d in graph if d in [direction, prev_direction] and n.x == pos.x and n.y > pos.y]
                prev_node = min(in_sight, key=lambda p: p[0].y, default=None)
            elif direction == Direction.E:
                in_sight = [(n, d) for n, d in graph if d in [direction, prev_direction] and n.y == pos.y and n.x < pos.x]
                prev_node = max(in_sight, key=lambda p: p[0].x, default=None)
            elif direction == Direction.S:
                in_sight = [(n, d) for n, d in graph if d in [direction, prev_direction] and n.x == pos.x and n.y < pos.y]
                prev_node = max(in_sight, key=lambda p: p[0].y, default=None)
            elif direction == Direction.W:
                in_sight = [(n, d) for n, d in graph if d in [direction, prev_direction] and n.y == pos.y and n.x > pos.x]
                prev_node = min(in_sight, key=lambda p: p[0].x, default=None)
            
            if prev_node:
                new_graph[prev_node] = (pos, direction)
    return new_graph


def check_loop(graph, start, direction):
    seen = set()
    current = start
    while (current, direction) not in seen:
        seen.add((current, direction))
        current, direction = graph.get((current, direction), (None, None))
        if not current:
            return False
    return True


@watch.measure_time
def solve2(data):
    global path
    start, grid = data
    minx, maxx, miny, maxy = utils.corners(grid)
    # make grid sparse
    grid = {k: v for k, v in grid.items() if v != "."}
    graph = grid_to_graph(grid, start, Direction.N)
    obstacles = set()
    for x, y in tqdm(path):
        if Vec(x, y) == start or Vec(x, y) in grid:
            continue
        # put an obstacle at x, y
        new_graph = insert(graph, grid, Vec(x, y))
        if check_loop(new_graph, start, Direction.N):
            obstacles.add(Vec(x, y))

    print(utils.dictgrid_to_str(grid | {o: "O" for o in obstacles}, empty=".", keybuilder=Vec))
    return len(obstacles)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

