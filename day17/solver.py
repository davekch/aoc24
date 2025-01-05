#!/usr/bin/env python

from pathlib import Path
import math
from copy import copy
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
        register["B"] = combo(operand, register) % 8
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


@watch.measure_time
def solve1(data):
    register, program = data
    register = copy(register)
    output = run(register, program)
    return ",".join(map(str, output))


# my program translates to
# B = 0
# C = 0
# while A != 0:
#     B = (A % 8) ^ 1            # B becomes least significant digit of A (in base 8) XOR 1
#     C = math.floor(A / 2**B)   # C is dependent on the whole value of A
#     A = math.floor(A / 8)      # A strips off its least significant digit (in base 8)
#     B = B ^ 4
#     B = B ^ C
#     output.append(B % 8)
#
# (thinking in base 8) at each step, A gets reduced by one digit
# this means we can work our way up digit by digit
# the first output depends on the entire value of A
# last output only depends on first (most significant) digit of A
# -> find most significant digit first, then iterate


@watch.measure_time
def solve2(data):
    register_orig, program = data
    # print(program)
    digits_candidates = [""]  # not every digit must be unambiguous -- keep track of possibilities
    for i, expected_output in enumerate(reversed(program)):
        # print(f"trying to find the {i}. digit with {expected_output=}")
        new_digit_candidates = []
        for digits in digits_candidates:
            # print(f" trying with A={digits}")
            for digit in range(8):
                # print(f"  trying {digit}")
                register = register_orig | {"A": int(f"{digits}{digit}", base=8)}
                output = run(register, program)
                # print(f"   {output}")
                if output[0] == expected_output:
                    # only carry on with this `digits` if the output works with any new digit
                    new_digit_candidates.append(digits + str(digit))
                    # print(f" correct {i}. digit is {digit}")
        digits_candidates = new_digit_candidates
    # print(digits_candidates)  # -> interesting: the solution is not unique
    return int(digits_candidates[0], base=8)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

