import os
import tempfile
import unittest

from dcp_symmetric_relation_lift import (
    audit_symmetric_pair,
    best_regev_matching_probe,
    build_contamination_certificates,
    build_weighted_matching_certificate,
    run_symmetric_relation_lift_audit,
    verify_regev_source_sites,
    weighted_matching_mass,
    write_symmetric_relation_lift_audit,
)
from dcp_quantum_relation_fidelity import write_quantum_relation_fidelity_audit
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_frontier_map import build_frontier_map
from dcp_subset_sum_solver_synthesis import build_solver_primitives, synthesize_solver_hypotheses
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPSymmetricRelationLiftTests(unittest.TestCase):
    def test_primary_regev_structure_is_source_verified(self):
        sites = verify_regev_source_sites()
        self.assertEqual(len(sites), 4)
        self.assertTrue(all(site.verified for site in sites), sites)
        self.assertTrue(all(site.line_number > 0 for site in sites))
        self.assertTrue(all(site.evidence_sha256 for site in sites))

    def test_double_evaluation_equalizes_complex_amplitudes_and_garbage(self):
        pair = audit_symmetric_pair(
            10,
            13,
            "x",
            "y",
            {"x": 0.3 + 0.4j},
            {"y": -0.2 + 0.1j},
            "left-arbitrary-workspace",
            "right-different-workspace",
        )
        self.assertEqual(pair.amplitude_difference, 0.0)
        self.assertTrue(pair.ordered_workspace_equal)
        self.assertEqual(pair.paired_visibility, 1.0)
        self.assertEqual(pair.decision, "exact-symmetric-pair-state")

    def test_zero_relation_amplitude_fails_closed(self):
        pair = audit_symmetric_pair(1, 2, "x", "y", {}, {"y": 1.0}, "g0", "g1")
        self.assertEqual(pair.paired_visibility, 0.0)
        self.assertTrue(pair.decision.startswith("rejected"))

    def test_weighted_matching_mass_counts_each_edge_once(self):
        probabilities = [1.0, 1.0, 0.0, 0.0]
        self.assertEqual(weighted_matching_mass(probabilities, 1, 1), 1.0)
        self.assertEqual(weighted_matching_mass(probabilities, 1, 2), 0.0)

    def test_weighted_certificate_separates_fixed_and_global_losses(self):
        certificate = build_weighted_matching_certificate()
        self.assertEqual(certificate.fixed_list_polynomial_loss_exponent, 5)
        self.assertEqual(certificate.global_source_polynomial_loss_exponent, 7)
        self.assertIn("mu^5", certificate.weighted_matching_mass_lower_bound)
        self.assertIn("mu^7", certificate.global_source_routine_success_lower_bound)
        self.assertGreaterEqual(len(certificate.conditions), 7)

    def test_finite_adversarial_probability_profile_has_explicit_matching(self):
        probabilities = [0.4 if (t % 8) in {0, 1, 4, 5} else 0.01 for t in range(128)]
        probe = best_regev_matching_probe(probabilities)
        self.assertGreater(probe.threshold_support_size, 0)
        self.assertGreater(probe.matching_count, 0)
        self.assertGreater(probe.best_weighted_mass, 0.0)
        self.assertGreater(probe.normalized_routine_success, 0.0)

    def test_report_proves_interface_but_not_solver(self):
        report = run_symmetric_relation_lift_audit()
        metrics = report.headline_metrics
        self.assertEqual(metrics["coherent_relation_interface_certificate_count"], 1)
        self.assertEqual(metrics["deterministic_selector_required_count"], 0)
        self.assertEqual(metrics["proved_polynomial_relation_solver_count"], 0)
        self.assertEqual(metrics["global_source_weighted_matching_loss_exponent"], 7)
        self.assertEqual(metrics["product_contamination_composition_certificate_count"], 1)
        self.assertTrue(report.claim_gate["product_contamination_information_bound_composed"])
        self.assertTrue(report.claim_gate["general_purified_relation_solver_interface_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_product_contamination_retains_constant_all_good_weight(self):
        rows = build_contamination_certificates()
        self.assertTrue(all(row.constant_weight_regime for row in rows))
        self.assertGreater(min(row.all_good_probability_lower_bound for row in rows), 0.25)
        self.assertLess(max(row.all_good_probability_lower_bound for row in rows), 0.5)

    def test_writer_records_result_and_negative_controls(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_quantum_relation_fidelity_audit()
                write_symmetric_relation_lift_audit()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                frontier = build_frontier_map()
                primitives = build_solver_primitives()
                hypotheses = synthesize_solver_hypotheses()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(any(item["artifacts"].get("dcp_symmetric_relation_lift") for item in results))
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-DCP-ARBITRARY-RELATION-INCOMPATIBLE-WITH-MATCHING", negative_ids)
        self.assertIn("NEG-DCP-RELATION-LIFT-AS-SOLVER-CONSTRUCTION", negative_ids)
        finding = next(
            item
            for item in dequantization["findings"]
            if item["id"]
            == "DEQ-DCP-SYMMETRIC-RELATION-LIFT-SEPARATES-INTERFACE-FROM-SOLVER"
        )
        self.assertFalse(finding["blocks_speedup_claim"])
        direct_fidelity = next(
            item
            for item in dequantization["findings"]
            if item["id"] == "DEQ-DCP-QUANTUM-RELATION-WORKSPACE-FIDELITY"
        )
        self.assertFalse(direct_fidelity["blocks_speedup_claim"])
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-GENERAL-QUANTUM-RELATION-MATCHING-LIFT"]["status"],
            "proved-conditional-symmetric-double-evaluation",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-SYMMETRIC-RELATION-WEIGHTED-MATCHING"]["status"],
            "proved-conditional-product-contamination-composed",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-QUANTUM-RELATION-WORKSPACE-FIDELITY"]["status"],
            "bypassed-by-symmetric-double-evaluation-interface",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Symmetric double-evaluation" in item for item in query_record["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Symmetric relation lift", dcp_frontier["evidence"])
        self.assertIn("symmetric-quantum-relation-lift", {item.primitive_id for item in primitives})
        relation_hypothesis = next(
            item
            for item in hypotheses
            if item.hypothesis_id == "HYP-DCP-SS-COHERENT-PARTIAL-SOLVER-BRIDGE"
        )
        self.assertIn("symmetric-quantum-relation-lift", relation_hypothesis.primitive_ids)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_symmetric_lift(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-DCP-SYMMETRIC-RELATION-LIFT")
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result.status, "completed")
        self.assertIn("EXP-DHS-DCP-SYMMETRIC-RELATION-LIFT", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
