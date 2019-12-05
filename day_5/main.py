#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
from typing import List
import argparse
import enum


Intcode = List[str]


@enum.unique
class Operation(enum.Enum):
    Add = 1
    Multiply = 2
    Halt = 99


class SingleCode:

    _OPERATION_STEP = 4
    _HALT_STEP = 0

    def __init__(
        self,
        op: Operation,
        first_adr: int,
        second_adr: int,
        target_adr: int,
    ) -> None:
        self.operation = op
        self.first_value_adress = first_adr
        self.second_value_adress = second_adr
        self.target_adress = target_adr

    @classmethod
    def from_intcode(cls, intcode_slice: Intcode):
        op = Operation(int(intcode_slice[0]))
        if op == Operation.Halt:
            return cls(op, 0, 0, 0)
        first_adr = int(intcode_slice[1])
        second_adr = int(intcode_slice[2])
        target_adr = int(intcode_slice[3])
        return cls(op, first_adr, second_adr, target_adr)

    def execute(self, intcode: Intcode) -> int:
        if self.operation == Operation.Add:
            intcode[self.target_adress] = str(
                int(intcode[self.first_value_adress])
                + int(intcode[self.second_value_adress])
            )
            return self._OPERATION_STEP
        if self.operation == Operation.Multiply:
            intcode[self.target_adress] = str(
                int(intcode[self.first_value_adress])
                * int(intcode[self.second_value_adress])
            )
            return self._OPERATION_STEP
        return self._HALT_STEP


def init_intcode(intcode: Intcode, state='1202') -> None:
    intcode[1] = str(int(state[0:2]))
    intcode[2] = str(int(state[2:4]))


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

    init_intcode(intcode)

    step: int = 0
    position: int = 0
    code: SingleCode = SingleCode.from_intcode(intcode[position:position+4])

    while code.operation != Operation.Halt:
        step = code.execute(intcode)
        position += step
        try:
            code = SingleCode.from_intcode(intcode[position:position+4])
        except IndexError:
            code = SingleCode.from_intcode(intcode[position])

    print(intcode[0])
