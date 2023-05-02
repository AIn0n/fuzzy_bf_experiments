import pytest
import numpy as np
from bf_interpyter import get_bfvm_memory


@pytest.mark.parametrize("N", [1, 23, 3849])
def test_asking_for_N_size_returns_nparray_with_len_N(N):
    memory = get_bfvm_memory(8, N)
    assert len(memory) == N


@pytest.mark.parametrize("N", [0, -100, -248])
def test_asking_for_minus_N_size_returns_empty_list(N):
    memory = get_bfvm_memory(8, N)
    assert len(memory) == 0


@pytest.mark.parametrize("N", [8, 16, 32, 64])
def test_asking_for_N_bit_number_returns_number_which_roll_after_overflow(N):
    memory = get_bfvm_memory(N, 1)
    value_to_overflow = np.int64(2) ** (N - 1)
    memory[0] += value_to_overflow
    assert memory[0] == -value_to_overflow
