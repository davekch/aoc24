import matplotlib.pyplot as plt
import numpy as np

from solver import *


initial_state = (
    ("A", "numeric"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
    ("A", "directional"),
)


data = parse(open("input.txt").read().strip())
data = [data[0]]  # only do this for one code
lengths = []
n_robots = list(range(1, 21))

for n in n_robots:
    state = initial_state[:n]
    results = solve(data, state)
    presses, = results.values()
    lengths.append(len(presses))


plt.plot(n_robots, lengths, marker="o")
plt.yscale("log")
plt.xlabel("number of robots controlling each other")
plt.ylabel("length of final sequence")
plt.show()