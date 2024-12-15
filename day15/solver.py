#!/usr/bin/env python

from pathlib import Path
from copy import copy
import rich
from aoc import utils
from aoc.geometry import Vec, Direction

watch = utils.stopwatch()


@watch.measure_time
def parse(raw_data):
    upper, lower = raw_data.split("\n\n")
    walls = {}
    boxes = []
    for pos, char in utils.str_to_grid_dict(upper).items():
        if char == "#":
            walls[Vec(*pos)] = char
        elif char == "O":
            boxes.append(Vec(*pos))
        elif char == "@":
            robot = Vec(*pos)
    directions = {
        "^": Direction.N,
        ">": Direction.E,
        "v": Direction.S,
        "<": Direction.W,
    }
    movements = [directions[c] for c in lower.replace("\n", "")]
    return walls, boxes, robot, movements 


def try_moving(walls, boxes, item, dir):
    """tries to move item in dir. returns lists of new positions"""
    moved_so_far = []

    def _try_moving(item):
        if item + dir in walls:
            return []  # if at any point we can't move, nothing moves
        i = boxes.index(item)
        moved_so_far.append((i, item + dir))
        if item + dir in boxes:
            return _try_moving(item + dir)
        return moved_so_far     

    return _try_moving(item)


@watch.measure_time
def solve1(data):
    # rich.print(data)
    walls, boxes, robot, movements = data
    boxes = copy(boxes)
    for dir in movements:
        new_robot = robot + dir
        if new_robot in walls:
            continue
        elif new_robot in boxes:
            new_boxpos = try_moving(walls, boxes, new_robot, dir)
            if new_boxpos:
                robot = new_robot
                for i, pos in new_boxpos:
                    boxes[i] = pos
        else:
            robot = new_robot
    
    # print(utils.dictgrid_to_str(
    #     walls | {b: "o" for b in boxes} | {robot: "@"},
    #     keybuilder=Vec,
    #     empty="."
    # ))
    result = 0
    for box in boxes:
        result += 100 * box.y + box.x
    return result


@watch.measure_time
def parse2(raw_data):
    raw_data = raw_data.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
    upper, lower = raw_data.split("\n\n")
    walls = {}
    boxes = []
    for pos, char in utils.str_to_grid_dict(upper).items():
        if char == "#":
            walls[Vec(*pos)] = char
        elif char == "[":
            boxes.append((Vec(*pos), Vec(*pos) + Direction.E))
        elif char == "@":
            robot = Vec(*pos)
    directions = {
        "^": Direction.N,
        ">": Direction.E,
        "v": Direction.S,
        "<": Direction.W,
    }
    movements = [directions[c] for c in lower.replace("\n", "")]
    return walls, boxes, robot, movements 


def try_moving2(walls, boxes, item, dir):
    """tries to move item in dir. returns lists of new positions"""
    moved_so_far = []

    def _try_moving(item):
        if any(b + dir in walls for b in item):
            return []  # if at any point we can't move, nothing moves

        i = boxes.index(item)
        moved_item = tuple(b + dir for b in item)
        moved_so_far.append((i, moved_item))
        hit_boxes = []
        for box in boxes:
            if box == item:
                continue
            if any(b in box for b in moved_item):
                hit_boxes.append(box)
        
        if hit_boxes:
            moved = []
            for hit_box in hit_boxes:
                _moved = _try_moving(hit_box)
                if not _moved:
                    return []
                else:
                    moved += _moved
            return _moved
        return moved_so_far     

    return _try_moving(item)


@watch.measure_time
def solve2(data):
    # rich.print(data)
    walls, boxes, robot, movements = data
    boxes = copy(boxes)
    # print(boxes)
    for dir in movements:
        # print(dir)
        new_robot = robot + dir
        if new_robot in walls:
            continue
        box_hit = None
        for box in boxes:
            if new_robot in box:
                box_hit = box
                break
        if box_hit:
            new_boxpos = try_moving2(walls, boxes, box_hit, dir)
            # print(new_boxpos)
            if new_boxpos:
                robot = new_robot
                for i, pos in new_boxpos:
                    boxes[i] = pos
        else:
            robot = new_robot

        # print(utils.dictgrid_to_str(
        #     walls | {b: "[" for b,_ in boxes} | {b: "]" for _,b in boxes} | {robot: "@"},
        #     keybuilder=Vec,
        #     empty="."
        # ))

    result = 0
    for box in boxes:
        result += 100 * box[0].y + box[0].x
    return result


if __name__ == "__main__":
    raw = open(Path(__file__).parent / "input.txt").read().strip()
    print(f"Part 1: {solve1(parse(raw))}")
    print(f"Part 2: {solve2(parse2(raw))}")
    print()
    watch.print_times()

