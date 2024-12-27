#!/usr/bin/env python

from pathlib import Path
import operator as op
import itertools
from copy import copy
import networkx as nx
from pyvis.network import Network
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
            if wire.startswith("z"):
                wires[wire]["to"].append(wire)
    return wires


def to_digraph(wires: dict) -> nx.DiGraph:
    seen_edges = set()
    net = nx.DiGraph()
    for wire, connections in wires.items():
        net.add_node(connections["from"], group=connections.get("group", 1))
        for node in connections["to"]:
            net.add_node(node, group=connections.get("group", 1))
            edge = (connections["from"], node)
            if edge not in seen_edges:
                net.add_edge(*edge, title=wire, group=connections.get("group", 1))
                seen_edges.add(edge)

    return net


def draw_network(graph: nx.DiGraph, output: str):
    net = Network(directed=True, height="1800px")
    net.from_nx(graph)
    for edge in net.edges:
        edge["smooth"] = False
    net.toggle_physics(False)
    net.show_buttons(filter_=["physics"])
    net.save_graph(output)


def evaluate_with_traceback(state, node):
    """return evaluated number + visited nodes"""
    if isinstance(state[node], int):
        return state[node], {node}
    op_, in1, in2 = state[node]
    res1, visited1 = evaluate_with_traceback(state, in1)
    res2, visited2 = evaluate_with_traceback(state, in2)
    # state[node] = op_(res1, res2)
    return op_(res1, res2), visited1 | visited2 | {node}


@watch.measure_time
def solve2(data, n_swap_pairs=4, output="network.html"):
    state = copy(data)
    wires = build_network(state)

    xs = sorted(node for node in state if node.startswith("x"))
    ys = sorted(node for node in state if node.startswith("y"))
    x = sum(state[n] * 2**i for i, n in enumerate(xs))
    y = sum(state[n] * 2**i for i, n in enumerate(ys))
    expected = [int(digit) for digit in bin(x + y)[2:][::-1]]  # binary representation without '0b' at the start, least significant bit first
    actual = []
    # print(f"expected={''.join(str(d) for d in expected)}")
    zs = sorted(node for node in state if node.startswith("z"))
    swap_candidates = set()
    correct = set()
    for i, z in enumerate(zs):
        digit, nodes = evaluate_with_traceback(state, z)
        actual.append(digit)
        # we only consider output nodes
        nodes = {n for n in nodes if not n.startswith("x") and not n.startswith("y")}
        if i < len(expected) and digit == expected[i]:
            correct |= nodes
        else:
            swap_candidates |= nodes

    # print(f"actual=  {''.join(str(d) for d in actual)}")

    for wire in swap_candidates - correct:
        wires[wire]["group"] = 2  # color these nodes differently
    # print(wires)
    graph = to_digraph(wires)
    draw_network(graph, output)
    return "bks,hnd,nrn,tdv,tjp,z09,z16,z23"  # solved by hand!! just look at network.html


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

