import unittest
from bf_interpyter import get_bfvm_memory

class TestInterpreterBehavior(unittest.TestCase):
    def test_asking_for_N_size_returns_nparray_with_len_N(self):
        N = 1000
        memory = get_bfvm_memory(8, N)
        self.assertEqual(len(memory), N)

    def test_asking_for_minus_N_size_returns_empty_list(self):
        N = -1000
        memory = get_bfvm_memory(8, N)
        self.assertEqual(len(memory), 0)

    def test_asking_for_N_bit_number_returns_number_which_roll_after_overflow(self):
        N = 8
        memory = get_bfvm_memory(N, 1)
        value_to_overflow = 2 ** (N - 1)
        memory[0] += value_to_overflow
        self.assertEqual(memory[0], -value_to_overflow)

if __name__ == "__main__":
    unittest.main()