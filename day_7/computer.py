from typing import List, Tuple
from itertools import permutations

from operations import Operation
from singlecode import SingleCode
from values import ImmutableIntcode, Intcode
from handler import IOHandler, StdIOWrapper, IOWrapper


class IntcodeComputer:

    _computer_instruction_ptr: int = 0

    init_intcode: ImmutableIntcode
    intcode: Intcode
    io_wrapper: IOHandler = StdIOWrapper()

    def __init__(self, intcode: Intcode) -> None:
        self.init_intcode = tuple(intcode)
        self.intcode = list(self.init_intcode[:])

    def reset_computer(self) -> None:
        self._step = 0
        self._computer_instruction_ptr = 0
        self.intcode = list(self.init_intcode[:])

    def compute_step(self) -> Operation:
        code: SingleCode = SingleCode.from_intcode(
            self.intcode[
                self._computer_instruction_ptr:self._computer_instruction_ptr
                + 4
            ]
        )
        code.instruction_pointer = self._computer_instruction_ptr
        self._computer_instruction_ptr = code.execute(
            self.intcode, self.io_wrapper
        )
        return code.operation

    def compute_all(self) -> IOHandler:
        while self.compute_step() != Operation.Halt:
            pass
        return self.io_wrapper


class AmplifierControllerSoftware:

    _SEQUENCE_VALUES: Tuple[int, ...] = (0, 1, 2, 3, 4)

    signals: List[int] = []

    def __init__(self, intcode: Intcode) -> None:
        self._computer = IntcodeComputer(intcode)
        self._sequences = tuple(permutations(self._SEQUENCE_VALUES))

    def run_software(self) -> None:
        for sequence in self._sequences:
            wrapper = IOWrapper(sequence)
            for _ in sequence:
                self._computer.io_wrapper = wrapper
                wrapper = self._computer.compute_all()
            self.signals.append(wrapper.output_values[-1])
            self._computer.reset_computer()

    def get_max_signal(self) -> int:
        return max(self.signals)
