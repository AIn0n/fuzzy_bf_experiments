import numpy as np
from enum import IntEnum

np.seterr(over="ignore")  # ignore overflow warnings


def get_bfvm_memory(mem_type: int, size: int) -> np.array:
    size_to_constr = {
        8: np.int8,
        16: np.int16,
        32: np.int32,
        64: np.int64,
    }
    if mem_type not in size_to_constr.keys():
        mem_type = 8
    return np.array([0] * size, dtype=size_to_constr[mem_type])


class BF_error:
    pass


class BF_interpreter:
    def __init__(self, mem_type: int = 64, size: int = 4000):
        self.memory = get_bfvm_memory(mem_type, size)
        self.pointer = 0

    def execute(self, commands: str) -> BF_error:
        comeback_stack = []
        n: int = 0
        while n < len(commands):
            match commands[n]:
                case "+":
                    self.memory[self.pointer] += 1
                case "-":
                    self.memory[self.pointer] -= 1
                case ">":
                    self.pointer += 1
                case "<":
                    self.pointer -= 1
                case "[":
                    if self.memory[self.pointer] == 0:
                        n += commands[n:].find("]")
                    else:
                        comeback_stack.append(n)
                case "]":
                    n = comeback_stack.pop()
                    continue
            n += 1
        return BF_error()
