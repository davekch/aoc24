#!/usr/bin/env python

from pathlib import Path
from bidict import frozenbidict
from functools import cache
from collections import defaultdict, Counter
import rich
import re
import rich.pretty
from tqdm import tqdm
from aoc import utils
from aoc.geometry import Vec, Direction

try:
    from itertools import batched
except ImportError:
    # for pypy
    def batched(l, n):
        i = 0
        while i < len(l):
            yield l[i:i+n]
            i += n

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


directions = frozenbidict({
    "^": Direction.N,
    ">": Direction.E,
    "v": Direction.S,
    "<": Direction.W,
})


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


@cache
def least_presses(to: str, state: tuple) -> tuple[list, tuple]:
    """
    calculates the sequence of least keypresses on the last controller to get
    the first robot to `to`. returns the sequence and the updated state
    """
    # print(len(state))
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
            controller_target = directions.inverse[pads[keypad][p] - pads[keypad][current]]
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


def counter_len(c: Counter) -> int:
    return sum(len(code) * n for code, n in c.items())


@cache
def least_presses__(code: str, state: tuple) -> tuple[Counter[str], tuple]:
    robot, *controllers = state
    position, keypad = robot
    if not controllers:
        return Counter({code: 1}), ((code[-1], keypad),)

    result = Counter()
    for key in code:
        paths = get_paths(position, key, keypad)
        # tranlsate the paths into what needs to be pressed on the controller
        controller_codes = []
        for path in paths:
            current = position
            controller_code = ""
            for p in path:
                controller_code += directions.inverse[pads[keypad][p] - pads[keypad][current]]
                current = p
            controller_codes.append(controller_code + "A")
        # now we know what needs to be pressed on the first controller in order to move the
        # finger along each of the paths to get to key -> figure out which of
        # the paths requires the least key presses
        key_presses = [least_presses__(subcode, tuple(controllers)) for subcode in controller_codes]
        best, new_controllers = min(key_presses, key=lambda i: counter_len(i[0]))
        result += best
        position = key

    return result, new_controllers



def solve(data, initial_state, progress_bar=False):
    results = defaultdict(str)
    for code in data:
        # print(code)
        state = initial_state
        if progress_bar:
            iter_code = tqdm(code)
        else:
            iter_code = code
        for key in iter_code:
            # print(least_presses.cache_info())
            # print(key)
            presses, state = least_presses(key, state)
            results[code] += "".join(presses)
        #     print("".join(presses), end="")
        # print()
        assert all(k == "A" for k, _ in state)
    return results


def calculate_complexities(results):
    result = 0
    for code, presses in results.items():
        result += int(code[:-1]) * len(presses)
    return result


@watch.measure_time
def solve1(data):
    initial_state = (
        ("A", "numeric"),
        ("A", "directional"),
        ("A", "directional"),
        ("A", "directional"),
    )
    results = solve(data, initial_state)
    # rich.print({code: Counter(re.findall(r"[<>^v]*A", presses)) for code, presses in results.items()})
    return calculate_complexities(results)


@cache
def solve_partial_code(code, states):
    """
    get the sequence of keypresses on the last controller needed make the first robot
    punch in the code
    """
    total_presses = ""
    for key in code:
        presses, states = least_presses(key, states)
        total_presses += "".join(presses)
    return total_presses


@watch.measure_time
def solve2(data, robots=None):
    if not robots:
        robots = (
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

    result = 0
    for code in data:
        counter, _ = least_presses__(code, robots)
        result += int(code[:-1]) * counter_len(counter)
    return result
    # results = solve(data, robots)
    # return calculate_complexities(results)

    test_result = solve(data, robots)
    print("test:")
    rich.print(test_result)
    # rich.print({code: Counter(re.findall(r"[<>^v]*A", presses)) for code, presses in test_result.items()})

    results = {code: Counter({code: 1}) for code in data}
    for code in results:
        counter = results[code]
        print(code)
        for i in range(len(robots) - 1):
            robot = robots[i]
            controller = robots[i+1]
            # print(f"{code=}")
            new_counter = Counter()
            for partial_code in counter.keys():
                # print(f" {partial_code=}")
                presses = solve_partial_code(partial_code, (robot, controller))
                # print(presses)
                # devide the sequence into chunks that end with A -> this way we don't
                # really need to care about state + we increase cache hit rate (?)
                for new_partial_code in re.findall(r"[<>^v]*A", presses):
                    new_counter[new_partial_code] += counter[partial_code]
            # print(new_counter)
            results[code] = new_counter
            counter = new_counter
            print(f"  {new_counter=}")
        print()

    # rich.print(results)

    print()
    for (code, expected), actual in zip(test_result.items(), results.values()):
        expected = Counter(re.findall(r"[<>^v]*A", expected))
        if expected != actual:
            print(f"{code} differs!")
            rich.print(expected)
            rich.print(actual)
            print()

    result = 0
    for code, counter in results.items():
        result += int(code[:-1]) * sum(len(partial) * n for partial, n in counter.items())
    return result


# 10547227264 too low
# 485508384600 not right


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

