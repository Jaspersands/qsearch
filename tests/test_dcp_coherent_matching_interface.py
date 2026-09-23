import os
import json
import tempfile
import unittest
from pathlib import Path

from dcp_coherent_matching_interface import (
    interference_visibility,
    run_coherent_matching_interface_audit,
    seeded_bridge_certificate,
    write_coherent_matching_interface_audit,
)
from research_registry import initialize_seed_registry, load_negative_results, load_experiment_results


class DCPCoherentMatchingInterfaceTests(unittest.TestCase):
    def test_workspace_overlap_exactly_controls_phase_visibility(self):
        self.assertAlmostEqual(interference_visibility([1, 0], [1, 0]), 1.0)
        self.assertAlmostEqual(interference_visibility([1, 0], [0, 1]), 0.0)
        self.assertAlmostEqual(interference_visibility([1, 0], [0.5, 3**0.5 / 2]), 0.5)

    def test_seeded_randomized_bridge_retains_inverse_polynomial_success(self):
        small = seeded_bridge_certificate(32, 2)
        large = seeded_bridge_certificate(64, 2)
        self.assertTrue(small.conditional_seeded_randomized_bridge_proved)
        self.assertGreater(small.routine_success_probability_lower_bound, 0.0)
        ratio = small.routine_success_probability_lower_bound / large.routine_success_probability_lower_bound
        self.assertLess(ratio, 2 ** (small.polynomial_success_exponent + 3))
        self.assertEqual(small.polynomial_success_exponent, 10)

    def test_report_keeps_conditional_interfaces_separate_from_solver_construction(self):
        report = run_coherent_matching_interface_audit(
            n_values=[16, 32], legal_coverage_exponents=[1, 2]
        )
        self.assertEqual(report.headline_metrics["proved_seeded_randomized_solver_bridge_count"], 4)
        self.assertEqual(report.headline_metrics["proved_arbitrary_quantum_relation_solver_bridge_count"], 0)
        self.assertGreater(report.headline_metrics["zero_visibility_counterexample_count"], 0)
        self.assertTrue(report.claim_gate["seeded_randomized_partial_solver_bridge_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertFalse(report.claim_gate["arbitrary_quantum_solvers_excluded"])
        self.assertTrue(report.claim_gate["pairing_finite_controls_passed"])
        self.assertEqual(report.headline_metrics["physical_pairing_control_count"], 9)
        self.assertEqual(report.headline_metrics["physical_permutation_control_count"], 2)
        self.assertEqual(report.headline_metrics["noise_mass_envelope_count"], 14)
        self.assertEqual(report.headline_metrics["explicit_exponential_pairing_finder_count"], 2)
        self.assertEqual(report.headline_metrics["affine_marked_program_control_count"], 3)
        self.assertEqual(report.headline_metrics["balanced_mitm_program_control_count"], 3)
        self.assertTrue(report.claim_gate["balanced_mitm_controls_passed"])
        self.assertTrue(report.claim_gate["coherent_edge_controls_passed"])
        self.assertEqual(report.headline_metrics["coherent_edge_physical_control_count"], 96)
        self.assertIn("double-evaluation", report.source_contract["quantum_obstruction"])

    def test_writer_records_general_quantum_interface_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_coherent_matching_interface_audit(
                    n_values=[16], legal_coverage_exponents=[1]
                )
                artifact_exists = Path(
                    "research/reductions/dcp_coherent_matching_interface.json"
                ).exists()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["proved_seeded_randomized_solver_bridge_count"], 1)
        self.assertTrue(
            any(
                item["id"]
                == "NEG-DCP-ARBITRARY-QUANTUM-RELATION-SOLVER-WITHOUT-WORKSPACE-OVERLAP"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()


def test_no_registry_option_writes_only_requested_artifact(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path/"audit.json"
    payload = write_coherent_matching_interface_audit(path=path, write_registry=False,
                                                     n_values=[16], legal_coverage_exponents=[1])
    assert path.exists()
    assert not (tmp_path/"research/registry").exists()
    assert json.loads(path.read_text())["pairing_programs"]["control_failures"] == 0
    assert payload["artifacts"]["dcp_coherent_matching_interface"] == str(path)


def test_writer_honors_custom_ids_and_updates_instead_of_duplicating(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for _ in range(2):
        write_coherent_matching_interface_audit(n_values=[16], legal_coverage_exponents=[1],
            registry_experiment_id="EXP-CUSTOM", registry_candidate_id="CUSTOM", registry_result_id="CUSTOM-RESULT")
    results = load_experiment_results()
    assert len(results) == 1
    assert results[0]["id"] == "CUSTOM-RESULT"
    assert results[0]["experiment_id"] == "EXP-CUSTOM"
    assert results[0]["candidate_id"] == "CUSTOM"
    negatives = load_negative_results()
    assert len(negatives) == 6
    assert all(item["applies_to"] == ["CUSTOM"] for item in negatives)


def test_runner_and_direct_writer_share_one_fresh_result(tmp_path, monkeypatch):
    from experiment_runner import run_experiment
    from research_registry import validate_registry
    monkeypatch.chdir(tmp_path)
    initialize_seed_registry()
    write_coherent_matching_interface_audit(n_values=[16], legal_coverage_exponents=[1])
    run = run_experiment("EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE")
    results = [r for r in load_experiment_results() if r["experiment_id"] == run.experiment_id]
    assert len(results) == 1
    assert results[0]["id"] == run.result_id
    assert results[0]["metrics"]["physical_pairing_failure_count"] == 0
    assert results[0]["metrics"]["seeded_bridge_certificate_count"] == 12
    assert validate_registry()["valid"]


def test_failed_controls_do_not_record_mathematical_negatives(tmp_path, monkeypatch):
    import dcp_coherent_matching_interface as audit
    real = audit.build_pairing_controls
    def failed():
        report = real()
        report["control_failures"] = 1
        return report
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(audit, "build_pairing_controls", failed)
    payload = audit.write_coherent_matching_interface_audit(n_values=[16], legal_coverage_exponents=[1])
    assert payload["status"] == "failed-physical-pairing-controls"
    assert payload["claim_gate"]["pairing_finite_controls_passed"] is False
    assert not load_negative_results()


def test_pairing_proof_records_require_literal_verified_gates(tmp_path, monkeypatch):
    from proof_tracker import _dcp_pairing_program_lemmas
    monkeypatch.chdir(tmp_path)
    records = _dcp_pairing_program_lemmas("DHS-GOWERS-SIEVE")
    assert len(records) == 6
    assert all(item.status.startswith("blocked") for item in records)
    payload = write_coherent_matching_interface_audit(write_registry=False,
                                                     n_values=[16], legal_coverage_exponents=[1])
    assert all("review-pending" in item.status for item in _dcp_pairing_program_lemmas("DHS-GOWERS-SIEVE"))
    payload["claim_gate"]["affine_marked_coverage_controls_passed"] = "false"
    Path("research/reductions/dcp_coherent_matching_interface.json").write_text(json.dumps(payload))
    records = _dcp_pairing_program_lemmas("DHS-GOWERS-SIEVE")
    assert all("review-pending" in item.status for item in records[:3])
    assert records[3].status.startswith("blocked")
    assert "review-pending" in records[4].status
    payload["claim_gate"]["balanced_mitm_controls_passed"] = "false"
    Path("research/reductions/dcp_coherent_matching_interface.json").write_text(json.dumps(payload))
    assert _dcp_pairing_program_lemmas("DHS-GOWERS-SIEVE")[4].status.startswith("blocked")
    assert "review-pending" in _dcp_pairing_program_lemmas("DHS-GOWERS-SIEVE")[5].status
    payload["claim_gate"]["coherent_edge_controls_passed"] = "false"
    Path("research/reductions/dcp_coherent_matching_interface.json").write_text(json.dumps(payload))
    assert _dcp_pairing_program_lemmas("DHS-GOWERS-SIEVE")[5].status.startswith("blocked")
    payload["claim_gate"]["pairing_finite_controls_passed"] = "false"
    Path("research/reductions/dcp_coherent_matching_interface.json").write_text(json.dumps(payload))
    assert all(item.status.startswith("blocked") for item in _dcp_pairing_program_lemmas("DHS-GOWERS-SIEVE"))


def test_new_scope_negatives_are_not_reported_as_classical_algorithms(tmp_path, monkeypatch):
    from dequantization_checks import findings_from_negative_results
    monkeypatch.chdir(tmp_path)
    write_coherent_matching_interface_audit(n_values=[16], legal_coverage_exponents=[1])
    findings = findings_from_negative_results([{"id": "DHS-GOWERS-SIEVE"}], load_negative_results())
    pairing = [item for item in findings if item.id.endswith(("DCP-RECIPROCAL-COVERAGE-CONTRACT", "DCP-PAIRING-NOISE-COVERAGE-CONTRACT"))]
    assert len(pairing) == 2
    assert all("not classical dequantization" in item.required_action for item in pairing)
    enumeration = next(item for item in findings if item.id.endswith("DCP-AFFINE-MARKED-ENUMERATION-COST"))
    assert "12D" in enumeration.evidence
    assert "not classical dequantization" in enumeration.required_action
    balanced = next(item for item in findings if item.id.endswith("DCP-BALANCED-MITM-RESOURCE-CONTRACT"))
    assert "coherent storage" in balanced.evidence
    assert "not classical dequantization" in balanced.required_action
    edge = next(item for item in findings if item.id.endswith("DCP-LIST-FREE-EDGE-TIME-CONTRACT"))
    assert "polynomial workspace" in edge.evidence
    assert "not a lower bound" in edge.required_action
