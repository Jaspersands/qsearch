import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
import pytest

from ternary_character_sdp_decoder import (
    DERIVATION, REPORT, audit_matrix, baseline_proposals, character_matrix, compile_model,
    coordinate_refine, decode, phase_round, reference_maximum, rounded_proposals,
    solve_relaxation, verify_fresh,
)
from ternary_covariant_noise import CovariantRecord, heldout_score


def honest(q=9):
    secret = (2, 4)
    rows = (((1, 0), (0, 1)), ((1, 1), (2, 1)), ((3, 4), (4, 5)))
    rows = tuple((tuple(x % q for x in a), tuple(x % q for x in c)) for a, c in rows)
    return tuple(CovariantRecord(a, c, tuple(sum(x*s for x, s in zip(v, secret)) % q for v in (a, c)), q)
                 for a, c in rows), secret


@pytest.mark.parametrize("q", [3, 9, 27, 81])
def test_actual_characters_satisfy_every_complete_difference_and_objective(q):
    records, secret = honest(q)
    secret = tuple(x % q for x in secret)
    model = compile_model(records)
    X = character_matrix(model, secret)
    audit = audit_matrix(model, X)
    assert audit["numerically_feasible"]
    assert audit["all_equal_difference_residual"] < 1e-12
    assert audit["objective_score"] == pytest.approx(len(records)*heldout_score(records, secret))
    assert audit["largest_eigenvalue_over_dimension"] == pytest.approx(1)
    assert model["complete_difference_entries"] == model["matrix_nodes"]**2


def test_node_quotient_and_all_constraints_read_labels_not_outcomes():
    records, _ = honest()
    changed = tuple(CovariantRecord(r.first, r.second, ((r.outcome[0]+1) % 9, (r.outcome[1]+2) % 9), 9) for r in records)
    a, b = compile_model(records), compile_model(changed)
    assert a["nodes"] == b["nodes"] and a["equalities"] == b["equalities"]
    assert not a["templates_read_outcomes"]
    assert not np.allclose(a["objective_matrix"], b["objective_matrix"])
    assert len(a["nodes"]) == len(set(a["nodes"])) <= a["formal_circuit_nodes"]


def test_unknown_rank_and_caps_do_not_solve_a_truncated_model():
    records = (CovariantRecord((0, 0), (0, 0), (0, 0), 9),)
    assert compile_model(records)["status"] == "UNKNOWN_NO_FULL_UNIT_ROW_BASIS"
    records, _ = honest()
    model = compile_model(records, max_matrix_nodes=2)
    assert model["status"] == "MATRIX_CAP_EXHAUSTED" and not model["partial_relaxation_solved"]
    assert not solve_relaxation(model)["solver_invoked"]
    assert compile_model(records, max_formal_nodes=2)["status"] == "FORMAL_CIRCUIT_CAP_EXHAUSTED"


def test_feasibility_and_rounding_refuse_corrupted_or_missing_matrices():
    records, secret = honest()
    model = compile_model(records)
    X = character_matrix(model, secret)
    X[0, 1] += .2
    audit = audit_matrix(model, X)
    assert not audit["numerically_feasible"]
    assert rounded_proposals(model, X)["status"] == "ROUNDING_REFUSED_INFEASIBLE_MATRIX"
    assert not audit_matrix(model, np.full(X.shape, np.nan))["numerically_feasible"]
    assert not audit_matrix(model, np.eye(2))["numerically_feasible"]


def test_exact_character_phase_rounding_recovers_through_composite_inverse():
    records, secret = honest()
    model = compile_model(records)
    X = character_matrix(model, secret)
    assert phase_round(model, X[:, 0]) == secret
    proposals = rounded_proposals(model, X, gaussian_draws=4, seed=28)
    assert proposals["proposals"] == (secret,)
    assert not proposals["rank_one_or_rounding_recovery_theorem"]


def test_complete_coordinate_work_and_baseline_are_truth_blind():
    records, _ = honest()
    starts = baseline_proposals(records, 6, 123)
    assert starts == baseline_proposals(records, 6, 123)
    output = coordinate_refine(records, starts, sweeps=2)
    assert output["training_score"] >= max(heldout_score(records, x) for x in starts)-1e-10
    assert output["complete_score_evaluations"] <= len(set(starts))*(1+9*2*2)
    assert output["runtime_polynomial_in_q_not_logq"]
    assert not output["training_truth_or_holdout_used"]
    cap = coordinate_refine(records, starts, max_root_values=3)
    assert cap["status"] == "ROOT_ENUMERATION_CAP_EXHAUSTED" and not cap["partial_coordinate_scan_used"]


def test_fresh_verification_is_not_training_or_reused_source_and_keeps_error_bound():
    records, secret = honest()
    output = verify_fresh(records, secret, ["fresh-a", "fresh-b", "fresh-c"], ["train-a"])
    assert output["threshold_passed"] and output["gate"]["tested_candidates"] == 1
    assert not output["distinct_IDs_prove_physical_IID_supply"]
    with pytest.raises(ValueError, match="disjoint fresh"):
        verify_fresh(records, secret, ["train-a", "b", "c"], ["train-a"])


def test_capped_reference_is_not_a_decoder_or_scaling_result():
    records, _ = honest()
    skipped = reference_maximum(records, max_secrets=5)
    assert skipped["status"] == "NOT_RUN_EXPONENTIAL_REFERENCE_CAP"
    assert not skipped["reference_used_by_decoder"]
    ref = reference_maximum(records)
    assert ref["best_score"] == pytest.approx(3)
    assert not ref["exhaustive_reference_is_scaling_evidence"]


@pytest.fixture(scope="module")
def solved_control():
    pytest.importorskip("cvxpy")
    records = (CovariantRecord((1,), (2,), (1, 2), 3),)
    return records, decode(records, ["physical-a"], gaussian_draws=2, max_iterations=3000)


def test_actual_SDP_positive_control_is_full_group_calibration_only(solved_control):
    records, result = solved_control
    assert result["status"] == "HEURISTIC_CANDIDATE_NOT_RECOVERY_THEOREM"
    assert result["candidate"] == (1,)
    assert result["model"]["full_group_saturation"]
    assert result["solver"]["audit"]["numerically_feasible"]
    assert not result["solver"]["dual_optimality_or_integrality_gap_certified"]
    assert not result["efficient_population_recovery_proved"]
    assert heldout_score(records, result["candidate"]) == pytest.approx(3)
    assert set(result["matched_nonSDP_baseline"]["initial_proposals"]).issubset(result["stronger_nonSDP_baseline"]["initial_proposals"])


def test_ancestor_validation_and_solver_iteration_caps_are_not_silently_ignored():
    records, _ = honest()
    with pytest.raises(ValueError, match="distinct nonempty"):
        decode(records, ["a", "a", "b"])
    with pytest.raises(ValueError, match="matrix node cap"):
        compile_model(records, max_matrix_nodes=True)
    with pytest.raises(ValueError, match="solver iteration cap"):
        solve_relaxation(compile_model(records), max_iterations=0)


def test_live_artifact_records_failures_and_no_unproved_algorithm_admission():
    report = json.loads(REPORT.read_text())
    assert report["derivation_sha256"] == hashlib.sha256(DERIVATION.read_bytes()).hexdigest()
    assert report["raw_failures_and_cap_exhaustions_retained"]
    assert not report["accepted_candidate_or_speedup"]
    assert not report["population_recovery_or_tightness_proved"]
    assert not report["algorithm_input_contains_truth"]
    assert not report["exact_PSD_dual_or_integrality_gap_certificates_supplied"]
    for control in report["native_controls"]:
        result = control["decoder"]
        assert control["charged_original_native_qutrits"] == len(control["training_records"])+len(control["heldout_records"])
        assert result["charged_training_qutrits"] == len(control["training_records"])
        assert set(map(tuple, result["matched_nonSDP_baseline"]["initial_proposals"])).issubset(set(map(tuple, result["stronger_nonSDP_baseline"]["initial_proposals"])))
        assert result["stronger_nonSDP_baseline"]["training_score"] >= result["matched_nonSDP_baseline"]["training_score"]-1e-9
        if result["candidate"] is not None:
            assert not control["fresh_verification"]["speedup_claim_allowed"]
            assert not result["solver"]["audit"]["exact_PSD_or_optimality_certificate"]


def test_independent_checker_replays_all_matrices_and_public_decoders():
    checker = Path(__file__).resolve().parents[1]/"research/certificates/ternary_character_sdp_decoder_crosscheck.js"
    output = subprocess.run(["node", str(checker)], check=True, capture_output=True, text=True)
    data = json.loads(output.stdout)
    assert data["status"] == "PASS" and data["matrix_entries_checked"] > 0
    assert not data["exact_PSD_optimality_or_population_recovery_certified"]
