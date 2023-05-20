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


@pytest.mark.parametrize("X,Y", [(2, 1), (30, 8), (28, 21)])
def test_move_right_X_plus_Y_returns_Y_in_X(X, Y):
    interpreter = BF_interpreter()
    interpreter.execute(">" * X)
    interpreter.execute("+" * Y)
    assert interpreter.memory[X] == Y


@pytest.mark.parametrize("X,Y,Z", [(3, 1, 10), (30, 8, 32), (28, 21, 9)])
def test_move_right_X_move_left_Y_plus_Z_returns_Z_in_X_minus_Y(X, Y, Z):
    interpreter = BF_interpreter()
    interpreter.execute(">" * X)
    interpreter.execute("<" * Y)
    interpreter.execute("+" * Z)
    assert interpreter.memory[X - Y] == Z


@pytest.mark.parametrize("N", [3, 7, 12, 32])
def test_loop_to_copy_to_next_cell(N):
    interpreter = BF_interpreter()
    interpreter.execute("+" * N)
    interpreter.execute("[->+<]")
    assert interpreter.memory[interpreter.pointer + 1] == N
    assert interpreter.memory[interpreter.pointer] == 0


@pytest.mark.parametrize("N", [1, 5, 49, 348])
def test_nested_loop_to_move_pointers_returns_state_with_moved_pointer(N):
    interpreter = BF_interpreter()
    # init first cell at the tape with iterator value
    interpreter.execute("+" * N)
    interpreter.execute(
        """
    [
        [->+<] ## move iterator one to the right
        >- ## move pointer and decrement iterator
    ] # end loop
    """
    )
    assert interpreter.pointer == N
    assert not interpreter.memory.any()


@pytest.mark.parametrize("N", [1, 16, 48, 89])
def test_nested_loops_without_closing_returns_bf_error_with_trace(N):
    interpreter = BF_interpreter()
    err = interpreter.execute(
        ("+" * N)
        + """[
        [->+<] ## move iterator one to the right
        >- ## move pointer and decrement iterator
    #  lack of loop closing
    """
    )
    # message should be somehow meaningful
    assert "unclosed bracked" in err.msg
    # error should be shown at index bracked right after iterator init
    assert err.where == N
    # error should have information about if code was executed or not
    assert err.executed == False
