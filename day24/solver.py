#!/usr/bin/env python

from pathlib import Path
import operator as op
import itertools
from copy import copy
import networkx as nx
import bidict
import matplotlib.pyplot as plt
from aoc import utils

watch = utils.stopwatch()


ops = bidict.bidict({
    "AND": op.and_,
    "OR": op.or_,
    "XOR": op.xor,
})


@watch.measure_time
def parse(raw_data):
    upper, lower = raw_data.split("\n\n")
    state = {}
    for line in upper.splitlines():
        k, v = line.split(": ")
        state[k] = int(v)
    for line in lower.splitlines():
        line = line.replace(" -> ", " ")
        in1, op_, in2, out = line.split()
        state[out] = (ops[op_], in1, in2)
    return state


def evaluate(state, node):
    if isinstance(state[node], int):
        return state[node]
    op_, in1, in2 = state[node]
    state[node] = op_(evaluate(state, in1), evaluate(state, in2))
    return state[node]


@watch.measure_time
def solve1(data):
    state = copy(data)
    zs = sorted(node for node in state if node.startswith("z"))
    result = 0
    for i, z in enumerate(zs):
        result += evaluate(state, z) * 2**i
    return result


def build_network(data):
    wires = {}

    for wire in data:
        if isinstance(data[wire], int):
            wires[wire] = {"from": wire, "to": []}
        else:
            op_, in1, in2 = data[wire]
            node = f"{in1} {ops.inverse[op_]} {in2} -> {wire}"
            # initialize
            if wire not in wires:
                wires[wire] = {"from": None, "to": []}
            if in1 not in wires:
                wires[in1] = {"from": None, "to": []}
            if in2 not in wires:
                wires[in2] = {"from": None, "to": []}
            # set correct values
            wires[wire]["from"] = node
            wires[in1]["to"].append(node)
            wires[in2]["to"].append(node)

    seen_edges = set()
    edge_labels = {}
    net = nx.DiGraph()
    for wire, connections in wires.items():
        net.add_node(connections["from"])
        for node in connections["to"]:
            net.add_node(node)
            edge = (connections["from"], node)
            if edge not in seen_edges:
                net.add_edge(*edge)
                seen_edges.add(edge)
                edge_labels[edge] = wire

    return net, edge_labels


def draw_network(graph: nx.DiGraph, labels: dict):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.axis("off")
    plt.show()


def evaluate_with_traceback(state, node):
    """return evaluated number + visited nodes"""
    if isinstance(state[node], int):
        return state[node], {node}
    op_, in1, in2 = state[node]
    res1, visited1 = evaluate_with_traceback(state, in1)
    res2, visited2 = evaluate_with_traceback(state, in2)
    # state[node] = op_(res1, res2)
    return op_(res1, res2), visited1 | visited2 | {node}


def all_pairings(items):
    if len(items) % 2 != 0:
        raise ValueError("The number of elements must be even.")
    
    if len(items) == 2:
        return [[items]]
    
    results = []
    # take one element and pair it with each other element
    for pair in itertools.combinations(items, 2):
        remaining = [i for i in items if i not in pair]
        for rest in all_pairings(remaining):
            results.append([list(pair)] + rest)
    return results


@watch.measure_time
def solve2(data, n_swap_pairs=4):
    state = copy(data)
    xs = sorted(node for node in state if node.startswith("x"))
    ys = sorted(node for node in state if node.startswith("y"))
    x = sum(state[n] * 2**i for i, n in enumerate(xs))
    y = sum(state[n] * 2**i for i, n in enumerate(ys))
    expected = [int(digit) for digit in bin(x + y)[2:]]  # binary representation without '0b' at the start
    # print(f"{expected=}")
    zs = sorted(node for node in state if node.startswith("z"))
    # swap_candidates = {
    #     0: set(),  # leads to 0, should be 1
    #     1: set(),  # leads to 1, should be 0
    # }
    swap_candidates = set()
    correct = set()
    for i, z in enumerate(zs):
        digit, nodes = evaluate_with_traceback(state, z)
        # we only consider output nodes
        nodes = {n for n in nodes if not n.startswith("x") and not n.startswith("y")}
        if digit == expected[i]:
            correct |= nodes
        else:
            # swap_candidates[digit] |= nodes
            swap_candidates |= nodes
    
    # print(len([n for n in (swap_candidates[0] | swap_candidates[1] )- correct if not n.startswith("x") and not n.startswith("y")]))
    
    to_swap = swap_candidates # - correct
    print(len(to_swap))
    print(to_swap)
    for swapgroup in itertools.combinations(to_swap, 8):
        for pairs in all_pairings(swapgroup):
            state = copy(data)
            for n1, n2 in pairs:
                state[n1], state[n2] = state[n2], state[n1]
            result = watch.ignore(solve1)(state)
            if result == x + y:
                return ",".join(sorted(swapgroup))
    return

    # print(len(swap_candidates[0] - correct), len(swap_candidates[1] - correct))
    print(swap_candidates)
    for swapgroup1 in itertools.combinations(swap_candidates[0], n_swap_pairs):
        for swapgroup2 in itertools.combinations(swap_candidates[1], n_swap_pairs):
            state = copy(data)
            for swp1, swp2 in itertools.product(swapgroup1, swapgroup2):
                state[swp1], state[swp2] = state[swp2], state[swp1]
            result = watch.ignore(solve1)(state)
            print(result, x+y)
            if result == x + y:
                return ",".join(sorted(set(swapgroup1) | set(swapgroup2)))



if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

