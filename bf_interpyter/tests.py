import unittest
from bf_interpyter import get_bfvm_memory

class TestInterpreterBehavior(unittest.TestCase):
    def test_asking_for_N_size_returns_nparray_with_len_N(self):
        N = 1000
        memory = get_bfvm_memory(8, N)
        self.assertEqual(len(memory), N)

if __name__ == "__main__":
    unittest.main()