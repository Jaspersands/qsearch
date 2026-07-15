import os
import random
import tempfile
import unittest
from pathlib import Path

from dcp_likelihood_branch_bound import (
    exact_branch_bound_decode,
    generate_contaminated_quadrature_samples,
    interval_score_upper_bound,
    likelihood_score,
    run_likelihood_branch_bound_report,
    write_likelihood_branch_bound_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPLikelihoodBranchBoundTests(unittest.TestCase):
    def test_interval_upper_bound_dominates_every_contained_score(self):
        records, _ = generate_contaminated_quadrature_samples(6, 17, 64, 1.0 / 6.0, seed=4)
        rng = random.Random(7)
        for _ in range(20):
            lower = rng.randrange(64)
            upper = rng.randrange(lower, 64)
            bound = interval_score_upper_bound(records, 64, lower, upper)
            exact_maximum = max(likelihood_score(records, 64, candidate) for candidate in range(lower, upper + 1))
            self.assertGreaterEqual(bound + 1e-9, exact_maximum)

    def test_branch_bound_matches_exhaustive_argmax(self):
        records, _ = generate_contaminated_quadrature_samples(7, 53, 96, 1.0 / 7.0, seed=9)
        decoded, metrics = exact_branch_bound_decode(records, 128)
        exhaustive = max(range(128), key=lambda candidate: likelihood_score(records, 128, candidate))

        self.assertEqual(decoded, exhaustive)
        self.assertTrue(metrics["complete_exact_search"])
        self.assertLessEqual(metrics["unique_score_evaluation_count"], 128)

    def test_report_preserves_restricted_scope(self):
        report = run_likelihood_branch_bound_report(n_values=[7, 8, 9], trials_per_size=2, sample_multiplier=12.0)

        self.assertEqual(report.headline_metrics["complete_exact_search_count"], 6)
        self.assertEqual(report.headline_metrics["proved_polynomial_branch_bound_count"], 0)
        self.assertEqual(report.headline_metrics["proved_nonlinear_decoder_lower_bound_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_result_and_method_specific_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_likelihood_branch_bound_report(n_values=[7, 8], trials_per_size=1)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/dcp_likelihood_branch_bound.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-LIKELIHOOD-BRANCH-BOUND" for item in results))
        self.assertIn(
            "NEG-DCP-LIKELIHOOD-INTERVAL-BOUND-EXPONENTIAL-SCALING",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
