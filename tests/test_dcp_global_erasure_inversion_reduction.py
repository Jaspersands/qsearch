import tempfile
import unittest
from pathlib import Path

from dcp_global_erasure_inversion_reduction import (
    audit_target_law_transfer,
    build_global_erasure_inversion_report,
    coherence_erasure_certificate,
    write_global_erasure_inversion_report,
)
from experiment_runner import run_experiment
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
)


class DCPGlobalErasureInversionReductionTests(unittest.TestCase):
    def test_coherence_certificate_requires_common_garbage(self):
        certificate = coherence_erasure_certificate()
        self.assertTrue(certificate.proved)
        self.assertIn("<g_t|g_s>", certificate.coherence_multiplier)
        self.assertIn("identical", certificate.common_garbage_conclusion)

    def test_target_law_domination_is_exact(self):
        for n_bits in (6, 8, 10):
            row = audit_target_law_transfer(
                n_bits, 0, 1009 * n_bits
            )
            self.assertEqual(
                row.status,
                "uniform-legal-dominated-by-source-weighted-law",
            )
            self.assertLessEqual(row.domination_residual, 1e-12)
            self.assertLessEqual(
                row.maximum_exact_law_ratio,
                row.domination_constant + 1e-12,
            )

    def test_report_reduces_erasure_but_not_arbitrary_pgm(self):
        report = build_global_erasure_inversion_report(
            n_values=(6, 8, 10),
            trials_per_size=2,
        )
        self.assertTrue(
            report.claim_gate[
                "coherent_erasure_implies_average_witness_solver"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "arbitrary_full_rank_pgm_reduced_to_witness_solver"
            ]
        )
        self.assertEqual(
            report.headline_metrics[
                "polynomial_coherent_erasure_circuit_count"
            ],
            0,
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_runner_register_negative_result(self):
        initialize_seed_registry(overwrite=False)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "erasure.json"
            payload = write_global_erasure_inversion_report(
                output_path=output,
                n_values=(6, 8),
                trials_per_size=1,
            )
            self.assertTrue(output.exists())
            self.assertEqual(
                payload["headline_metrics"][
                    "proved_coherent_erasure_to_witness_reduction_count"
                ],
                1,
            )
            self.assertTrue(
                any(
                    row["id"]
                    == "NEG-DCP-COHERENT-ERASURE-AS-PGM-SHORTCUT"
                    for row in load_negative_results()
                )
            )
        result = run_experiment(
            "EXP-DHS-DCP-GLOBAL-ERASURE-INVERSION-REDUCTION"
        )
        self.assertEqual(result.status, "completed")
        self.assertTrue(
            any(
                row["experiment_id"]
                == "EXP-DHS-DCP-GLOBAL-ERASURE-INVERSION-REDUCTION"
                for row in load_experiment_results()
            )
        )


if __name__ == "__main__":
    unittest.main()
