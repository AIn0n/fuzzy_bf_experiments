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
    def __init__(self, idx: int = -1, msg: str = "", suc: bool = True) -> None:
        self.executed = suc
        self.where = idx
        self.msg = msg


class BF_IO_handler:
    def __init__(self) -> None:
        self.input = []
        self.output = []

    def input_append(self, el: int) -> None:
        self.input.append(el)

    def input_pop(self):
        return self.input.pop()

    def output_append(self, el: int) -> None:
        self.output.append(el)

    def get_output(self) -> list:
        return self.output


def get_jump_table(commands: str) -> tuple[dict, BF_error]:
    comeback_stack = []
    jump_map = {}
    for idx, val in enumerate(commands):
        if val == "[":
            comeback_stack.append(idx)
        if val == "]":
            last = comeback_stack.pop()
            jump_map[last] = idx
            jump_map[idx] = last
    if len(comeback_stack) > 0:
        idx = comeback_stack.pop()
        return jump_map, BF_error(idx=idx, msg=f"unclosed bracked at {idx}", suc=False)

    return jump_map, BF_error()


def get_io_err_msg(idx, which):
    return BF_error(
        idx=idx, msg=f"IO handler not defined, {which} needed in {idx}", suc=False
    )


class BF_interpreter:
    def __init__(self, mem_type: int = 64, size: int = 4000):
        self.memory = get_bfvm_memory(mem_type, size)
        self.pointer = 0

    def execute(self, commands: str, io_handler: BF_IO_handler = None) -> BF_error:
        jump_map, err = get_jump_table(commands)
        if not err.executed:
            return err
        n: int = 0
        while n < len(commands):
            match commands[n]:
                case ".":
                    if io_handler == None:
                        return get_io_err_msg(n, "output")
                    io_handler.output_append(self.memory[self.pointer])
                case ",":
                    if io_handler == None:
                        return get_io_err_msg(n, "input")
                    self.memory[self.pointer] = io_handler.input_pop()
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
                        n = jump_map[n]
                case "]":
                    n = jump_map[n]
                    continue
            n += 1
        return BF_error()
