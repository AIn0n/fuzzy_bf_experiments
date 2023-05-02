import pytest
import numpy as np
from bf_interpyter import get_bfvm_memory, BF_interpreter


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


@pytest.mark.parametrize("N", [1, 2, 40, 80])
def test_execute_plus_N_times_sign_returns_N(N):
    interpreter = BF_interpreter()
    interpreter.execute("+" * N)
    assert interpreter.memory[0] == N


@pytest.mark.parametrize("X,Y", [(1, 2), (8, 30), (21, 28)])
def test_execute_plus_times_X_plus_times_Y_returns_XY(X, Y):
    interpreter = BF_interpreter()
    interpreter.execute("+" * X)
    interpreter.execute("+" * Y)

    assert interpreter.memory[0] == X + Y


def test_giving_wrong_memory_type_defaults_to_8bit():
    memory = get_bfvm_memory(9, 100)
    assert memory.dtype == np.int8


@pytest.mark.parametrize("N", [1, 10, 100])
def test_all_commands_except_default_commands_set_are_ignored(N):
    interpreter = BF_interpreter()
    interpreter.execute("+" * N + "hello world!")
    assert interpreter.memory[0] == N

@pytest.mark.parametrize("X,Y", [(2, 1), (30, 8), (28, 21)])
def test_plus_X_minus_Y_returns_X_minus_Y(X, Y):
    interpreter = BF_interpreter()
    interpreter.execute("+" * X)
    interpreter.execute("-" * Y)
    assert interpreter.memory[0] == X - Y
