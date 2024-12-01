from collections import Counter
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    xs, ys = [], []
    for line in raw_data.splitlines():
        x, y = utils.ints(line)
        xs.append(x)
        ys.append(y)
    return xs, ys


@watch.measure_time
def solve1(data):
    xs, ys = data
    s = 0
    for x, y in zip(sorted(xs), sorted(ys)):
        s += abs(x - y)
    return s


@watch.measure_time
def solve2(data):
    xs, ys = data
    right = Counter(ys)
    s = 0
    for x in xs:
        s += x * right[x]
    return s


if __name__ == "__main__":
    data = parse(open("input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

