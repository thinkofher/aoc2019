from typing import Tuple

from handler import IOHandler
from operations import (
    Operation,
    OperationType,
    SingleParameter,
    TwoParameters,
    ThreeParametrs,
)
from values import WrappedValue, Modes, Intcode
from memory import IntcodeMemory


def wrap_values(
    modes: Modes, values: Tuple[int, ...], relative_base: int
) -> Tuple[WrappedValue, ...]:
    return tuple(
        WrappedValue(parameter, value, relative_base)
        for parameter, value in zip(modes.parameters, values)
    )


class SingleCode:

    instruction_pointer: int
    _OPERATION_STEP = 4
    _JUMP_STEP = 3
    _INPUT_OUTPUT_STEP = 2
    _ADJUST_REL_BASE_STEP = 2
    _HALT_STEP = 0

    def __init__(
        self,
        op: Operation,
        first: WrappedValue,
        second: WrappedValue,
        target: WrappedValue,
    ) -> None:
        self.operation = op
        self.first_value = first
        self.second_value = second
        self.target_adress = target

    @classmethod
    def from_intcode(
        cls, intcode_slice: Intcode, relative_base: int
    ) -> "SingleCode":
        modes = Modes.from_intcode(intcode_slice)
        values: Tuple[int, ...] = tuple(map(int, intcode_slice[1:]))

        if modes.opcode == Operation.Halt:
            return cls._halt_code(modes)

        if modes.opcode in ThreeParametrs:
            return cls._three_parameters_code(modes, values, relative_base)

        if modes.opcode in TwoParameters:
            return cls._two_parameters_code(modes, values, relative_base)

        if modes.opcode in SingleParameter:
            return cls._single_parameter_code(modes, values[0], relative_base)

        raise ValueError(f"Bad operation: {modes.opcode}.")

    @classmethod
    def _halt_code(cls, modes: Modes) -> "SingleCode":
        return cls(
            modes.opcode,
            WrappedValue.empty(),
            WrappedValue.empty(),
            WrappedValue.empty(),
        )

    @classmethod
    def _single_parameter_code(
        cls, modes: Modes, value: int, relative_base: int
    ) -> "SingleCode":
        return cls(
            modes.opcode,
            WrappedValue.empty(),
            WrappedValue.empty(),
            WrappedValue(modes.parameters[0], value, relative_base),
        )

    @classmethod
    def _two_parameters_code(
        cls, modes: Modes, values: Tuple[int, ...], relative_base: int
    ) -> "SingleCode":
        wrapped_values = wrap_values(modes, values, relative_base)
        wrapped_values += (WrappedValue.empty(),)  # add empty value

        return cls(modes.opcode, *wrapped_values,)

    @classmethod
    def _three_parameters_code(
        cls, modes: Modes, values: Tuple[int, ...], relative_base: int
    ) -> "SingleCode":
        wrapped_values = wrap_values(modes, values, relative_base)
        return cls(modes.opcode, *wrapped_values)

    def execute(
        self, intcode_memory: IntcodeMemory, io_handler: IOHandler
    ) -> int:

        if self.operation == Operation.Add:
            return self._add(intcode_memory)
        if self.operation == Operation.Multiply:
            return self._multiply(intcode_memory)
        if self.operation == Operation.JumpIfTrue:
            return self._jumpt_if_true(intcode_memory)
        if self.operation == Operation.JumpIfFalse:
            return self._jump_if_false(intcode_memory)
        if self.operation == Operation.LessThan:
            return self._less_than(intcode_memory)
        if self.operation == Operation.Equals:
            return self._equals(intcode_memory)
        if self.operation == Operation.Input:
            return self._input(intcode_memory, io_handler)
        if self.operation == Operation.Output:
            return self._output(intcode_memory, io_handler)
        if self.operation == Operation.AdjustBase:
            return self._adjust_relative_base(intcode_memory, io_handler)
        if self.operation == Operation.Halt:
            return self._HALT_STEP

        raise ValueError(f"There is no operation like {self.operation}")

    def _calc_first_value(self, mem: IntcodeMemory) -> int:
        return self.first_value.get_value(mem, OperationType.Read)

    def _calc_second_value(self, mem: IntcodeMemory) -> int:
        return self.second_value.get_value(mem, OperationType.Read)

    def _read_target_adress(self, mem: IntcodeMemory) -> int:
        return self.target_adress.get_value(mem, OperationType.Read)

    def _write_target_adress(self, mem: IntcodeMemory) -> int:
        return self.target_adress.get_value(mem, OperationType.Write)

    def _add(self, mem: IntcodeMemory) -> int:
        mem[self._write_target_adress(mem)] = str(
            self._calc_first_value(mem) + self._calc_second_value(mem)
        )
        return self._OPERATION_STEP + self.instruction_pointer

    def _multiply(self, mem: IntcodeMemory) -> int:
        mem[self._write_target_adress(mem)] = str(
            self._calc_first_value(mem) * self._calc_second_value(mem)
        )
        return self._OPERATION_STEP + self.instruction_pointer

    def _input(self, mem: IntcodeMemory, io_handler: IOHandler) -> int:
        input_value = io_handler.get_input()
        mem[self._write_target_adress(mem)] = str(input_value)
        return self._INPUT_OUTPUT_STEP + self.instruction_pointer

    def _output(self, mem: IntcodeMemory, io_handler: IOHandler) -> int:
        value_to_output = self._read_target_adress(mem)
        io_handler.set_output(value_to_output)
        return self._INPUT_OUTPUT_STEP + self.instruction_pointer

    def _jumpt_if_true(self, mem: IntcodeMemory) -> int:
        if self.first_value.get_value(mem, OperationType.Read) != 0:
            return self.second_value.get_value(mem, OperationType.Read)
        return self._JUMP_STEP + self.instruction_pointer

    def _jump_if_false(self, mem: IntcodeMemory) -> int:
        if self._calc_first_value(mem) == 0:
            return self._calc_second_value(mem)
        return self._JUMP_STEP + self.instruction_pointer

    def _less_than(self, mem: IntcodeMemory) -> int:
        first = self._calc_first_value(mem)
        second = self._calc_second_value(mem)
        adress = self._write_target_adress(mem)

        if first < second:
            mem[adress] = str(1)
        else:
            mem[adress] = str(0)
        return self._OPERATION_STEP + self.instruction_pointer

    def _equals(self, mem: IntcodeMemory) -> int:
        first = self._calc_first_value(mem)
        second = self._calc_second_value(mem)
        adress = self._write_target_adress(mem)

        if first == second:
            mem[adress] = str(1)
        else:
            mem[adress] = str(0)
        return self._OPERATION_STEP + self.instruction_pointer

    def _adjust_relative_base(
        self, mem: IntcodeMemory, io_handler: IOHandler
    ) -> int:
        io_handler.relative_base_adjust_value = self._read_target_adress(mem)
        return self._ADJUST_REL_BASE_STEP + self.instruction_pointer
