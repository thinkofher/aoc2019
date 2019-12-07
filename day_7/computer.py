from typing import List, Tuple
from itertools import permutations, cycle

from operations import Operation
from singlecode import SingleCode
from values import ImmutableIntcode, Intcode
from handler import IOHandler, StdIOWrapper, IOWrapper, IOLoopWrapper


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


class Amplifier(IntcodeComputer):

    tag: str
    saved_values: List[int]

    def __init__(self, intcode: Intcode, tag: str) -> None:
        super().__init__(intcode)
        self.tag = tag
        self.saved_values = []

    def compute_until_output(self) -> IOHandler:
        step = self.compute_step()
        while step != Operation.Halt:
            if step == Operation.Output:
                self.saved_values.append(self.io_wrapper.output_values[-1])
                return self.io_wrapper
            step = self.compute_step()
        raise StopIteration("Computer got Halt signal.")


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


class AmplifiersFeedbackLoopSoftware:

    _SEQUENCE_VALUES: Tuple[int, ...] = (5, 6, 7, 8, 9)
    _AMP_TAGS: Tuple[str, ...] = ("A", "B", "C", "D", "E")

    _intcode: Tuple[int, ...]
    signals: List[int]

    def __init__(self, intcode: Intcode) -> None:
        self._intcode = tuple(intcode)
        self._sequences = tuple(permutations(self._SEQUENCE_VALUES))
        self._allocate_computers()
        self.signals = []

    def _allocate_computers(self) -> None:
        self._computers = [
            Amplifier(list(self._intcode), tag) for tag in self._AMP_TAGS
        ]

    def run_software(self) -> None:
        for sequence in self._sequences:
            wrapper = IOLoopWrapper(sequence)
            try:
                for computer in cycle(self._computers):
                    computer.io_wrapper = wrapper
                    wrapper = computer.compute_until_output()
            except StopIteration:
                self.signals.append(self._computers[-1].saved_values[-1])
                self._allocate_computers()

    def get_max_signal(self) -> int:
        return max(self.signals)
