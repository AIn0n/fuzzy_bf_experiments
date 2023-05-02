import numpy as np

np.seterr(over='ignore')  # ignore overflow warnings

def get_bfvm_memory(mem_type: int, size: int) -> np.array:
    size_to_constr = {
        8: np.int8,
        16: np.int16,
        32: np.int32,
        64: np.int64,
    }
    return np.array([0] * size, dtype= size_to_constr[mem_type])
