#!/usr/bin/env python

from pathlib import Path
import math
from copy import copy
import numba
import re
# from aoc import utils

# watch = utils.stopwatch()


def ints(s: str) -> list[int]:
    return list(map(int, re.findall(r"[+-]?\d+", s)))

# @watch.measure_time
def parse(raw_data):
    lines = iter(raw_data.splitlines())
    register = {}
    register["A"] = ints(next(lines))[0]
    register["B"] = ints(next(lines))[0]
    register["C"] = ints(next(lines))[0]
    next(lines)
    program = ints(next(lines))
    return register, program


@numba.njit
def combo(operand, register):
    if operand <= 3:
        return operand
    elif operand == 4:
        return register["A"]
    elif operand == 5:
        return register["B"]
    elif operand == 6:
        return register["C"]
    else:
        raise ValueError()


def instruction(opcode, operand, register, i, output):
    if opcode == 0:
        register["A"] = math.floor(register["A"] / 2 ** combo(operand, register))
        return i + 2
    if opcode == 1:
        register["B"] = register["B"] ^ operand
        return i + 2
    if opcode == 2:
        register["B"] = int(str(combo(operand, register) % 8)[:3])
        return i + 2
    if opcode == 3:
        if register["A"] == 0:
            return i + 2
        return operand
    if opcode == 4:
        register["B"] = register["B"] ^ register["C"]
        return i + 2
    if opcode == 5:
        output.append(combo(operand, register) % 8)
        return i + 2
    if opcode == 6:
        register["B"] = math.floor(register["A"] / 2 ** combo(operand, register))
        return i + 2
    if opcode == 7:
        register["C"] = math.floor(register["A"] / 2 ** combo(operand, register))
        return i + 2


# @watch.measure_time
def solve1(data):
    register, program = data
    # print(register)
    # print(program)
    i = 0
    output = []
    while i < len(program):
        i = instruction(program[i], program[i+1], register, i, output)
        # print(i)
    return ",".join(map(str, output))


jitted_instruction = numba.njit(instruction)
# jitted_combo = numba.njit(combo)


# @watch.measure_time
@numba.njit(parallel=True)
def solve2(data):
    register_backup, program = data
    quine = ",".join(map(str, program))
    for A in numba.prange(int(1e15)):
        if A % 100000000:
            print(A)
        register = [v for v in register_backup.values()]
        register["A"] = A
        i = 0
        output = numba.typed.List()
        while i < len(program):
            i = jitted_instruction(program[i], program[i+1], register, i, output)
            # print(i)
        if quine == ",".join(map(str, output)):
            return A


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    # watch.print_times()

