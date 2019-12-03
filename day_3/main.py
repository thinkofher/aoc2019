#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
from typing import NamedTuple, List, Set
import sys

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


class Instruction(NamedTuple):
    direction: int
    length: int


class InstructionBuilder:
    direction: int
    length: int

    def __init__(self, instruction_str: str):
        self.direction = self._transcript_direction(instruction_str[0])
        self.length = int(instruction_str[1:])

    def build(self) -> Instruction:
        return Instruction(self.direction, self.length)

    @staticmethod
    def _transcript_direction(direction: str) -> int:
        if direction == "R":
            return RIGHT
        if direction == "L":
            return LEFT
        if direction == "U":
            return UP
        if direction == "D":
            return DOWN


class Point(NamedTuple):
    x: int
    y: int


Wire = Set[Point]
Wires = List[Wire]
Instructions = List[Instruction]


def manhattan_distance(origin: Point, target: Point):
    return abs(target.x - origin.x) + abs(target.y - origin.y)


def execute_instructions(instructions: Instructions) -> Wire:
    last_point = Point(0, 0)
    wire: Wire = set()

    for instruction in instructions:
        for position in range(1, instruction.length+1):
            if instruction.direction == LEFT:
                new_point = Point(last_point.x - position, last_point.y)
                wire.add(new_point)

            if instruction.direction == RIGHT:
                new_point = Point(last_point.x + position, last_point.y)
                wire.add(new_point)

            if instruction.direction == UP:
                new_point = Point(last_point.x, last_point.y + position)
                wire.add(new_point)

            if instruction.direction == DOWN:
                new_point = Point(last_point.x, last_point.y - position)
                wire.add(new_point)
        last_point = new_point
    return wire


if __name__ == "__main__":
    instructions: Instructions = []
    wires: Wires = []
    for lines in sys.stdin:
        for line in lines.split('\n\n'):
            for instruction_str in line.replace('\n', '').split(','):
                instructions.append(
                    InstructionBuilder(instruction_str).build()
                )
            wires.append(execute_instructions(instructions))
            instructions: Instructions = []

    intersection: Set[Point] = wires[0]
    for points in wires[1:]:
        intersection = intersection.intersection(points)

    origin = Point(0, 0)
    ans = min([manhattan_distance(origin, point) for point in intersection])
    print(ans)
