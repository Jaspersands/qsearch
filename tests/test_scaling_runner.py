import os
import tempfile
import unittest
from pathlib import Path

from research_registry import initialize_seed_registry, load_scaling_runs, validate_registry
from scaling_runner import parse_int_csv, write_hidden_shift_sweep


class ScalingRunnerTests(unittest.TestCase):
    def test_parse_int_csv(self):
        self.assertEqual(parse_int_csv("5, 6,8"), [5, 6, 8])

    def test_hidden_shift_sweep_writes_scaling_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_hidden_shift_sweep(
                    n_values=[4, 5],
                    sample_counts=[128, 256],
                    families=["bent_quadratic_f2", "masked_quadratic_f2"],
                    seed=3,
                )
                artifact_exists = Path("research/scaling/hidden_shift_sweep.json").exists()
                runs = load_scaling_runs()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(len(payload["rows"]), 4)
        self.assertTrue(artifact_exists)
        self.assertTrue(any(run["id"] == "SWEEP-HIDDEN-SHIFT-LATEST" for run in runs))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
