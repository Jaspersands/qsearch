import json
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from coset_typical_parity_complete_separator import (
    CERTIFICATE_PATH,
    DISCOVERY_COEFFICIENTS,
    GENERATOR_NAMES,
    build_parity_complete_separator_report,
    exact_portfolio_mean_variance,
    load_n7_search_certificate,
    primitive_coefficient_vectors,
    search_coefficients,
    write_parity_complete_separator_report,
)
from research_registry import load_experiment_results, load_negative_results


class TypicalParityCompleteSeparatorTests(unittest.TestCase):
    def test_coefficient_search_space_is_canonical_and_complete(self):
        vectors = primitive_coefficient_vectors()

        self.assertEqual(len(vectors), 1744)
        self.assertEqual(len(set(vectors)), len(vectors))
        self.assertIn(DISCOVERY_COEFFICIENTS, vectors)
        self.assertTrue(
            all(next(value for value in vector if value) > 0 for vector in vectors)
        )

    def test_exactly_repairs_former_scalar_blocks(self):
        for right in ((3, 3), (2, 2, 2)):
            mean, variance = exact_portfolio_mean_variance(
                6,
                (3, 2, 1),
                right,
                (3, 2, 1),
            )
            self.assertEqual(abs(mean), Fraction(7, 120))
            self.assertGreater(variance, 0)

    def test_lightweight_search_finds_collision_free_parity_rule(self):
        records = search_coefficients((5, 6))

        self.assertEqual(len(records), 1744)
        self.assertEqual(records[0].collision_count, 0)
        discovery = next(
            record
            for record in records
            if record.coefficients == DISCOVERY_COEFFICIENTS
        )
        self.assertEqual(discovery.collision_count, 0)

    def test_hash_gated_n7_certificate_and_report(self):
        certificate = load_n7_search_certificate()
        report = build_parity_complete_separator_report()

        self.assertEqual(
            certificate["search"]["coefficient_vector_count"],
            1744,
        )
        self.assertEqual(
            certificate["search"]["block_count_by_n"],
            {"5": 6, "6": 89, "7": 568},
        )
        self.assertEqual(report.best_candidate.collision_count, 0)
        self.assertGreater(
            report.headline_metrics[
                "collision_free_finite_candidate_count"
            ],
            0,
        )
        self.assertEqual(
            report.headline_metrics[
                "former_scalar_block_exact_repair_count"
            ],
            2,
        )
        self.assertFalse(report.claim_gate["all_n_square_free_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_result_and_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                certificate = json.loads(
                    (
                        Path(old_cwd)
                        / CERTIFICATE_PATH
                    ).read_text()
                )
                local_certificate = Path(CERTIFICATE_PATH)
                local_certificate.parent.mkdir(parents=True, exist_ok=True)
                local_certificate.write_text(
                    json.dumps(certificate, indent=2, sort_keys=True)
                )
                write_parity_complete_separator_report(
                    output_path=Path("parity.json")
                )
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(
            any(
                result["experiment_id"]
                == "EXP-COSET-TYPICAL-PARITY-COMPLETE-SEPARATOR"
                for result in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-COSET-TYPICAL-ONE-SIDED-PORTFOLIO-PARITY-INCOMPLETE"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
