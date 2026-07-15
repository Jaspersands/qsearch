import os
import tempfile
import unittest
from pathlib import Path

from coset_recoupling_mechanism_synthesis import (
    TEMPLATES,
    build_recoupling_mechanism_synthesis_report,
    build_recoupling_mutation_proposals,
    evaluate_template,
    write_recoupling_mechanism_synthesis_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from mutation_engine import build_mutation_proposals
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_mutation_proposals,
    load_negative_results,
    validate_registry,
)


class RecouplingMechanismSynthesisTests(unittest.TestCase):
    def test_all_templates_have_valid_typed_stage_chains(self):
        for template in TEMPLATES:
            evaluation = evaluate_template(template)
            self.assertTrue(evaluation.typed_interfaces_valid, evaluation.interface_issues)
            self.assertTrue(evaluation.holevo_copy_budget_obligation_attached)
            self.assertIn("chi_1", evaluation.minimum_copy_budget_rule)

    def test_known_shortcuts_are_rejected(self):
        evaluations = {template.id: evaluate_template(template) for template in TEMPLATES}
        for mechanism_id in (
            "MECH-QFT-WEAK-LABELS",
            "MECH-PROJECTOR-COUNT-DECODER",
            "MECH-PAIR-TREE-RANK-PGM",
            "MECH-RESTRICTED-COMMUTING-CLASS",
        ):
            self.assertEqual(evaluations[mechanism_id].decision, "rejected")
            self.assertTrue(evaluations[mechanism_id].known_no_go_violations)

    def test_high_upside_architectures_remain_proposal_only(self):
        evaluations = {template.id: evaluate_template(template) for template in TEMPLATES}
        full = evaluations["MECH-FULL-RECOUPLING-TRANSITION-DECODER"]
        tensor = evaluations["MECH-TENSOR-ASSOCIATOR-DECODER"]
        commutant = evaluations["MECH-JM-LABEL-MULTIPLICITY-RECOUPLING"]
        self.assertEqual(full.decision, "proposal-only-missing-proof-capabilities")
        self.assertEqual(tensor.decision, "proposal-only-missing-proof-capabilities")
        self.assertFalse(full.proof_gate_eligible)
        self.assertIn("CAP-INTERNAL-SN-KRONECKER-TRANSFORM", full.missing_capabilities)
        self.assertIn("CAP-HIDDEN-INVOLUTION-OUTCOME-DECODER", full.missing_capabilities)
        self.assertIn(
            "CAP-GAPPED-KRONECKER-MULTIPLICITY-TRANSFORM",
            commutant.missing_capabilities,
        )

    def test_mutation_proposals_are_explicitly_not_gate_eligible(self):
        proposals = build_recoupling_mutation_proposals()
        self.assertEqual(len(proposals), 3)
        for proposal in proposals:
            self.assertFalse(proposal["proof_gate_eligible"])
            self.assertTrue(proposal["typed_stages"])
            self.assertTrue(proposal["proof_obligations_to_resolve"])

    def test_report_promotes_no_undefined_architecture(self):
        report = build_recoupling_mechanism_synthesis_report()
        self.assertEqual(report.headline_metrics["known_no_go_rejected_count"], 4)
        self.assertEqual(report.headline_metrics["proposal_only_count"], 3)
        self.assertEqual(report.headline_metrics["proof_gate_eligible_count"], 0)
        self.assertEqual(report.headline_metrics["automatically_promoted_candidate_count"], 0)
        self.assertEqual(report.headline_metrics["undercharged_mechanism_promoted_count"], 0)
        self.assertTrue(report.claim_gate["exact_holevo_copy_budget_attached"])
        self.assertFalse(report.claim_gate["undefined_circuit_boxes_promoted"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_propagates_typed_gate_to_research_ledgers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_recoupling_mechanism_synthesis_report()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                results = load_experiment_results()
                negatives = load_negative_results()
                mutations = load_mutation_proposals()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_recoupling_mechanism_synthesis.json"
                ).exists()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(item["artifacts"].get("coset_recoupling_mechanism_synthesis") for item in results)
        )
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-MECH-PAIR-TREE-RANK-PGM", negative_ids)
        self.assertEqual(len([item for item in mutations if item["mutation_type"] == "typed-recoupling-mechanism"]), 3)
        finding = next(
            item
            for item in dequantization["findings"]
            if item["id"] == "DEQ-COSET-TYPED-RECOUPLING-SHORTCUTS-REJECTED"
        )
        self.assertTrue(finding["blocks_speedup_claim"])
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-TYPED-RECOUPLING-MECHANISM"]["status"],
            "blocked-no-typed-proof-complete-mechanism",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(any("Typed recoupling synthesis" in item for item in query_record["blocking_evidence"]))
        self.assertEqual(payload["headline_metrics"]["proof_gate_eligible_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_and_mutation_engine_use_typed_synthesis(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                runner_result = run_experiment("EXP-COSET-RECOUPLING-MECHANISM-SYNTHESIS")
                proposals = build_mutation_proposals()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(runner_result.status, "completed")
        self.assertIn("EXP-COSET-RECOUPLING-MECHANISM-SYNTHESIS", supported_experiment_ids())
        typed = [item for item in proposals if item["mutation_type"] == "typed-recoupling-mechanism"]
        self.assertEqual(len(typed), 3)
        self.assertTrue(all(item["proof_gate_eligible"] is False for item in typed))
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
