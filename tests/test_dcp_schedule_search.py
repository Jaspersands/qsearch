import os
import tempfile
import unittest
from pathlib import Path

from dcp_schedule_search import (
    mutate_schedule,
    normalize_schedule,
    _two_sided_discordant_p_value,
    run_dcp_schedule_search_report,
    search_schedule,
    write_dcp_schedule_search_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPScheduleSearchTests(unittest.TestCase):
    def test_exact_discordant_test_penalizes_balanced_pairs(self):
        self.assertEqual(_two_sided_discordant_p_value(0, 0), 1.0)
        self.assertEqual(_two_sided_discordant_p_value(4, 4), 1.0)
        self.assertLess(_two_sided_discordant_p_value(12, 0), 0.001)

    def test_schedule_normalization_is_increasing_and_reaches_target(self):
        schedule = normalize_schedule(12, [8, 2, 2, 15, -1])

        self.assertEqual(schedule, (2, 8, 11))
        self.assertEqual(list(schedule), sorted(set(schedule)))

    def test_mutations_preserve_schedule_contract(self):
        import random

        rng = random.Random(4)
        schedule = (3, 6, 9, 11)
        for _ in range(40):
            schedule = mutate_schedule(12, schedule, rng)
            self.assertEqual(schedule[-1], 11)
            self.assertTrue(all(1 <= value < 12 for value in schedule))
            self.assertEqual(list(schedule), sorted(set(schedule)))

    def test_search_uses_disjoint_train_and_holdout_seeds(self):
        record = search_schedule(
            n_bits=10,
            rule="randomized-equal-residue-difference",
            population_size=5,
            generations=2,
            train_trials=3,
            holdout_trials=5,
            confirmation_trials=7,
            seed=2,
        )

        self.assertNotEqual(record.train_evaluation.seed_start, record.holdout_evaluation.seed_start)
        self.assertEqual(record.holdout_evaluation.seed_start, record.default_holdout_evaluation.seed_start)
        self.assertEqual(record.train_evaluation.split, "train")
        self.assertEqual(record.holdout_evaluation.split, "holdout")
        self.assertEqual(record.train_evaluation.evaluator_query_count, 0)
        self.assertFalse(record.below_birthday_sample_regime)
        self.assertFalse(record.heldout_seed_improvement)
        self.assertFalse(record.statistically_confirmed_improvement)
        self.assertNotEqual(record.holdout_evaluation.seed_start, record.confirmation_seed_start)
        self.assertEqual(record.optimizer_trial_count, record.evaluated_schedule_count * 3)

    def test_heldout_search_never_opens_asymptotic_claim_gate(self):
        report = run_dcp_schedule_search_report(
            n_values=[10],
            population_size=5,
            generations=2,
            train_trials=3,
            holdout_trials=5,
            confirmation_trials=7,
            seed=2,
        )

        self.assertTrue(report.claim_gate["train_holdout_separation_enforced"])
        self.assertFalse(report.claim_gate["uniform_recurrence_proved"])
        self.assertFalse(report.claim_gate["asymptotic_improvement_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_result_and_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_dcp_schedule_search_report(
                    n_values=[10],
                    population_size=5,
                    generations=2,
                    train_trials=3,
                    holdout_trials=5,
                    confirmation_trials=7,
                    seed=2,
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                exists = Path("research/phase_workbench/dcp_schedule_search.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(exists)
        self.assertGreater(payload["headline_metrics"]["unique_schedule_count"], 0)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-SCHEDULE-SEARCH" for item in results))
        self.assertIn(
            "NEG-DCP-SCHEDULE-SELECTION-NOT-ASYMPTOTIC-PROOF",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
