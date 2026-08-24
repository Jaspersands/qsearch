import unittest
from symmetric_character import conjugacy_class_size, normalize_partition

class SymmetricCharacterTests(unittest.TestCase):
    def test_partition_and_class_size(self):
        part = normalize_partition((3, 1, 0, 0))
        self.assertEqual(part, (3, 1))
        size = conjugacy_class_size((2, 1))
        self.assertEqual(size, 3)  # 3 transpositions in S_3

if __name__ == "__main__":
    unittest.main()
