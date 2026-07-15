import os
import tempfile
import unittest
from pathlib import Path

from phase_state_workbench import (
    audit_hidden_shift_family,
    generate_cyclic_phase_family,
    generate_phase_state_records,
    run_phase_state_collimation_trace,
    run_kuperberg_sieve_baseline,
    run_sieve_strategy_search,
    two_adic_valuation,
    write_hidden_shift_workbench,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results


class PhaseStateWorkbenchTests(unittest.TestCase):
    def test_kloosterman_trace_family_is_natural_prime_field_phase(self):
        spec, signal = generate_cyclic_phase_family("kloosterman_trace", n_bits=6)
        self.assertEqual(spec.id, "kloosterman_trace")
        self.assertEqual(spec.group, "Z_p")
        self.assertEqual(signal.shape[0], spec.domain_size)
        self.assertIn("trace_function", spec.parameters)
        self.assertTrue(abs(abs(signal[1]) - 1.0) < 1e-8)

    def test_quadratic_chirp_generates_scalable_prime_domain(self):
        spec, signal = generate_cyclic_phase_family("quadratic", n_bits=5)
        self.assertEqual(spec.id, "quadratic_chirp")
        self.assertGreaterEqual(spec.domain_size, 2**5)
        self.assertEqual(len(signal), spec.domain_size)
        self.assertEqual(abs(signal[3]), 1.0)

    def test_fp2_quadratic_family_uses_noncyclic_vector_space_and_is_dequantized(self):
        spec, signal = generate_cyclic_phase_family("fp2_quadratic_form", n_bits=6)
        self.assertEqual(spec.group, "F_p^2")
        self.assertEqual(spec.domain_size, spec.modulus * spec.modulus)
        self.assertEqual(len(signal), spec.domain_size)

        shift = spec.modulus + 2
        audit = audit_hidden_shift_family("fp2_quadratic_form", n_bits=6, shift=shift, sample_count=8, seed=4)
        self.assertTrue(
            any(
                attack.name == "fp2_quadratic_algebraic_reconstruction" and attack.success
                for attack in audit.classical_attacks
            )
        )
        self.assertTrue(audit.dequantization_risk.startswith("critical"))

    def test_mm_majority_family_is_structured_f2_phase_not_random_table(self):
        spec, signal = generate_cyclic_phase_family("mm_majority_bent_f2", n_bits=8)
        self.assertEqual(spec.group, "F2^n")
        self.assertEqual(spec.domain_size, 256)
        self.assertIn("Maiorana", spec.description)
        self.assertTrue(all(abs(value) == 1.0 for value in signal[:16]))

    def test_f2_bent_family_detected_as_algebraically_dequantized(self):
        audit = audit_hidden_shift_family("bent_quadratic_f2", n_bits=6, shift=13, sample_count=8, seed=2)
        self.assertTrue(any(attack.name == "f2_quadratic_algebraic_reconstruction" and attack.success for attack in audit.classical_attacks))
        self.assertTrue(audit.dequantization_risk.startswith("critical"))
        self.assertIn("random_sample", audit.survives_restricted_query_models)

    def test_sample_limited_baseline_differs_from_full_table_baseline(self):
        audit = audit_hidden_shift_family("masked_quadratic_f2", n_bits=8, shift=37, sample_count=8, seed=2)
        full_table_success = any(
            attack.success and "full_table" in attack.legal_query_models for attack in audit.classical_attacks
        )
        sample_success = any(
            attack.success and "random_sample" in attack.legal_query_models for attack in audit.classical_attacks
        )
        self.assertTrue(full_table_success)
        self.assertFalse(sample_success)
        self.assertIn("random_sample", audit.survives_restricted_query_models)
        random_probe = next(probe for probe in audit.query_lower_bound_probes if probe.model == "random_sample")
        self.assertEqual(random_probe.verdict, "undersampled-gap-not-evidence")
        self.assertGreater(random_probe.required_queries_for_constant_signal, random_probe.observed_query_budget)

    def test_classical_shift_baselines_recover_known_shift_and_flag_risk(self):
        audit = audit_hidden_shift_family("quadratic_chirp", n_bits=5, shift=9)
        self.assertEqual(audit.true_shift, 9)
        self.assertTrue(any(attack.success for attack in audit.classical_attacks))
        self.assertTrue(audit.falsifiers_triggered)
        self.assertIn("dequantization", audit.dequantization_risk)
        self.assertTrue(any(attack.name == "chosen_query_exhaustive_correlation" for attack in audit.classical_attacks))

    def test_phase_state_records_and_collimation_trace_keep_merge_histories(self):
        states = generate_phase_state_records(n_bits=6, sample_count=16, seed=4)
        self.assertEqual(len(states), 16)
        self.assertTrue(states[0].phase_expression.startswith("omega_64^("))
        trace = run_phase_state_collimation_trace(
            n_bits=6,
            sample_count=128,
            schedule=[1, 2, 3],
            seed=4,
            target_two_adic_valuation=3,
            strategy="test_schedule",
        )
        self.assertEqual(trace.input_model, "coherent_oracle_to_phase_states")
        self.assertGreaterEqual(len(trace.rounds), 1)
        self.assertLessEqual(len(trace.survivor_states_sample), 12)
        self.assertTrue(all(state.merge_history for state in trace.survivor_states_sample))
        self.assertGreaterEqual(trace.best_two_adic_valuation, 0)

    def test_kuperberg_sieve_baseline_increases_two_adic_valuation(self):
        self.assertEqual(two_adic_valuation(40, n_bits=8), 3)
        sieve = run_kuperberg_sieve_baseline(
            n_bits=8,
            sample_count=1024,
            schedule=[2, 3, 4],
            seed=3,
            target_two_adic_valuation=4,
        )
        self.assertGreaterEqual(sieve.best_two_adic_valuation, 4)
        self.assertTrue(sieve.reached_target)
        self.assertGreater(len(sieve.rounds), 0)
        self.assertGreaterEqual(sieve.memory_exponent_log2, 0.0)
        self.assertGreaterEqual(sieve.merge_depth, 1)

    def test_sieve_strategy_search_records_best_strategy(self):
        search = run_sieve_strategy_search(n_bits=8, sample_count=1024, seed=7)
        self.assertGreaterEqual(len(search.candidates), 3)
        self.assertIn(search.best_strategy, {candidate.strategy for candidate in search.candidates})
        self.assertGreaterEqual(search.best_two_adic_valuation, search.baseline.best_two_adic_valuation)

    def test_workbench_writes_artifact_and_experiment_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_hidden_shift_workbench(
                    families=["bent_quadratic_f2", "masked_quadratic_f2"],
                    min_bits=4,
                    max_bits=5,
                    shift=5,
                    sieve_samples=512,
                    sample_count=6,
                    seed=11,
                )
                artifact_exists = Path("research/phase_workbench/hidden_shift_audit.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(len(payload["family_audits"]), 4)
        self.assertIn("sieve_search", payload)
        self.assertIn("phase_state_trace", payload)
        self.assertIn("query_lower_bound_probes", payload["family_audits"][0])
        self.assertIn("scaling_history", payload)
        self.assertTrue(artifact_exists)
        self.assertTrue(any(result["id"] == "RESULT-HIDDEN-SHIFT-WORKBENCH-LATEST" for result in results))
        self.assertTrue(any(item["id"].startswith("HS-DEQUANTIZED-") for item in negatives))


if __name__ == "__main__":
    unittest.main()
