#!/usr/bin/env python

from pathlib import Path
from bidict import frozenbidict
from functools import cache
from collections import Counter
from aoc import utils
from aoc.geometry import Vec, Direction


watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    return raw_data.splitlines()


numeric_keypad = frozenbidict({
    "7": Vec(0, 0),
    "8": Vec(1, 0),
    "9": Vec(2, 0),
    "4": Vec(0, 1),
    "5": Vec(1, 1),
    "6": Vec(2, 1),
    "1": Vec(0, 2),
    "2": Vec(1, 2),
    "3": Vec(2, 2),
    "0": Vec(1, 3),
    "A": Vec(2, 3),
})


directional_keypad = frozenbidict({
    "^": Vec(1, 0),
    "A": Vec(2, 0),
    "<": Vec(0, 1),
    "v": Vec(1, 1),
    ">": Vec(2, 1),
})


pads = {
    "numeric": numeric_keypad,
    "directional": directional_keypad,
}


directions = {
    Direction.N: "^",
    Direction.E: ">",
    Direction.S: "v",
    Direction.W: "<",
}


@cache
def get_paths(start_: str, target_: str, pad: str) -> list[str]:
    start = pads[pad][start_]
    target = pads[pad][target_]
    # assume that it is sufficient to only consider paths that go as straight as possible
    # two possibilities: horizontal first, then vertical, or the other way round
    def walk(dir) -> list:
        current = start
        path = ""
        while current != target:
            if dir == "x":  # urgh
                if current.x != target.x:
                    delta = Vec((target.x - current.x) // abs(target.x - current.x), 0)
                    if current + delta not in pads[pad].inverse:
                        dir = "y"
                        continue
                else:
                    dir = "y"
                    continue
            elif dir == "y":
                if current.y != target.y:
                    delta = Vec(0, (target.y - current.y) // abs(target.y - current.y))
                    if current + delta not in pads[pad].inverse:
                        dir = "x"
                        continue
                else:
                    dir = "x"
                    continue
            current += delta
            path += pads[pad].inverse[current]
        return path
    
    return [walk("x"), walk("y")]


def counter_len(c: Counter) -> int:
    return sum(len(code) * n for code, n in c.items())


@cache
def count_keypad_sequences(code: str, robots: tuple) -> Counter[str]:
    keypad, *controllers = robots
    position = "A"
    if not controllers:
        return Counter({code: 1})

    result = Counter()
    for key in code:
        # figure out possibilities how to get from the current position to the next key
        paths = get_paths(position, key, keypad)
        # tranlsate the paths into what needs to be pressed on the controller
        controller_codes = []
        for path in paths:
            current = position
            controller_code = ""
            for p in path:
                controller_code += directions[pads[keypad][p] - pads[keypad][current]]
                current = p
            controller_codes.append(controller_code + "A")
        # now we know what needs to be pressed on the first controller in order to move the
        # finger along each of the paths to get to key -> figure out which of
        # the paths requires the least key presses
        key_presses = [count_keypad_sequences(subcode, tuple(controllers)) for subcode in controller_codes]
        best = min(key_presses, key=counter_len)
        result += best
        position = key

    return result


def solve(data, robots):
    result = 0
    for code in data:
        counter = count_keypad_sequences(code, robots)
        result += int(code[:-1]) * counter_len(counter)
    return result


@watch.measure_time
def solve1(data):
    robots = ("numeric", "directional", "directional", "directional")
    return solve(data, robots)


@watch.measure_time
def solve2(data):
    robots = ("numeric",) + 26 * ("directional",)
    return solve(data, robots)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

