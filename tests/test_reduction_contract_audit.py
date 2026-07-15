import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from dequantization_checks import write_dequantization_report
from reduction_contract_audit import build_reduction_contract_audit, write_reduction_contract_audit
from reduction_gate import evaluate_reduction_edge, reduction_edges_for_candidate, write_reduction_ledger
from reduction_theorem_catalog import seed_theorem_contracts, validate_theorem_contract
from research_registry import initialize_seed_registry, load_candidates


class ReductionContractAuditTests(unittest.TestCase):
    def test_primary_source_contracts_are_structured_and_valid(self):
        contracts = seed_theorem_contracts()

        self.assertEqual(len(contracts), 3)
        self.assertTrue(all(validate_theorem_contract(contract) == [] for contract in contracts))
        regev = next(contract for contract in contracts if contract.id == "THM-REGEV-USVP-TO-DCP-2003")
        self.assertEqual(regev.source_problem, "theta-n-2.5-unique-svp")
        self.assertIn("independent-coset-state-samples", regev.target_access_supplied)
        self.assertIn("adversarial-bad-registers-at-rate-1-over-logN-to-f", regev.target_access_supplied)
        self.assertIn("M=2^(4n)", regev.parameter_map)
        self.assertTrue(any("not automatically" in item for item in regev.limitations))

    def test_literature_edge_must_match_exact_theorem_contract(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                hidden = next(candidate for candidate in load_candidates() if "dihedral-hsp" in candidate["ontology_node_ids"])
                upstream = reduction_edges_for_candidate(hidden)[0]
                accepted = evaluate_reduction_edge(upstream)
                mismatched = evaluate_reduction_edge(replace(upstream, source_problem="exact-svp"))
            finally:
                os.chdir(old_cwd)

        self.assertTrue(accepted.accepted)
        self.assertFalse(mismatched.accepted)
        self.assertIn("source_problem", {issue.field for issue in mismatched.issues})

    def test_state_native_hidden_shift_access_passes_while_family_and_coset_gaps_remain(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                report = build_reduction_contract_audit()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["certified_interface_count"], 0)
        self.assertEqual(report["blocked_interface_count"], report["route_audit_count"])
        hidden_audits = [audit for audit in report["audits"] if "DHS" in audit["candidate_id"] or "HIDDEN-SHIFT" in audit["candidate_id"]]
        self.assertTrue(hidden_audits)
        primary_hidden = next(audit for audit in hidden_audits if audit["candidate_id"] == "DHS-GOWERS-SIEVE")
        hidden_access = next(check for check in primary_hidden["checks"] if check["axis"] == "access-model")
        hidden_coverage = next(check for check in primary_hidden["checks"] if check["axis"] == "full-family-coverage")
        hidden_bad_registers = next(
            check for check in primary_hidden["checks"] if check["axis"] == "bad-register-robustness"
        )
        self.assertTrue(hidden_access["passed"])
        self.assertFalse(hidden_coverage["passed"])
        self.assertFalse(hidden_bad_registers["passed"])
        coset_audits = [audit for audit in report["audits"] if audit not in hidden_audits]
        self.assertTrue(
            any(
                any(check["axis"] == "access-model" and check["passed"] for check in audit["checks"])
                and any(check["axis"] == "full-family-coverage" and not check["passed"] for check in audit["checks"])
                for audit in coset_audits
            )
        )

    def test_write_audit_feeds_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_reduction_ledger()
                payload = write_reduction_contract_audit()
                dequantization = write_dequantization_report()
                catalog_exists = Path("research/reductions/theorem_contracts.json").exists()
                audit_exists = Path("research/reductions/interface_audit.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(catalog_exists)
        self.assertTrue(audit_exists)
        self.assertEqual(payload["status"], "candidate-interfaces-blocked")
        self.assertTrue(
            any(
                finding["target_type"] == "reduction_contract_interface"
                for finding in dequantization["findings"]
            )
        )


if __name__ == "__main__":
    unittest.main()
