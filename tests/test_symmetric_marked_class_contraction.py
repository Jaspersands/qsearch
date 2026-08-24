import unittest
from symmetric_marked_class_contraction import canonical_pair_key, compose, cycle_type, inverse

class SymmetricMarkedClassContractionTests(unittest.TestCase):
    def test_permutations_and_cycle_type(self):
        p = (1, 2, 0)
        inv = inverse(p)
        self.assertEqual(compose(p, inv), (0, 1, 2))
        self.assertEqual(cycle_type(p), (3,))
        key = canonical_pair_key((1, 0), (0, 1))
        self.assertIsInstance(key, tuple)

if __name__ == "__main__":
    unittest.main()
