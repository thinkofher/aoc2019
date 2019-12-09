from typing import Tuple

from handler import IOHandler
from operations import Operation, Parameters
from values import WrappedValue, Modes, Intcode


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

    def execute(self, intcode: Intcode, io_handler: IOHandler) -> int:

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
            return self._input(intcode, io_handler)
        if self.operation == Operation.Output:
            return self._output(intcode, io_handler)
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

    def _input(self, intcode: Intcode, io_handler: IOHandler) -> int:
        input_value = io_handler.get_input()
        intcode[self.target_adress] = str(input_value)
        return self._INPUT_OUTPUT_STEP + self.instruction_pointer

    def _output(self, intcode: Intcode, io_handler: IOHandler) -> int:
        value_to_output = int(intcode[self.target_adress])
        io_handler.set_output(value_to_output)
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
