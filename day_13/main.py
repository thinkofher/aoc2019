#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
import argparse
import sys
from typing import List


from computer import IntcodeComputer
from game import IOGame, IOGameBot, Tile


BOT = "bot"
PLAYER = "player"
SPEED_MULTIPLIER = 10


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Solution for the 11th day of Advent of Code.",
    )
    parser.add_argument(
        "filename", type=str, help="name of the file with input data",
    )
    parser.add_argument("--first", dest="solve_first", action="store_true")
    parser.add_argument("--second", dest="solve_first", action="store_false")
    parser.add_argument(
        "--game",
        type=str,
        help="choose game mode. default is bot",
        default="bot",
        choices=[BOT, PLAYER],
    )
    parser.add_argument(
        "--bot-speed",
        dest='speed',
        type=int,
        help="1 - slowest, ..., 5 - fastest. default is 5",
        default=5,
        choices=[1, 2, 3, 4, 5],
    )
    args = parser.parse_args()

    intcode: List[str] = []
    with open(args.filename, "r") as f:
        for line in f.readlines():
            intcode += line.strip("\n").split(",")

    computer = IntcodeComputer(intcode)

    if args.solve_first:
        computer.io_wrapper = IOGame()
        computer.compute_all()
        print(
            len(
                list(
                    filter(
                        lambda tile: tile == Tile.Block,
                        computer.io_wrapper.tiles.values(),
                    )
                )
            )
        )
        sys.exit(0)

    try:
        intcode[0] = "2"  # game mode
        if args.game == BOT:
            computer.io_wrapper = IOGameBot(1/(SPEED_MULTIPLIER*args.speed))
            computer.compute_all()
            print(f"Final score: {computer.io_wrapper.score}")
            sys.exit(0)

        if args.game == PLAYER:
            computer.io_wrapper = IOGame()
            computer.compute_all()
            print(f"Final score: {computer.io_wrapper.score}")
            sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(0)
