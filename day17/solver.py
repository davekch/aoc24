#!/usr/bin/env python

from pathlib import Path
import math
from copy import copy
import re
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    lines = iter(raw_data.splitlines())
    register = {}
    register["A"] = utils.ints(next(lines))[0]
    register["B"] = utils.ints(next(lines))[0]
    register["C"] = utils.ints(next(lines))[0]
    next(lines)
    program = utils.ints(next(lines))
    return register, program


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


def run(register, program):
    i = 0
    output = []
    while i < len(program):
        i = instruction(program[i], program[i+1], register, i, output)
    return output

def run_while_quine(register, program):
    i = 0
    quine_i = 0
    output = []
    while i < len(program):
        _i = instruction(program[i], program[i+1], register, i, output)
        if program[i] == 5:
            # something was added to the output
            if output[quine_i] != program[quine_i]:
                return output
            else:
                quine_i += 1
        i = _i
    return output


@watch.measure_time
def solve1(data):
    register, program = data
    output = run(register, program)
    return ",".join(map(str, output))


@watch.measure_time
def solve2(data):
    register_backup, program = data
    for A in range(int(1e15)):
        if A % 100000 == 0:
            print(A)
        register = copy(register_backup)
        register["A"] = A
        output = run_while_quine(register, program)
        if output == program:
            return A


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

