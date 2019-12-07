from itertools import chain
from typing import Tuple, List
from abc import ABC, abstractmethod


class IOHandler(ABC):

    output_values: List[int] = []

    @abstractmethod
    def get_input(self) -> int:
        pass

    def set_output(self, value: int) -> None:
        self.output_values.append(value)


class IOWrapper(IOHandler):

    setting_sequence: Tuple[int]
    _in_pos: int = 0

    def __init__(self, setting_sequence: Tuple[int]) -> None:
        self.setting_sequence = setting_sequence
        # Add zero as the first input value for the computer
        self.output_values = [0]

    def _all_values(self) -> Tuple[int, ...]:
        return tuple(
            chain.from_iterable(zip(self.setting_sequence, self.output_values))
        )

    def get_input(self) -> int:
        index, self._in_pos = self._in_pos, self._in_pos + 1
        return self._all_values()[index]


class IOLoopWrapper(IOHandler):

    setting_sequence: List[int]
    _out_val_pos: int
    _sequence_turn: bool

    def __init__(self, setting_sequence: Tuple[int]) -> None:
        self.setting_sequence = list(setting_sequence)
        # Add zero as the first input value for the computer
        self.output_values = [0]
        self._sequence_turn = True
        self._out_val_pos = 0

    def _switch_turn(self) -> None:
        self._sequence_turn = not self._sequence_turn

    def get_input(self) -> int:
        try:
            if self._sequence_turn:
                self._switch_turn()
                return self.setting_sequence.pop(0)
            else:
                self._switch_turn()
                return self.output_values[-1]
        except IndexError:
            return self.output_values[-1]


class StdIOWrapper(IOHandler):
    def get_input(self) -> int:
        input_value = input("Enter input: ")
        return int(input_value)

    def set_output(self, value: int) -> None:
        print(value)
