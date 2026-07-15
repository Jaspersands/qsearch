import os
import tempfile
import unittest
from pathlib import Path

from dcp_sample_workbench import (
    DCPPhaseState,
    _nonzero_equal_residue_pairs,
    _target_complement_pairs,
    audit_dcp_decoder,
    combine_dcp_phase_states,
    dcp_state_access_contract,
    generate_dcp_phase_samples,
    run_dcp_sample_workbench,
    run_dcp_sieve_trial,
    write_dcp_sample_workbench,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPSampleWorkbenchTests(unittest.TestCase):
    def test_access_contract_supplies_states_and_forbids_evaluator(self):
        contract = dcp_state_access_contract()

        self.assertFalse(contract.full_family_coverage)
        self.assertFalse(contract.current_workbench_models_bad_registers)
        self.assertEqual(contract.failure_parameter, 1)
        self.assertTrue(any("independent D_N register samples" in item for item in contract.supplied_resources))
        self.assertIn("coherent phase evaluator", contract.forbidden_resources)
        self.assertFalse(any("evaluator" in resource.lower() for resource in contract.supplied_resources))

    def test_exact_combine_has_equal_sum_and_difference_branches(self):
        left = DCPPhaseState("left", 16, 5, 0, [0], 0, "omega_16^(5*s)")
        right = DCPPhaseState("right", 16, 3, 0, [1], 0, "omega_16^(3*s)")

        sum_branch = combine_dcp_phase_states(left, right, "sum")
        difference_branch = combine_dcp_phase_states(left, right, "difference")

        self.assertEqual(sum_branch.probability, 0.5)
        self.assertEqual(difference_branch.probability, 0.5)
        self.assertEqual(sum_branch.output_state.label, 8)
        self.assertEqual(difference_branch.output_state.label, 2)
        self.assertEqual(difference_branch.output_state.two_adic_valuation, 1)

    def test_sample_native_trial_charges_postselection_and_no_evaluator(self):
        trial = run_dcp_sieve_trial(
            n_bits=8,
            sample_count=512,
            rule="equal-residue-difference",
            seed=7,
        )

        self.assertEqual(trial.coset_state_query_count, 512)
        self.assertEqual(trial.evaluator_query_count, 0)
        self.assertTrue(trial.rounds)
        for round_record in trial.rounds:
            self.assertEqual(
                round_record.favorable_branch_count + round_record.unfavorable_branch_count,
                round_record.pair_count,
            )
            self.assertLessEqual(round_record.actual_output_states, round_record.legacy_optimistic_output_states)
            self.assertEqual(
                round_record.exact_conditional_expected_outputs,
                0.5 * round_record.desired_nonzero_pair_count,
            )
            self.assertEqual(
                round_record.exact_conditional_expected_targets,
                0.5 * round_record.target_capable_pair_count,
            )
            self.assertEqual(
                round_record.exact_conditional_no_target_probability,
                2.0 ** (-round_record.target_capable_pair_count),
            )
        self.assertGreater(sum(item.postselection_optimism_gap for item in trial.rounds), 0)

    def test_target_label_is_only_a_parity_endpoint(self):
        target = DCPPhaseState("target", 32, 16, 4, [0, 1], 1, "omega_32^(16*s)")
        decoder = audit_dcp_decoder([target], n_bits=5)

        self.assertTrue(decoder.parity_observation_available)
        self.assertEqual(decoder.independent_congruence_bits_recovered, 1)
        self.assertEqual(decoder.hidden_reflection_bits_required, 5)
        self.assertFalse(decoder.full_hidden_reflection_recovered)
        self.assertTrue(decoder.missing_decoder_stages)

    def test_strong_equal_residue_baseline_avoids_zero_differences(self):
        states = [
            DCPPhaseState(f"s{i}", 32, label, 0, [i], 0, f"omega_32^({label}*s)")
            for i, label in enumerate([1, 1, 1, 9, 17, 25])
        ]
        pairs, unpaired = _nonzero_equal_residue_pairs(states, bucket_bits=3)

        self.assertTrue(pairs)
        self.assertTrue(all(left.label != right.label for left, right in pairs))
        self.assertEqual(2 * len(pairs) + unpaired, len(states))

    def test_target_complement_baseline_pairs_known_half_modulus_labels(self):
        states = [
            DCPPhaseState(f"s{i}", 32, label, 0, [i], 0, f"omega_32^({label}*s)")
            for i, label in enumerate([1, 17, 3, 19, 4, 4])
        ]
        pairs, unpaired = _target_complement_pairs(states, target_label=16)

        self.assertEqual(len(pairs), 2)
        self.assertTrue(all((left.label - right.label) % 32 == 16 for left, right in pairs))
        self.assertEqual(unpaired, 2)

    def test_report_and_registry_record_methodological_negative_results(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_dcp_sample_workbench(
                    n_values=[8],
                    sample_count=512,
                    seed=11,
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_sample_native_sieve.json").exists()
            finally:
                os.chdir(old_cwd)

        negative_ids = {item["id"] for item in negatives}
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["evaluator_query_count"], 0)
        self.assertEqual(payload["headline_metrics"]["full_hidden_reflection_decode_count"], 0)
        self.assertIn("NEG-DCP-DETERMINISTIC-FAVORABLE-BRANCH", negative_ids)
        self.assertIn("NEG-DCP-PARITY-ENDPOINT-NOT-FULL-DECODER", negative_ids)
        result = next(item for item in results if item["experiment_id"] == "EXP-DHS-DCP-SAMPLE-NATIVE-SIEVE")
        self.assertIn("dcp_sample_native_sieve", result["artifacts"])
        self.assertTrue(result["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_generated_labels_follow_full_uniform_domain_including_zero(self):
        samples = generate_dcp_phase_samples(n_bits=4, sample_count=256, seed=3)
        labels = {state.label for state in samples}

        self.assertIn(0, labels)
        self.assertTrue(all(0 <= label < 16 for label in labels))
        self.assertGreater(len(labels), 12)

    def test_workbench_never_promotes_target_valuation_to_full_decode(self):
        report = run_dcp_sample_workbench(n_values=[8], sample_count=512, seed=5)

        self.assertEqual(report.headline_metrics["evaluator_query_count"], 0)
        self.assertEqual(report.headline_metrics["full_hidden_reflection_decode_count"], 0)
        self.assertGreater(report.headline_metrics["postselection_optimism_gap"], 0)
        self.assertEqual(report.status, "sample-native-baseline-blocks-speedup-claim")


if __name__ == "__main__":
    unittest.main()
