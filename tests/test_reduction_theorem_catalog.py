import unittest
from reduction_theorem_catalog import build_theorem_catalog, seed_theorem_contracts

class ReductionTheoremCatalogTests(unittest.TestCase):
    def test_catalog_build(self):
        contracts = seed_theorem_contracts()
        self.assertTrue(len(contracts) > 0)
        catalog = build_theorem_catalog()
        self.assertEqual(catalog["status"], "contracts-validated")

if __name__ == "__main__":
    unittest.main()
