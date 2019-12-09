import enum
from typing import Tuple


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
    AdjustBase = 9
    Halt = 99


ThreeParametrs: Tuple[Operation, ...] = (
    Operation.Add,
    Operation.Multiply,
    Operation.LessThan,
    Operation.Equals,
)
TwoParameters: Tuple[Operation, ...] = (
    Operation.JumpIfTrue,
    Operation.JumpIfFalse,
)
SingleParameter: Tuple[Operation, ...] = (
    Operation.Input,
    Operation.Output,
    Operation.AdjustBase,
)


@enum.unique
class OperationType(enum.Enum):
    Read = 0
    Write = 1


@enum.unique
class Parameters(enum.Enum):
    Position = 0
    Immediate = 1
    Relative = 2
