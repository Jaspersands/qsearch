import itertools
import os
import tempfile
import unittest

from dcp_carry_high_part_no_go import (
    carry_slice_assignments,
    carry_union_bound,
    compose_power_of_two_label,
    exact_target_translation_census,
    high_equation_matches_full_equation,
    run_carry_high_part_no_go,
    split_power_of_two_label,
    write_carry_high_part_no_go,
)
from experiment_runner import run_experiment, supported_experiment_ids
from dcp_subset_sum_solver_synthesis import write_subset_sum_solver_synthesis
from dequantization_checks import write_dequantization_report
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class CarryHighPartNoGoTests(unittest.TestCase):
    def test_power_of_two_decomposition_is_a_bijection(self):
        for n_bits in range(3, 7):
            for low_bits in range(1, n_bits):
                for value in range(1 << n_bits):
                    low, high = split_power_of_two_label(value, n_bits, low_bits)
                    self.assertEqual(
                        compose_power_of_two_label(low, high, n_bits, low_bits),
                        value,
                    )

    def test_carry_slices_partition_low_congruence_assignments(self):
        low_labels = [1, 2, 3, 1]
        low_modulus = 4
        target_low = 2
        sliced = set()
        for carry in range(len(low_labels) + 1):
            sliced.update(carry_slice_assignments(low_labels, target_low, low_modulus, carry))
        direct = {
            bits
            for bits in itertools.product((0, 1), repeat=len(low_labels))
            if sum(label * bit for label, bit in zip(low_labels, bits)) % low_modulus == target_low
        }
        self.assertEqual(sliced, direct)

    def test_high_equation_is_exactly_the_full_equation_on_each_slice(self):
        n_bits = 5
        low_bits = 2
        labels = [3, 11, 26, 17]
        for target in range(1 << n_bits):
            for assignment in itertools.product((0, 1), repeat=len(labels)):
                self.assertTrue(
                    high_equation_matches_full_equation(
                        labels, target, assignment, n_bits, low_bits
                    )
                )

    def test_target_translation_is_exactly_uniform_for_every_carry(self):
        for quotient_modulus in (2, 4, 8, 16):
            for carry in range(9):
                census = exact_target_translation_census(quotient_modulus, carry)
                self.assertTrue(census["translation_is_bijection"])
                self.assertEqual(census["minimum_output_multiplicity"], 1)
                self.assertEqual(census["maximum_output_multiplicity"], 1)

    def test_polynomial_carry_union_bound_cannot_rescue_exponential_probability(self):
        self.assertEqual(carry_union_bound(2**-40, 100), 100 * 2**-40)
        report = run_carry_high_part_no_go(n_values=(128, 256, 512))
        self.assertTrue(report.theorem_certificate.exponentially_rare_generic_event_remains_exponential)
        self.assertTrue(all(row.asymptotically_exponential_after_sweep for row in report.rows))
        self.assertFalse(report.claim_gate["generic_high_event_proved_exponentially_rare"])
        self.assertFalse(report.claim_gate["joint_low_high_lattice_geometry_closed"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_runner_register_the_no_go(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_carry_high_part_no_go(n_values=(32, 64))
                runner = run_experiment("EXP-DHS-DCP-CARRY-HIGH-PART-NOGO")
                synthesis = write_subset_sum_solver_synthesis()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-DHS-DCP-CARRY-HIGH-PART-NOGO", supported_experiment_ids())
        self.assertTrue(any(item["artifacts"].get("dcp_carry_high_part_no_go") for item in results))
        self.assertIn(
            "NEG-DCP-LOW-ONLY-CARRY-SELECTION-HIGH-GEOMETRY",
            {item["id"] for item in negatives},
        )
        primitive_ids = {item["primitive_id"] for item in synthesis["primitives"]}
        self.assertIn("carry-selected-high-part-product-no-go", primitive_ids)
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn("DEQ-DCP-CARRY-SELECTED-HIGH-QUOTIENT-IS-GENERIC", finding_ids)
        lemma = next(
            item
            for item in proofs["proof_debt"]["lemmas"]
            if item["id"] == "LEMMA-DHS-GOWERS-SIEVE-DCP-CARRY-HIGH-PART-PRODUCT-NOGO"
        )
        self.assertEqual(lemma["status"], "proved-low-only-carry-high-part-product-no-go")
        query = next(item for item in queries["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE")
        self.assertTrue(any("Carry-selected high-part theorem" in item for item in query["blocking_evidence"]))
        dcp_frontier = next(
            item for item in frontier["frontiers"] if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Carry-selected high quotient", dcp_frontier["evidence"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
