#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
import argparse
from typing import List


from computer import IntcodeComputer
from game import IOGame


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solution for the 11th day of Advent of Code.",
    )
    parser.add_argument(
        "filename", type=str, help="name of the file with input data",
    )
    args = parser.parse_args()

    intcode = []  # type: List[str]
    with open(args.filename, "r") as f:
        for line in f.readlines():
            intcode += line.strip("\n").split(",")

    intcode[0] = '2'
    computer = IntcodeComputer(intcode)
    computer.io_wrapper = IOGame()
    computer.compute_all()
