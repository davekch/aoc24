#!/usr/bin/env python

from pathlib import Path
import math
from copy import copy
from collections import defaultdict
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


def investigate_output_patterns(data):
    register_backup, program = data
    out_sequence = defaultdict(list)
    A = 0
    for A in range(5000):
        register = copy(register_backup)
        register["A"] = A
        output = run(register, program)
        for i, o in enumerate(output):
            out_sequence[i].append(o)

    import matplotlib.pyplot as plt
    for i, seq in out_sequence.items():
        plt.plot(seq, label=str(i))
    plt.legend()
    plt.savefig("outsequences.png")


def solve2_numba(data):
    import numba as nb
    import numpy as np

    # the input program is
    # 2,4: write lowest three bits of A to B
    # 1,1: xor that with 1 (flip lowest bit)
    # 7,5: write floor(A / 2**B) to C
    # 0,3: write floor(A / 2**3) to A
    # 1,4: xor B with 4 (flip first bit?)
    # 4,0: xor B with C and write to B
    # 5,5: write lowest three bits of B to output
    # 3,0: loop until A == 0

    @nb.njit(parallel=True)
    def get_A(program):
        program_len = len(program)
        result = nb.typed.List([0])
        for A in nb.prange(1, np.int64(1e15)):
            if A % 1000000 == 0:
                print(A)
            if result[0] != 0:
                continue
            B = np.int32(0)
            C = np.int32(0)
            output_i = np.int32(0)
            while A != 0:
                B = np.int32(A % 8) ^ 1
                C = math.floor(A / 2**B)
                A = math.floor(A / 8)
                B = B ^ 4
                B = B ^ C
                # output is B % 8
                if program[output_i] == np.int32(B % 8):
                    if output_i == program_len - 1:
                        result[0] = A
                    else:
                        output_i += 1
                else:
                    break
        return result[0]

    _, program = data
    program = np.array(program, dtype=np.int32)
    return get_A(program)


@watch.measure_time
def solve2(data):
    return solve2_numba(data)


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

