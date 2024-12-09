#!/usr/bin/env python

from pathlib import Path
from aoc import utils

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    digits = [int(d) for d in raw_data.strip()]
    files = digits[::2]
    free = digits[1::2]
    return files, free


@watch.measure_time
def solve1(data):
    files, free = data
    current_id = 0
    current_free = 0
    dismantling_id = len(files) - 1
    left = {i: l for i, l in enumerate(files)}
    left_free = {i: f for i, f in enumerate(free)}
    blockpos = 0
    checksum = 0
    while not all(v == 0 for v in left.values()):
        if left[current_id]:
            left[current_id] -= 1
            checksum += blockpos * current_id
        else:
            # we are done with current_id, fill up free space if there is some
            if left_free[current_free]:
                if not left[dismantling_id]:
                    dismantling_id -=1
                left[dismantling_id] -= 1
                left_free[current_free] -= 1
                checksum += blockpos * dismantling_id
            else:
                # current file is done moving + there is no free space, move to next file
                current_free += 1
                current_id += 1
                continue
        
        blockpos += 1
    return checksum


@watch.measure_time
def solve2(data):
    files, free = data
    left = {i: l for i, l in enumerate(files)}
    free = {
        i: {"left": f, "occupied": {}} for i, f in enumerate(free)
    }
    free[len(files)-1] = {"left": 0, "occupied": {}}
    # rearrange
    for i in reversed(range(len(files))):
        # if i == 4:
        #     break
        free_slots = [j for j in free if j < i and free[j]["left"] >= files[i]]
        if not free_slots:
            continue
        slot = min(free_slots)
        free[slot]["occupied"][i] = files[i]
        free[slot]["left"] -= files[i]
        free[i-1]["left"] += files[i]
        left[i] = 0
    
    checksum = 0
    blockpos = 0
    # layout = ""
    for i in left:
        # first what's left from the original files
        for _ in range(left[i]):
            checksum += blockpos * i
            blockpos += 1
            # layout += str(i)
        # now the originally free space
        for j, l in free[i]["occupied"].items():
            for _ in range(l):
                checksum += blockpos * j
                blockpos += 1
                # layout += str(j)
        # skip still free space
        blockpos += free[i]["left"]
        # layout += free[i]["left"] * "."

    # print(layout)
    return checksum


if __name__ == "__main__":
    data = parse(open(Path(__file__).parent / "input.txt").read().strip())
    print(f"Part 1: {solve1(data)}")
    print(f"Part 2: {solve2(data)}")
    print()
    watch.print_times()

