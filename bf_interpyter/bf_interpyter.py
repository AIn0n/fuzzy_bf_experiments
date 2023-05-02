import numpy as np

np.seterr(over="ignore")  # ignore overflow warnings


def get_bfvm_memory(mem_type: int, size: int) -> np.array:
    size_to_constr = {
        8: np.int8,
        16: np.int16,
        32: np.int32,
        64: np.int64,
    }
    return np.array([0] * size, dtype=size_to_constr[mem_type])

class BF_error:
    pass

class BF_interpreter:
    def __init__(self, mem_type: int = 64, size: int = 4000):
        self.memory = get_bfvm_memory(mem_type, size)

    def execute(self, commands: str)->BF_error:
        self.memory[0] = 1
        return BF_error()