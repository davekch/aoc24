#!/usr/bin/env python

from pathlib import Path
from queue import Queue
from itertools import combinations
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
            region, area, perimeter = flood_fill(graph, point)
            seen |= region
            regions.append(((grid[point], region), area, perimeter))
    return regions



def flood_fill(graph: Graph, start: Vec):
    """returns points in region, border, area, permimeter"""
    region = set()
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
        # print(current, 4- len(ns))
        for n in ns:
            if n not in region:
                queue.put(n)
    return region, len(region), perimeter


@watch.measure_time
def solve1(data):
    price = 0
    for _, area, perimeter in data:
        price += area * perimeter
    return price


def count_corners(region: set, tile: Vec):
    """calculates how many corners this tile contributes to the shape"""
    neighbours = [n for n in neighbours4(tile) if n in region]
    if len(neighbours) == 0:
        return 4
    elif len(neighbours) == 1:
        return 2
    else:
        filled_diagonals = 0
        antiparallel = 0
        for n1, n2 in combinations(neighbours, 2):
            if tile - n1 != n2 - tile:
                # they are perpendicular, check the tile between
                if tile + (n1 - tile) + (n2 - tile) in region:
                    filled_diagonals += 1
            else:
                antiparallel += 1

        if len(neighbours) == 2:
            if antiparallel:
                return 0
            else:
                return 2 - filled_diagonals
        elif len(neighbours) == 3:
            return 2 - filled_diagonals
        elif len(neighbours) == 4:
            return 4 - filled_diagonals


@watch.measure_time
def solve2(data):
    price = 0
    for (name, region), area, _ in data:
        n_sides = 0
        for tile in region:
            n_sides += count_corners(region, tile)  # number of corners and sides is the same
        # print(f"{name}: {area=} {n_sides=}")
        price += area * n_sides
    return price


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

