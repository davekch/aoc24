#!/usr/bin/env python

from pathlib import Path
from collections import Counter
from aoc import utils
from aoc.geometry import Vec, neighbours4
from aoc.data import GraphABC
from aoc.algos import BFS, shortestpath

watch = utils.stopwatch()


class Graph(GraphABC):
    def neighbours(self, node):
        return [n for n in neighbours4(node) if n in self.graph and self.graph[n] != "#"]


@watch.measure_time
def parse(raw_data):
    grid = utils.str_to_grid_dict(raw_data, keybuilder=Vec)
    for point, char in grid.items():
        if char == "S":
            start = point
            grid[point] = "."
        elif char == "E":
            end = point
            grid[point] = "."
    return Graph(grid), start, end


@watch.measure_time
def solve1(data):
    graph, start, end = data
    path = BFS(graph, start, finished=lambda p: p == end)
    best_no_cheating = len(shortestpath(path, start, end))
    cheat_saves = Counter()
    from tqdm import tqdm
    for point in tqdm(graph.graph):
        if graph.graph[point] != "#":
            continue
        # disable this wall and do BFS again
        graph.graph[point] = "."
        path = BFS(graph, start, finished=lambda p: p == end)
        best_cheating = len(shortestpath(path, start, end))
        cheat_saves[best_no_cheating - best_cheating] += 1
        # add wall back in again
        graph.graph[point] = "#"
    result = 0
    for save, n in cheat_saves.items():
        if save >= 100:
            result += n
    return result



@watch.measure_time
def solve2(data):
    pass


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

