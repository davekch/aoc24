#!/usr/bin/env python

from pathlib import Path
from collections import defaultdict
from itertools import combinations
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    connections = defaultdict(list)
    for line in raw_data.splitlines():
        a, b = line.split("-")
        connections[a].append(b)
        connections[b].append(a)
    return connections


@watch.measure_time
def solve1(data):
    triplets = []
    for node, connections in data.items():
        for n2, n3 in combinations(connections, 2):
            if node in data[n2] and n3 in data[n2] and node in data[n3] and n2 in data[n3]:
                triplet = {node, n2, n3}
                if triplet not in triplets and any(n.startswith("t") for n in triplet):
                    triplets.append(triplet)
    return len(triplets)


def build_cluster(graph, node, cluster):
    for n in graph[node]:
        if n in cluster:
            continue
        if all(n in graph[nn] for nn in cluster):
            cluster |= build_cluster(graph, n, cluster | {n})
    return cluster


@watch.measure_time
def solve2(data):
    max_cluster = set()
    for node in data:
        cluster = build_cluster(data, node, {node})
        if len(cluster) > len(max_cluster):
            max_cluster = cluster
    return ",".join(sorted(max_cluster))


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

