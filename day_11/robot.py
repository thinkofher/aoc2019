import enum
from typing import NamedTuple, Dict

from handler import IOHandler


class Point(NamedTuple):
    x: int
    y: int


@enum.unique
class Color(enum.IntEnum):
    Black = 0
    White = 1


@enum.unique
class Instruction(enum.IntEnum):
    TurnLeft = 0
    TurnRight = 1


@enum.unique
class Direction(enum.IntEnum):
    North = 0
    East = 1
    South = 2
    West = 3


class Command(NamedTuple):
    color: Color
    instruction: Instruction


def turn(dir: Direction, instr: Instruction):
    if dir == Direction.North:
        if instr == Instruction.TurnLeft:
            return Direction.West
        else:
            return Direction.East

    elif dir == Direction.East:
        if instr == Instruction.TurnLeft:
            return Direction.North
        else:
            return Direction.South

    elif dir == Direction.South:
        return turn(Direction.North, Instruction(not instr))

    else:
        return turn(Direction.East, Instruction(not instr))


class Robot(IOHandler):
    table: Dict[Point, Color]
    position: Point
    direction: Direction
    color: Color
    _default_color: Color

    def __init__(self, default_color=Color.Black) -> None:
        self.output_values = []

        self.table = {}
        self.direction = Direction.North
        self.position = Point(0, 0)
        self._default_color = default_color
        self.color = self._default_color

    def get_input(self) -> int:
        try:
            return int(self.table[self.position])
        except KeyError:
            return int(self._default_color)

    def set_output(self, value: int) -> None:
        self.output_values.append(value)
        if len(self.output_values) == 2:
            command = Command(
                Color(self.output_values[0]),
                Instruction(self.output_values[1])
            )
            self.output_values = []
            self.load_command(command)
            self.paint()
            self.move()

    def load_command(self, c: Command) -> None:
        self.color = c.color
        self.direction = turn(self.direction, c.instruction)

    def paint(self):
        self.table[self.position] = self.color

    def move(self) -> None:
        curr_pos = self.position
        if self.direction == Direction.North:
            self.position = Point(curr_pos.x, curr_pos.y - 1)
        elif self.direction == Direction.South:
            self.position = Point(curr_pos.x, curr_pos.y + 1)
        elif self.direction == Direction.West:
            self.position = Point(curr_pos.x - 1, curr_pos.y)
        else:
            self.position = Point(curr_pos.x + 1, curr_pos.y)
