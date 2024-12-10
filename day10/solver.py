#!/usr/bin/env python

from pathlib import Path
from functools import cache
from aoc import utils
from aoc.geometry import Vec, neighbours4
from aoc.data import GraphABC

watch = utils.stopwatch()


class Graph(GraphABC):
    @cache
    def neighbours(self, node: Vec):
        return [n for n in neighbours4(node) if n in self.graph and self.graph[n] - 1 == self.graph[node]]

    @cache
    def reachable_tops(self, start: Vec):
        ns = self.neighbours(start)
        tops = []
        for n in ns:
            if self.graph[n] == 9:
                tops.append(n)
            else:
                tops += self.reachable_tops(n)
        return tops


@watch.measure_time
def parse(raw_data):
    grid = utils.str_to_grid_dict(raw_data)
    grid = {Vec(*p): int(h) for p, h in grid.items()}
    return Graph(grid)


@watch.measure_time
def solve1(data):
    starts = [s for s in data.graph if data.graph[s] == 0]
    s = 0
    for start in starts:
        s += len(set(data.reachable_tops(start)))
    return s


@watch.measure_time
def solve2(data):
    starts = [s for s in data.graph if data.graph[s] == 0]
    s = 0
    for start in starts:
        s += len(data.reachable_tops(start))
    return s


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

