#!/usr/bin/env python

from pathlib import Path
from bidict import frozenbidict
from functools import cache
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


directions = frozenbidict({
    "^": Direction.N,
    ">": Direction.E,
    "v": Direction.S,
    "<": Direction.W,
})


@cache
def get_paths(start_: str, target_: str, pad: frozenbidict) -> list[str]:
    start = pad[start_]
    target = pad[target_]
    # assume that it is sufficient to only consider paths that go as straight as possible
    # two possibilities: horizontal first, then vertical, or the other way round
    def walk(dir) -> list:
        current = start
        path = []
        while current != target:
            if dir == "x":  # urgh
                if current.x != target.x:
                    delta = Vec((target.x - current.x) // abs(target.x - current.x), 0)
                    if current + delta not in pad.inverse:
                        dir = "y"
                        continue
                else:
                    dir = "y"
                    continue
            elif dir == "y":
                if current.y != target.y:
                    delta = Vec(0, (target.y - current.y) // abs(target.y - current.y))
                    if current + delta not in pad.inverse:
                        dir = "x"
                        continue
                else:
                    dir = "x"
                    continue
            current += delta
            path.append(pad.inverse[current])
        return path
    
    return [walk("x"), walk("y")]


@cache
def least_presses(to: str, state: tuple) -> tuple[list, tuple]:
    # state: ((current, keypad), (current, keypad), ...)
    #          ^ target robot     ^
    #                             ^ robot controlling target robot ...
    this, *controllers = state
    position, keypad = this
    if not controllers:
        # we can directly control this robot, just press the button and update state
        return [to], ((to, keypad),)

    paths = get_paths(position, to, keypad)
    keypresses = []  # store pressed keys + final new state here
    # try out all paths to the desired key to find which requires the least key presses
    # given the current state of the controlling robots
    for path in paths:
        pressed_keys = []
        new_controllers = tuple(controllers)
        current = position
        for p in path:
            # figure out what to press on the first controller to get from current to p
            controller_target = directions.inverse[keypad[p] - keypad[current]]
            keys_, new_controllers = least_presses(controller_target, new_controllers)
            pressed_keys.extend(keys_)
            current = p
        # now press A on the first controller to confirm
        keys_, new_controllers = least_presses("A", new_controllers)
        pressed_keys.extend(keys_)
        # save pressed keys and new state
        keypresses.append((pressed_keys, new_controllers))

    best, new_controllers = min(keypresses, key=lambda i: len(i[0]))
    new_state = ((to, keypad), *new_controllers)
    return best, new_state


def solve(data, initial_state):
    result = 0
    for code in data:
        length = 0
        state = initial_state
        for key in code:
            presses, state = least_presses(key, state)
            length += len(presses)
        assert all(k == "A" for k, _ in state)
        result += int(code[:-1]) * length
    return result


@watch.measure_time
def solve1(data):
    initial_state = (
        ("A", numeric_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
    )
    return solve(data, initial_state)


@watch.measure_time
def solve2(data):
    initial_state = (
        ("A", numeric_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
        ("A", directional_keypad),
    )
    return solve(data, initial_state)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

