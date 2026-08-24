import unittest
from symmetric_modular_yjm_contraction import modular_inverse, transposition_word

class SymmetricModularYjmContractionTests(unittest.TestCase):
    def test_modular_inverse_and_words(self):
        self.assertEqual(modular_inverse(3, 7), 5)
        word = transposition_word(1, 2)
        self.assertIsInstance(word, tuple)

if __name__ == "__main__":
    unittest.main()
