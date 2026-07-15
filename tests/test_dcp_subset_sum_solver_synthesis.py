import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_solver_synthesis import (
    build_solver_primitives,
    run_subset_sum_solver_synthesis,
    synthesize_solver_hypotheses,
    write_subset_sum_solver_synthesis,
)
from research_registry import initialize_seed_registry, load_negative_results


class DCPSubsetSumSolverSynthesisTests(unittest.TestCase):
    def test_weak_mutations_are_rejected(self):
        rows = {item.hypothesis_id: item for item in synthesize_solver_hypotheses()}
        self.assertTrue(rows["REJECT-DCP-SS-LLL-CONSTANT-RETUNE"].preflight_status.startswith("rejected"))
        self.assertIn("ANF degree", rows["REJECT-DCP-SS-BOUNDED-DEGREE-CARRY"].rejection_reason)
        self.assertIn("exponential", rows["REJECT-DCP-SS-KNOWN-QUANTUM-EXPONENT"].rejection_reason)

    def test_high_variance_hybrids_survive_only_as_proof_debt(self):
        rows = {item.hypothesis_id: item for item in synthesize_solver_hypotheses()}
        hybrid = rows["HYP-DCP-SS-TWO-ADIC-LATTICE-PRECONDITIONER"]
        self.assertEqual(hybrid.preflight_status, "proposal-only-proof-debt")
        self.assertTrue(any("inverse-polynomial" in item for item in hybrid.proof_obligations))
        self.assertTrue(hybrid.falsifiers)
        self.assertIn("conditioned-high-bit-quotient", hybrid.primitive_ids)
        self.assertIn("carry-sliced-quotient-lattice", hybrid.primitive_ids)

    def test_conditioned_quotient_is_typed_as_open_implicit_decoder_primitive(self):
        primitives = {item.primitive_id: item for item in build_solver_primitives()}
        quotient = primitives["conditioned-high-bit-quotient"]
        self.assertIn("implicit decoder", quotient.interface_status)
        self.assertIn("explicit polynomial quotient lists", quotient.resource_status)

    def test_symmetric_lift_retargets_general_quantum_route_to_solver_construction(self):
        primitives = {item.primitive_id: item for item in build_solver_primitives()}
        interface = primitives["coherent-matching-interface"]
        hypothesis = {
            item.hypothesis_id: item for item in synthesize_solver_hypotheses()
        }["HYP-DCP-SS-COHERENT-PARTIAL-SOLVER-BRIDGE"]
        self.assertIn("shared-seed randomness proved compatible", interface.interface_status)
        self.assertIn("paired-workspace fidelity", interface.interface_status)
        self.assertIn("coherent-matching-interface", hypothesis.primitive_ids)
        self.assertIn("symmetric-quantum-relation-lift", hypothesis.primitive_ids)
        self.assertTrue(any("seventh-power" in item for item in hypothesis.proof_obligations))
        self.assertFalse(any("workspace overlap" in item for item in hypothesis.proof_obligations))

    def test_blind_odd_unit_orbit_is_rejected_but_analytic_odd_part_route_remains(self):
        primitives = {item.primitive_id: item for item in build_solver_primitives()}
        hypotheses = {item.hypothesis_id: item for item in synthesize_solver_hypotheses()}
        primitive = primitives["source-preserving-random-self-reduction"]
        rejected = hypotheses["REJECT-DCP-SS-BLIND-ODD-UNIT-ORBIT-LLL"]
        hypothesis = hypotheses["HYP-DCP-SS-ODD-PART-ORBIT-CERTIFICATE"]
        self.assertIn("signs are isometric controls", primitive.interface_status)
        self.assertIn("source-preserving-random-self-reduction", hypothesis.primitive_ids)
        self.assertTrue(rejected.preflight_status.startswith("rejected"))
        self.assertIn("0/256", rejected.rejection_reason)
        self.assertTrue(any("unit-orbit" in item for item in hypothesis.proof_obligations))
        self.assertEqual(hypothesis.preflight_status, "proposal-only-proof-debt")

    def test_nongeneric_representation_hypothesis_uses_source_target_law(self):
        rows = {item.hypothesis_id: item for item in synthesize_solver_hypotheses()}
        hypothesis = rows["HYP-DCP-SS-NONGENERIC-REPRESENTATION-COLLAPSE"]
        self.assertIn("source-target-representation-law", hypothesis.primitive_ids)
        self.assertTrue(any("size-biased" in item for item in hypothesis.falsifiers))

    def test_report_accepts_no_candidate_without_theorems(self):
        report = run_subset_sum_solver_synthesis()
        self.assertGreater(report.headline_metrics["proposal_only_survivor_count"], 0)
        self.assertGreater(report.headline_metrics["negative_match_rejection_count"], 0)
        self.assertEqual(report.headline_metrics["accepted_candidate_count"], 0)
        self.assertFalse(report.claim_gate["candidate_records_accepted"])

    def test_writer_records_artifact_and_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_subset_sum_solver_synthesis()
                artifact_exists = Path("research/hypotheses/dcp_subset_sum_solver_synthesis.json").exists()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["accepted_candidate_count"], 0)
        self.assertTrue(
            any(item["id"] == "NEG-DCP-SUBSET-SUM-SOLVER-SYNTHESIS-WEAK-MUTATIONS" for item in negatives)
        )


if __name__ == "__main__":
    unittest.main()
