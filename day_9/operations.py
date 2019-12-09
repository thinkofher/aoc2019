import enum


@enum.unique
class Operation(enum.Enum):
    Add = 1
    Multiply = 2
    Input = 3
    Output = 4
    JumpIfTrue = 5
    JumpIfFalse = 6
    LessThan = 7
    Equals = 8
    Halt = 99


@enum.unique
class Parameters(enum.Enum):
    Position = 0
    Immediate = 1
    Relative = 2
