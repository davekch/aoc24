#!/usr/bin/env python

from pathlib import Path
from aoc import utils
from aoc.geometry import Vec, neighbours4
from aoc.data import GraphABC
from aoc.algos import BFS, shortestpath

watch = utils.stopwatch()


class Graph(GraphABC):
    def __init__(self, graph, bounds):
        super().__init__(graph)
        self.bounds = bounds

    def neighbours(self, node):
        return [n for n in neighbours4(node) if n not in self.graph and 0 <= n.x <= self.bounds and 0 <= n.y <= self.bounds]


@watch.measure_time
def parse(raw_data):
    falling = []
    for line in raw_data.splitlines():
        falling.append(Vec(*utils.ints(line)))
    return falling


@watch.measure_time
def solve1(data: list[Vec], size=70, steps=1024):
    start = Vec(0, 0)
    end = Vec(size, size)
    corrupted = data[:steps]
    graph = Graph(set(corrupted), size)

    def finished(node):
        return node == end

    path = BFS(graph, start, finished=finished)
    shortest = shortestpath(path, start, end)

    # print(utils.dictgrid_to_str(
    #     {c: "#" for c in graph.graph} | {p: "O" for p in shortest},
    #     empty=".", keybuilder=Vec
    # ))
    return len(shortest) - 1


@watch.measure_time
def solve2(data, size=70, steps=1024):
    start = Vec(0, 0)
    end = Vec(size, size)

    def finished(node):
        return node == end

    graph = Graph(set(data[:steps]), size)
    path = BFS(graph, start, finished=finished)
    for i in range(steps, len(data)):
        byte = data[i]
        if byte in path:
            graph = Graph(set(data[:i+1]), size)
            path = BFS(graph, start, finished=finished)
            if end not in path:
                return f"{byte.x},{byte.y}"


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

