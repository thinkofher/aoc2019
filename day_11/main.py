#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
import argparse
from typing import List, Dict

from computer import IntcodeComputer
from robot import Robot, Point, Color


def visualize_table(table: Dict[Point, Color]) -> None:
    max_x = max(map(lambda p: p.x, table.keys()))
    min_x = min(map(lambda p: p.x, table.keys()))
    max_y = max(map(lambda p: p.y, table.keys()))
    min_y = min(map(lambda p: p.y, table.keys()))

    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            color = Color.Black
            try:
                color = table[Point(x, y)]
            except KeyError:
                pass

            if color == Color.White:
                print('#', end='')
            else:
                print(' ', end='')
        print('\n', end='')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solution for the 11th day of Advent of Code.",
    )
    parser.add_argument(
        "filename", type=str, help="name of the file with input data",
    )
    parser.add_argument(
        "default_color",
        type=str,
        help="set default color",
        choices=["black", "white"],
    )
    args = parser.parse_args()

    intcode = []  # type: List[str]
    with open(args.filename, "r") as f:
        for line in f.readlines():
            intcode += line.strip("\n").split(",")

    if args.default_color == "black":
        default_color = Color.Black
    else:
        default_color = Color.White

    robot = Robot(default_color=default_color)
    computer = IntcodeComputer(intcode)
    computer.io_wrapper = robot
    computer.compute_all()

    print('Robot did', len(robot.table.items()), 'operations.', end='\n'*2)
    visualize_table(robot.table)
