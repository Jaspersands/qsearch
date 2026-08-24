import unittest
from code_syzygy_invariants import gf2_bit_rank, gf2_kernel_from_columns, homogeneous_monomials

class CodeSyzygyInvariantsTests(unittest.TestCase):
    def test_monomials_and_gf2_rank(self):
        monoms = homogeneous_monomials(3, 2)
        self.assertEqual(len(monoms), 6)
        cols = [1, 2, 3]  # binary 01, 10, 11
        rank = gf2_bit_rank(cols)
        self.assertEqual(rank, 2)
        dim, basis = gf2_kernel_from_columns(cols)
        self.assertTrue(len(basis) >= 1)

if __name__ == "__main__":
    unittest.main()
