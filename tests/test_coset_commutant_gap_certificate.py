import os
import tempfile
import unittest
from pathlib import Path

import sympy as sp

from coset_commutant_gap_certificate import (
    build_commutant_gap_certificate,
    parity_specht_vector,
    stable_kronecker_multiplicity_certificate,
    target_polytabloid,
    write_commutant_gap_certificate,
)
from coset_commutant_gap_scaling import audit_commutant_gap_scaling
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class CommutantGapCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.certificate = build_commutant_gap_certificate()

    def test_polytabloid_maps_are_sparse_and_nonzero_in_both_parities(self) -> None:
        self.assertEqual(len(target_polytabloid()), 12)
        self.assertEqual(len(parity_specht_vector(1)), 24)
        self.assertEqual(len(parity_specht_vector(-1)), 36)
        records = {record.parity: record for record in self.certificate.parity_records}
        self.assertEqual(records["symmetric"].exact_norm, "24*(n - 3)/(n - 2)")
        self.assertEqual(records["antisymmetric"].exact_norm, "72*(n - 5)/(n - 2)")

    def test_character_factorial_moments_prove_total_multiplicity_two(self) -> None:
        certificate = stable_kronecker_multiplicity_certificate()
        self.assertTrue(certificate["proved"])
        self.assertEqual(certificate["stable_factorial_moment_threshold"], 7)
        self.assertEqual(certificate["stable_multiplicity_for_n_at_least_7"], 2)
        self.assertEqual(certificate["direct_n6_multiplicity"], 2)

    def test_symbolic_parity_eigenvalues_prove_inverse_quadratic_gap(self) -> None:
        report = self.certificate
        records = {record.parity: record for record in report.parity_records}
        self.assertEqual(
            records["symmetric"].exact_eigenvalue,
            "n**3 - 11*n**2 + 34*n - 26",
        )
        self.assertEqual(
            records["antisymmetric"].exact_eigenvalue,
            "(n - 1)*(n**2 - 10*n + 22)",
        )
        self.assertEqual(report.exact_gap_certificate["raw_gap"], "2*(n - 2)")
        self.assertEqual(
            report.exact_gap_certificate["lcu_normalized_gap"],
            "2/(n*(n - 1))",
        )
        self.assertTrue(report.claim_gate["all_n_restricted_gap_theorem_proved"])
        self.assertFalse(report.claim_gate["general_kronecker_multiplicity_transform_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_symbolic_formula_matches_independent_finite_seminormal_spectra(self) -> None:
        n = sp.symbols("n")
        symmetric = n**3 - 11 * n**2 + 34 * n - 26
        antisymmetric = (n - 1) * (n**2 - 10 * n + 22)
        for size in (6, 7):
            finite = audit_commutant_gap_scaling(size)
            expected_gap = abs(float(symmetric.subs(n, size) - antisymmetric.subs(n, size)))
            self.assertAlmostEqual(finite.critical_raw_gap, expected_gap, places=8)
            self.assertAlmostEqual(
                finite.critical_normalized_gap,
                2 / (size * (size - 1)),
                places=10,
            )

    def test_writer_runner_and_proof_tracker_preserve_restricted_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_commutant_gap_certificate()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                runner = run_experiment("EXP-COSET-COMMUTANT-GAP-CERTIFICATE")
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_commutant_gap_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-COMMUTANT-GAP-CERTIFICATE", supported_experiment_ids()
        )
        self.assertTrue(
            any(
                item["artifacts"].get("coset_commutant_gap_certificate")
                for item in results
            )
        )
        self.assertIn(
            "NEG-COSET-RESTRICTED-GAP-AS-GENERAL-KRONECKER-TRANSFORM",
            {item["id"] for item in negatives},
        )
        finding = next(
            item
            for item in dequantization["findings"]
            if item["id"]
            == "DEQ-COSET-FINITE-COMMUTANT-SPLITTING-NEEDS-GAP-THEOREM"
        )
        self.assertIn("restricted all-n gap theorems=1", finding["evidence"])
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        candidate = "CODE-COSET-COLLECTIVE"
        self.assertEqual(
            lemmas[f"LEMMA-{candidate}-COSET-RESTRICTED-COMMUTANT-GAP"]["status"],
            "proved-exact-restricted-inverse-quadratic-commutant-gap",
        )
        self.assertEqual(
            lemmas[f"LEMMA-{candidate}-COSET-KRONECKER-MULTIPLICITY-BASIS"]["status"],
            "blocked-restricted-gap-proved-general-multiplicity-basis-open",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
