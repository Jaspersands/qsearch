import unittest
from symmetric_yjm_projector_trace import compose, identity_permutation, transposition

class SymmetricYjmProjectorTraceTests(unittest.TestCase):
    def test_permutations_and_transposition(self):
        id_perm = identity_permutation(3)
        self.assertEqual(id_perm, (0, 1, 2))
        t = transposition(3, 0, 1)
        self.assertEqual(t, (1, 0, 2))
        self.assertEqual(compose(t, t), id_perm)

if __name__ == "__main__":
    unittest.main()
