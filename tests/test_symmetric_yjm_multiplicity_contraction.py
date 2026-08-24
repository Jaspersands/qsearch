import unittest
from symmetric_yjm_multiplicity_contraction import _source_adjacent_generators, yjm_content_penalty_operator

class SymmetricYjmMultiplicityContractionTests(unittest.TestCase):
    def test_generators_and_operator(self):
        gens = _source_adjacent_generators((2, 1))
        self.assertTrue(len(gens) > 0)
        op = yjm_content_penalty_operator((2, 1), (0, 1, -1))
        self.assertIsNotNone(op)

if __name__ == "__main__":
    unittest.main()
