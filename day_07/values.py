from typing import NamedTuple, Tuple, List

from operations import Operation, Parameters

Intcode = List[str]
ImmutableIntcode = Tuple[str, ...]


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
