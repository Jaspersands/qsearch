import unittest
from coset_stable_root_separation_certificate import build_stable_root_separation_certificate

class CosetStableRootSeparationCertificateTests(unittest.TestCase):
    def test_certificate_build(self):
        cert = build_stable_root_separation_certificate()
        self.assertEqual(cert.status, "stable-root-separation-proved-circuit-decoder-open")
        self.assertIsNotNone(cert.headline_metrics)

if __name__ == "__main__":
    unittest.main()
