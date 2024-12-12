#!/usr/bin/env python

from pathlib import Path
from queue import Queue
from aoc import utils
from aoc.geometry import Vec, neighbours4, Direction
from aoc.data import GraphABC

watch = utils.stopwatch()


class Graph(GraphABC):
    def neighbours(self, node):
        return [n for n in neighbours4(node) if n in self.graph and self.graph[node] == self.graph[n]]


@watch.measure_time
def parse(raw_data):
    """returns list of ((name, points in region), points in border, area, perimeter)"""
    grid = utils.str_to_grid_dict(raw_data)
    grid = {Vec(*k): v for k, v in grid.items()}
    graph = Graph(grid)
    seen = set()
    regions = []
    for point in graph.graph:
        if point not in seen:
            region, border, area, perimeter = flood_fill(graph, point)
            seen |= region
            regions.append(((grid[point], region), border, area, perimeter))
    return regions



def flood_fill(graph: Graph, start: Vec):
    """returns points in region, border, area, permimeter"""
    region = set()
    border = set()
    perimeter = 0
    queue = Queue()
    queue.put(start)
    while not queue.empty():
        current = queue.get()
        if current in region:
            continue
        region.add(current)
        ns = graph.neighbours(current)
        perimeter += 4 - len(ns)
        if 4 - len(ns) > 0:
            border.add(current)
        # print(current, 4- len(ns))
        for n in ns:
            if n not in region:
                queue.put(n)
    return region, border, len(region), perimeter


@watch.measure_time
def solve1(data):
    price = 0
    for _, _, area, perimeter in data:
        price += area * perimeter
    return price


def count_sides(region, border):
    # region = Graph(region)
    # note that a border can be inside the region
    invariant_dir = {
        Direction.N: ("N", 0),  # if the border is facing north, the x-direction is invariant
        Direction.E: ("E", 1),  # if the border is facing east, the y-direction is invariant
        Direction.S: ("S", 0),
        Direction.W: ("W", 1),
    }
    sides = set()   # (facing, invariant coordinate)
    for point in border:
        for dir in invariant_dir:
            if point + dir not in region:
                sides.add((invariant_dir[dir][0], point.coords[invariant_dir[dir][1]]))
    print(sides)
    return len(sides)

def count_corners(region: set, border: set):
    ...


@watch.measure_time
def solve2(data):
    price = 0
    for (name, region), border, area, _ in data:
        n_sides = count_sides(region, border)
        print(f"{name}: {n_sides=}")
        price += area * n_sides
    return price


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

