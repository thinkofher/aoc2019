from typing import Dict, Tuple, List

Intcode = List[str]
ImmutableIntcode = Tuple[str, ...]


class IntcodeMemory:

    _init_memory: ImmutableIntcode
    base_memory: Intcode
    additional_memory: Dict[int, str]

    def __init__(self, intcode: Intcode) -> None:
        self._init_memory = tuple(intcode)
        self.base_memory = intcode
        self.additional_memory = {}

    def __getitem__(self, key: int) -> str:
        try:
            return self.base_memory[key]
        except IndexError:
            try:
                return self.additional_memory[key]
            except KeyError:
                # return default value beyond memory
                self.additional_memory[key] = "0"
                return self.additional_memory[key]

    def __setitem__(self, key: int, value: str) -> None:
        try:
            self.base_memory[key] = value
        except IndexError:
            self.additional_memory[key] = value

    def reset(self) -> None:
        self.base_memory = list(self._init_memory)
        self.additional_memory = {}
