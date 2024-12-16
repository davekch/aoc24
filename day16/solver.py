#!/usr/bin/env python

from pathlib import Path
import rich
from aoc import utils
from aoc.geometry import Vec, neighbours4, Direction
from aoc.data import WeightedGraphABC
from aoc.algos import dijkstra, shortestpath


watch = utils.stopwatch()


class WeightedGraph(WeightedGraphABC):
    def neighbours(self, node):
        # nodes are (position, facing)
        ns = []
        for dir in [Direction.N, Direction.E, Direction.S, Direction.W]:
            if dir == -node[1]:
                continue
            n = (node[0] + dir, dir)
            if n in self.graph:
                ns.append(n)
        return ns

    def distance(self, node1, node2):
        if node1[1] == node2[1]:
            return 1
        return 1001  # 1000 for turning, 1 for moving


@watch.measure_time
def parse(raw_data):
    nodes = set()
    start = end = None
    for y, line in enumerate(raw_data.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                continue
            for dir in [Direction.N, Direction.E, Direction.S, Direction.W]:
                nodes.add((Vec(x, y), dir))
            if c == "S":
                start = (Vec(x, y), Direction.E)
            elif c == "E":
                end = Vec(x, y)
    graph = WeightedGraph(nodes)
    return graph, start, end


@watch.measure_time
def solve1(data):
    graph, start, end = data

    def finished(node):
        return node[0] == end

    current, distances, _ = dijkstra(graph, start, finished=finished)
    return distances[current]


@watch.measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

