#!/usr/bin/env python

from pathlib import Path
from queue import PriorityQueue
from collections import defaultdict
from functools import cache
from aoc import utils
from aoc.geometry import Vec, Direction
from aoc.data import WeightedGraphABC
from aoc.algos import dijkstra


watch = utils.stopwatch()


class WeightedGraph(WeightedGraphABC):
    @cache
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


def terrible_dijkstra(graph, start, end):
    queue = PriorityQueue()
    queue.put((0, start[1], [start[0]]))   # enqueue total_distance, facing, path_so_far
    distances = defaultdict(lambda: 1e15)
    distances[start] = 0
    valid_paths = defaultdict(list)   # maps total distance to list of paths
    while not queue.empty():
        current_distance, facing, current_path = queue.get()
        current_pos = current_path[-1]
        current = (current_pos, facing)
        for n in graph.neighbours(current):
            if n[0] in current_path:
                continue
            d = current_distance + graph.distance(current, n)
            if d > distances[n]:
                continue
            distances[n] = d
            if n[0] == end:
                valid_paths[d].append(current_path + [n[0]])
            else:
                queue.put((d, n[1], current_path + [n[0]]))
    return valid_paths


@watch.measure_time
def solve2(data):
    graph, start, end = data
    paths = terrible_dijkstra(graph, start, end)
    min_dist = min(paths.keys())
    on_path = set(sum(paths[min_dist], start=[]))
    return len(on_path)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

