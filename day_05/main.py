#!/usr/bin/env python
# Beniamin Dudek <beniamin.dudek@yahoo.com, github.com/thinkofher>
from typing import List, NamedTuple, Tuple
import argparse
import enum


Intcode = List[str]


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


class Modes(NamedTuple):
    opcode: Operation
    parameters: Tuple[Parameters, ...]

    @classmethod
    def from_intcode(cls, intcode_slice: Intcode):
        opcode_str: str = intcode_slice[0]

        # opcode (operation) is in the two last element of string
        opcode: int = int(opcode_str[-2:])

        additional_values: int = 0

        if opcode in [1, 2, 7, 8]:
            additional_values = 3
        elif opcode in [5, 6]:
            additional_values = 2
        elif opcode in [3, 4]:
            additional_values = 1
        elif opcode == 99:
            pass
        else:
            raise ValueError(
                f"Opcode ({opcode}) can only be 1, 2, 3, 4, 5, 6, 7, 8 or 99."
            )

        values_parameters: List[int] = list(map(int, opcode_str[:-2]))
        values_parameters.reverse()
        # add zeros omitted due to being a leading zero
        values_parameters += (additional_values - len(values_parameters)) * [0]

        return cls(
            Operation(opcode), tuple(map(Parameters, values_parameters))
        )


class WrappedValue(NamedTuple):
    mode: Parameters
    value: int

    def get_value(self, intcode: Intcode) -> int:
        if self.mode == Parameters.Position:
            return int(intcode[self.value])
        else:
            return self.value


class SingleCode:

    instruction_pointer: int
    _OPERATION_STEP = 4
    _JUMP_STEP = 3
    _INPUT_OUTPUT_STEP = 2
    _HALT_STEP = 0

    def __init__(
        self,
        op: Operation,
        first: WrappedValue,
        second: WrappedValue,
        target: int,
    ) -> None:
        self.operation = op
        self.first_value = first
        self.second_value = second
        self.target_adress = target

    @classmethod
    def from_intcode(cls, intcode_slice: Intcode):
        modes = Modes.from_intcode(intcode_slice)

        values: Tuple[int, ...] = tuple(map(int, intcode_slice[1:]))

        if modes.opcode == Operation.Halt:
            return cls(
                modes.opcode,
                WrappedValue(Parameters.Position, 0),
                WrappedValue(Parameters.Position, 0),
                0,
            )
        if modes.opcode in [
            Operation.Add,
            Operation.Multiply,
            Operation.LessThan,
            Operation.Equals,
        ]:
            wrapped_values: Tuple[WrappedValue, ...] = tuple(
                WrappedValue(parameter, value)
                for parameter, value in zip(modes.parameters, values)
            )
            return cls(
                modes.opcode,
                wrapped_values[0],
                wrapped_values[1],
                wrapped_values[2].value,
            )
        if modes.opcode in [Operation.JumpIfTrue, Operation.JumpIfFalse]:
            wrapped_values = tuple(
                WrappedValue(parameter, value)
                for parameter, value in zip(modes.parameters, values)
            )
            return cls(modes.opcode, wrapped_values[0], wrapped_values[1], 0)

        if modes.opcode in [Operation.Input, Operation.Output]:
            return cls(
                modes.opcode,
                WrappedValue(Parameters.Position, 0),
                WrappedValue(Parameters.Position, 0),
                values[0],
            )

        raise ValueError(f"Bad operation: {modes.opcode}.")

    def execute(self, intcode: Intcode) -> int:

        if self.operation == Operation.Add:
            return self._add(intcode)
        if self.operation == Operation.Multiply:
            return self._multiply(intcode)
        if self.operation == Operation.JumpIfTrue:
            return self._jumpt_if_true(intcode)
        if self.operation == Operation.JumpIfFalse:
            return self._jump_if_false(intcode)
        if self.operation == Operation.LessThan:
            return self._less_than(intcode)
        if self.operation == Operation.Equals:
            return self._equals(intcode)
        if self.operation == Operation.Input:
            return self._input(intcode)
        if self.operation == Operation.Output:
            return self._output(intcode)
        if self.operation == Operation.Halt:
            return self._HALT_STEP

        raise ValueError(f"There is no operation like {self.operation}")

    def _add(self, intcode: Intcode) -> int:
        intcode[self.target_adress] = str(
            self.first_value.get_value(intcode)
            + self.second_value.get_value(intcode)
        )
        return self._OPERATION_STEP + self.instruction_pointer

    def _multiply(self, intcode: Intcode) -> int:
        intcode[self.target_adress] = str(
            self.first_value.get_value(intcode)
            * self.second_value.get_value(intcode)
        )
        return self._OPERATION_STEP + self.instruction_pointer

    def _input(self, intcode: Intcode) -> int:
        input_value = int(input("Provide input: "))
        intcode[self.target_adress] = str(input_value)
        return self._INPUT_OUTPUT_STEP + self.instruction_pointer

    def _output(self, intcode: Intcode) -> int:
        value_to_output = intcode[self.target_adress]
        print(f"Output value: {value_to_output}")
        return self._INPUT_OUTPUT_STEP + self.instruction_pointer

    def _jumpt_if_true(self, intcode: Intcode) -> int:
        if self.first_value.get_value(intcode) != 0:
            return self.second_value.get_value(intcode)
        return self._JUMP_STEP + self.instruction_pointer

    def _jump_if_false(self, intcode: Intcode) -> int:
        if self.first_value.get_value(intcode) == 0:
            return self.second_value.get_value(intcode)
        return self._JUMP_STEP + self.instruction_pointer

    def _less_than(self, intcode: Intcode) -> int:
        if self.first_value.get_value(intcode) < self.second_value.get_value(
            intcode
        ):
            intcode[self.target_adress] = str(1)
        else:
            intcode[self.target_adress] = str(0)
        return self._OPERATION_STEP + self.instruction_pointer

    def _equals(self, intcode: Intcode) -> int:
        if self.first_value.get_value(intcode) == self.second_value.get_value(
            intcode
        ):
            intcode[self.target_adress] = str(1)
        else:
            intcode[self.target_adress] = str(0)
        return self._OPERATION_STEP + self.instruction_pointer


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

    step: int = 0
    global_instruction_pointer: int = 0
    code: SingleCode = SingleCode.from_intcode(
        intcode[global_instruction_pointer:global_instruction_pointer + 4]
    )
    code.instruction_pointer = global_instruction_pointer

    while code.operation != Operation.Halt:
        global_instruction_pointer = code.execute(intcode)
        code = SingleCode.from_intcode(
            intcode[global_instruction_pointer:global_instruction_pointer + 4]
        )
        code.instruction_pointer = global_instruction_pointer
