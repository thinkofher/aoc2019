#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
import argparse
from typing import List

from computer import AmplifierControllerSoftware

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solution for the 5th day of Advent of Code.",
    )
    parser.add_argument(
        "filename",
        metavar="f",
        type=str,
        help="name of the file with input data",
    )
    args = parser.parse_args()

    intcode = []  # type: List[str]
    with open(args.filename, "r") as f:
        for line in f.readlines():
            intcode += line.strip("\n").split(",")

    acs = AmplifierControllerSoftware(intcode)
    acs.run_software()
    print(acs.get_max_signal())
