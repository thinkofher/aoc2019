#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
import argparse
from typing import List

from computer import (
    AmplifierControllerSoftware,
    AmplifiersFeedbackLoopSoftware,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solution for the 7th day of Advent of Code.",
    )
    parser.add_argument(
        "filename",
        type=str,
        help="name of the file with input data",
    )
    parser.add_argument(
        "software",
        type=str,
        help="name of the software to run on intcode computer (acs/acsl)",
        choices=["acs", "acsl"],
    )
    args = parser.parse_args()

    intcode = []  # type: List[str]
    with open(args.filename, "r") as f:
        for line in f.readlines():
            intcode += line.strip("\n").split(",")

    if args.software == "acs":
        acs = AmplifierControllerSoftware(intcode)
        acs.run_software()
        print(acs.get_max_signal())

    if args.software == "acsl":
        acsl = AmplifiersFeedbackLoopSoftware(intcode)
        acsl.run_software()
        print(acsl.get_max_signal())
