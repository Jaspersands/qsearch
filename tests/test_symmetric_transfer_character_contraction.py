import unittest
from symmetric_transfer_character_contraction import unpack_pair

class SymmetricTransferCharacterContractionTests(unittest.TestCase):
    def test_translation_character_contraction(self):
        pair = unpack_pair(0, 2)
        self.assertIsInstance(pair, tuple)
        self.assertEqual(len(pair), 2)

if __name__ == "__main__":
    unittest.main()
