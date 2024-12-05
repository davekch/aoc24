#!/usr/bin/env python

from collections import defaultdict
from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    upper, lower = raw_data.split("\n\n")
    updates = list(map(utils.ints, lower.splitlines()))
    rules = defaultdict(list)
    for line in upper.splitlines():
        first, second = utils.ints(line)
        rules[first].append(second)

    # sort into correct and uncorrect updates so that we don't have to check the correct updates twice
    sorted_updates = {
        "correct": [],
        "incorrect": []
    }
    for update in updates:
        if check(update, rules):
            sorted_updates["correct"].append(update)
        else:
            sorted_updates["incorrect"].append(update)        
    return rules, sorted_updates


def check(update, rules):
    for i, page in enumerate(update):
        for later in rules[page]:
            if later in update and update.index(later) < i:
                return False
    return True


@watch.measure_time
def solve1(data):
    rules, updates = data
    s = 0
    for update in updates["correct"]:
        s += update[len(update) // 2]
    return s


def sort_by_rule(update: list, rules: list):
    sorted_update = update[:]
    while not check(sorted_update, rules):
        # for each rule that is not yet satisfied, swap the offenders
        for first in update:
            for second in rules[first]:
                if second in sorted_update:
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

