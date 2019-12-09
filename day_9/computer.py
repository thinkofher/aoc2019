from operations import Operation
from singlecode import SingleCode
from memory import ImmutableIntcode, Intcode
from handler import IOHandler, StdIOWrapper
from memory import IntcodeMemory


class IntcodeComputer:

    io_wrapper: IOHandler = StdIOWrapper()

    _computer_instruction_ptr: int
    init_intcode: ImmutableIntcode
    intcode: Intcode
    relative_base: int

    def __init__(self, intcode: Intcode) -> None:
        self.intcode_memory = IntcodeMemory(intcode)
        self._computer_instruction_ptr = 0
        self.relative_base = 0

    def reset_computer(self) -> None:
        self._step = 0
        self._computer_instruction_ptr = 0
        self.relative_base = 0
        self.intcode_memory.reset()

    def compute_step(self) -> Operation:
        ptr = self._computer_instruction_ptr

        code = SingleCode.from_intcode(
            self.intcode_memory.base_memory[ptr:ptr + 4], self.relative_base,
        )
        code.instruction_pointer = ptr
        self._computer_instruction_ptr = code.execute(
            self.intcode_memory, self.io_wrapper
        )

        # read relative value saved to io_wrapper
        self.relative_base += self.io_wrapper.relative_base_adjust_value

        # reset relative base adjust value of io_wrapper
        self.io_wrapper.relative_base_adjust_value = 0
        return code.operation

    def compute_all(self) -> IOHandler:
        while self.compute_step() != Operation.Halt:
            pass
        return self.io_wrapper
