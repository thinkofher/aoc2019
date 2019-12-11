from typing import NamedTuple, Tuple, List

from operations import Operation, OperationType, Parameters
from memory import IntcodeMemory, Intcode


class Modes(NamedTuple):
    opcode: Operation
    parameters: Tuple[Parameters, ...]

    @classmethod
    def from_intcode(cls, intcode_slice: Intcode) -> "Modes":
        opcode_str: str = intcode_slice[0]

        # opcode (operation) is in the two last element of string
        opcode: int = int(opcode_str[-2:])

        additional_values: int = 0

        if opcode in [1, 2, 7, 8]:
            additional_values = 3
        elif opcode in [5, 6]:
            additional_values = 2
        elif opcode in [3, 4, 9]:
            additional_values = 1
        elif opcode == 99:
            pass
        else:
            raise ValueError(
                f"Opcode ({opcode}) can only be 1, 2, 3, 4, 5, 6, 7, 8, 9 or 99."
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
    relative_base: int

    @classmethod
    def empty(cls) -> "WrappedValue":
        return cls(Parameters(0), 0, 0)

    def get_value(
        self, intcode_memory: IntcodeMemory, operation_type: OperationType
    ) -> int:
        if operation_type == OperationType.Read:
            return self._handle_read_operation(intcode_memory)
        if operation_type == OperationType.Write:
            return self._handle_write_operation(intcode_memory)

        raise ValueError("There is no such an operation type.")

    def _handle_read_operation(self, intcode_memory: IntcodeMemory) -> int:
        if self.mode == Parameters.Position:
            return int(intcode_memory[self.value])
        if self.mode == Parameters.Immediate:
            return self.value
        if self.mode == Parameters.Relative:
            return int(intcode_memory[self.value + self.relative_base])

        raise ValueError("There is no such a mode.")

    def _handle_write_operation(self, intcode_memory: IntcodeMemory) -> int:
        if self.mode in (Parameters.Position, Parameters.Immediate):
            return self.value
        if self.mode == Parameters.Relative:
            return self.value + self.relative_base

        raise ValueError("There is no such a mode.")
