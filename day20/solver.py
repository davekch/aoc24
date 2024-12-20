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
    graph = Graph(grid)
    path = BFS(graph, start, finished=lambda p: p == end)
    return shortestpath(path, start, end)


def count_cheats(path, i, distance):
    saved = Counter()  # counts number of picoseconds saved
    cheat_start = path[i]
    # get all points that are distance away from start
    for k in range(-distance, distance+1):
        for l in range(-(distance-abs(k)), distance-abs(k)+1):
            # ignore direct neighbors, no cheating needed for them
            if abs(k) + abs(l) > 1:
                cheat_end = Vec(cheat_start.x + k, cheat_start.y + l)
                if cheat_end in path:
                    # see if it's further down the path than we are now
                    # and if it saves time
                    j = path.index(cheat_end)
                    if j > i:
                        time_saved = j - i - abs(k) - abs(l)
                        saved[time_saved] += 1
    return saved


@watch.measure_time
def solve1(data):
    cheat_saves = Counter()
    from tqdm import tqdm
    for i in tqdm(range(len(data))):
        cheat_saves += count_cheats(data, i, 2)
    # print(cheat_saves)
    result = 0
    for save, n in cheat_saves.items():
        if save >= 100:
            result += n
    return result


@watch.measure_time
def solve2(data):
    cheat_saves = Counter()
    from tqdm import tqdm
    for i in tqdm(range(len(data))):
        cheat_saves += count_cheats(data, i, 20)
    result = 0
    for save, n in cheat_saves.items():
        if save >= 100:
            # print(f"{n} cheats to save {save}")
            result += n
    return result


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

