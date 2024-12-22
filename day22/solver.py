#!/usr/bin/env python

from pathlib import Path
import math
from collections import Counter, deque
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return list(map(int, raw_data.splitlines()))


def next_secret(secret: int) -> int:
    # first step
    next_secret = (secret * 64) ^ secret
    next_secret = next_secret % 16777216
    # second step
    next_secret = math.floor(next_secret / 32) ^ next_secret
    next_secret = next_secret % 16777216
    # third step
    next_secret = (next_secret * 2048) ^ next_secret
    return next_secret % 16777216


@watch.measure_time
def solve1(data):
    s = 0
    for num in data:
        for _ in range(2000):
            num = next_secret(num)
        s += num
    return s


@watch.measure_time
def solve2(data):
    bananas = Counter()
    for num in data:
        sequence = deque()
        price = num % 10
        _bananas = Counter()
        for _ in range(2000):
            num = next_secret(num)
            new_price = num % 10
            diff = new_price - price
            price = new_price
            sequence.append(diff)
            if len(sequence) > 4:
                sequence.popleft()
            _s = tuple(sequence)
            if _s not in _bananas:
                _bananas[_s] = price
        bananas += _bananas
    bananas = Counter({s: v for s, v in bananas.items() if len(s) == 4})
    (seq, b), = bananas.most_common(1)
    return b


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

