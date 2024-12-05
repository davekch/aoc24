#!/usr/bin/env python

from dataclasses import dataclass
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    upper, lower = raw_data.split("\n\n")
    rules = list(map(utils.ints, upper.splitlines()))
    updates = list(map(utils.ints, lower.splitlines()))
    # sort into correct and uncorrect updates so that we don't have to check the correct updates twice
    sorted_updates = {
        "correct": [],
        "incorrect": []
    }
    for update in updates:
        if all([check(update, r) for r in rules]):
            sorted_updates["correct"].append(update)
        else:
            sorted_updates["incorrect"].append(update)        
    return rules, sorted_updates


def check(update: list, rule):
    first, second = rule
    if not (first in update and second in update):
        return True
    return update.index(first) < update.index(second)


@watch.measure_time
def solve1(data):
    rules, updates = data
    s = 0
    for update in updates["correct"]:
        s += update[len(update) // 2]
    return s


def sort_by_rule(update: list, rules: list):
    sorted_update = update[:]
    while not all([check(sorted_update, r) for r in rules]):
        # for each rule that is not yet satisfied, swap the offenders
        for first, second in rules:
            if first in sorted_update and second in sorted_update:
                first_index = sorted_update.index(first)
                second_index = sorted_update.index(second)
                if first_index > second_index:
                    sorted_update[first_index], sorted_update[second_index] = sorted_update[second_index], sorted_update[first_index]
    return sorted_update


@watch.measure_time
def solve2(data):
    rules, updates = data
    s = 0
    for update in updates["incorrect"]:
        sorted_update = sort_by_rule(update, rules)
        s += sorted_update[len(sorted_update) // 2]
    return s


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

