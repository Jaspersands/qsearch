"""Scoped identities and counterexamples to an overbroad phase-bank no-go."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pytest
from sympy import Rational

import theorems.native_history_erasure_dequantization as module
from theorems.native_history_erasure_dequantization import (
    ARCHIVE, NEGATIVE_RESULT_ID, REGISTRY, REPORT, build_report,
    evaluate_path_parameters, exact_history_countercontrols,
    quarantine_unsupported_negative, verify_finite_coherence_vanishing,
)


@pytest.mark.parametrize("n,q,M,W,seed", [(2, 9, 4, 4, 42), (2, 9, 4, 4, 999), (3, 27, 9, 3, 77)])
def test_discarded_explicit_history_identity_is_kept_but_scoped(n, q, M, W, seed):
    record = verify_finite_coherence_vanishing(n, q, M, W, seed)
    assert record["max_off_diagonal_coherence"] == 0
    assert record["trace_distance_to_classical_bkw"] < 1e-14
    assert abs(record["density_matrix_trace"] - 1) < 1e-12
    assert record["all_paths_satisfy_cauchy_schwarz"]
    assert record["noise_inflation_lower_bound_satisfied"]
    assert not record["arbitrary_interleaved_receiver_or_joint_readout_covered"]
    assert "frequency marginal only" in record["scope"]


def test_complete_joint_readout_and_untagged_circuit_disagree_with_marginal_inference():
    controls = exact_history_countercontrols()["phase_and_joint_readout_controls"]
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    for row in controls:
        phase = np.exp(2j * np.pi * row["secret_first_coordinate"] / 9)
        untagged = H @ np.diag([1, phase]) @ H @ np.array([1, 0])
        tagged = np.array([1, 0, 0, phase]) / np.sqrt(2)
        joint = np.kron(H, H) @ tagged
        density = np.outer(tagged, tagged.conjugate()).reshape(2, 2, 2, 2)
        reduced = np.trace(density, axis1=1, axis2=3)
        assert np.allclose(reduced, np.eye(2) / 2)
        expected = float(Rational(row["joint_X_parity_even_probability_exact"]))
        assert abs(abs(untagged[0]) ** 2 - expected) < 1e-14
        assert abs(sum(abs(joint[i]) ** 2 for i in (0, 3)) - expected) < 1e-14
        assert row["clean_history_erasure_performed"] is False
    assert [r["joint_X_parity_even_probability_exact"] for r in controls] == ["1", "1/4"]


def test_source_fiber_eraser_does_not_violate_basiswise_unitarity():
    record = exact_history_countercontrols()["source_fiber_erasure"]
    A = np.array(record["public_matrix_A"])
    c1, c2 = map(np.array, record["history_exponent_paths"])
    assert not np.array_equal(c1, c2)
    assert np.array_equal(A @ c1 % 9, A @ c2 % 9)
    assert record["source_state_after_H"] == ["1", "0"]
    assert record["orthogonal_basis_image_overlap_exact"] == "0"
    assert not record["basiswise_many_to_one_erasure_possible"]
    assert not record["unique_basis_history_necessary_for_source_state_erasure"]
    assert not record["arbitrary_noisy_fiber_eraser_or_ISIS_solver_supplied"]


def test_full_native_QFT_of_bounded_fiber_has_mass_outside_dual_rowspace():
    record = exact_history_countercontrols()["bounded_history_QFT_countercontrol"]
    q, M = record["q"], record["M"]
    source = np.zeros((q,) * M, dtype=complex)
    source[1, 0, 0, 0] = source[0, 1, 0, 0] = 1 / np.sqrt(2)
    output = np.fft.ifftn(source, norm="ortho")
    point = tuple(record["Fourier_outcome_outside_rowspace"])
    assert point[0] != point[1] or point[2] != point[3]
    expected = float(Rational(record["outside_rowspace_probability_exact"]))
    assert expected > 0 and abs(abs(output[point]) ** 2 - expected) < 1e-16
    assert abs(float(np.sum(abs(output) ** 2)) - 1) < 1e-14
    assert record["outside_rowspace_probability_exact"] == "1/13122"
    assert not record["full_uniform_coset_identity_refuted"]


@pytest.mark.parametrize("n", [2, 3, 8, 64])
def test_parameter_arithmetic_never_assigns_hardness_from_a_ratio(n):
    row = evaluate_path_parameters(n)
    assert row["bank_size_M"] == row["exposure_W"] == n ** 2
    assert Rational(row["modulus_to_path_bound_ratio"]) == Rational(3 ** n, n ** 2)
    assert row["fixed_path_L1_equals_W_required_for_noise_bound"]
    assert not row["hardness_reduction_verified"]
    assert not row["general_history_eraser_implies_classical_ISIS_solver"]
    assert not row["arbitrary_receiver_dequantized"]
    assert "isis_hard_regime" not in row and "history_erasure_requires_gapsvp_oracle" not in row


def test_corrected_live_report_and_source_replay():
    report = json.loads(REPORT.read_text())
    assert report == build_report()
    assert report["status"] == "UNIVERSAL_HISTORY_ERASURE_NO_GO_RETRACTED"
    assert report["source_sha256"] == hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
    assert not report["speedup_claim_allowed"] and not report["general_no_go_claim_allowed"]
    assert not report["accepted_speedup_candidate"]
    assert len(report["scoped_identities"]) == 2
    assert all(row["verified"] for row in report["scoped_identities"])
    assert len(report["retracted_implications"]) == 6


def isolated_registry(tmp_path, monkeypatch):
    original = {"id": NEGATIVE_RESULT_ID, "claim": "overbroad claim", "source": "old evidence"}
    active, archive = tmp_path / "active.json", tmp_path / "archive.json"
    active.write_text(json.dumps([original, {"id": "unrelated"}]))
    archive.write_text("[]")
    monkeypatch.setattr(module, "REGISTRY", active)
    monkeypatch.setattr(module, "ARCHIVE", archive)
    return original, active, archive


def test_quarantine_preserves_complete_original_and_is_idempotent(tmp_path, monkeypatch):
    original, active, archive = isolated_registry(tmp_path, monkeypatch)
    quarantine_unsupported_negative()
    saved = json.loads(archive.read_text())
    assert len(saved) == 1 and saved[0]["original_record"] == original
    assert saved[0]["reinstatement_requires_scoped_mathematical_review"]
    assert json.loads(active.read_text()) == [{"id": "unrelated"}]
    before = active.read_bytes(), archive.read_bytes()
    quarantine_unsupported_negative()
    assert before == (active.read_bytes(), archive.read_bytes())


def test_changed_reintroduced_claim_fails_closed(tmp_path, monkeypatch):
    original, active, archive = isolated_registry(tmp_path, monkeypatch)
    quarantine_unsupported_negative()
    changed = original | {"claim": "new evidence requires review"}
    active.write_text(json.dumps([changed]))
    before = active.read_bytes(), archive.read_bytes()
    with pytest.raises(ValueError, match="independent review"):
        quarantine_unsupported_negative()
    assert before == (active.read_bytes(), archive.read_bytes())


def test_concurrent_update_is_not_overwritten_after_archival(tmp_path, monkeypatch):
    original, active, archive = isolated_registry(tmp_path, monkeypatch)
    import core.research_registry as registry
    real_write = registry._write_json

    def changed_after_archive(path, value):
        real_write(path, value)
        if path == archive:
            active.write_text(json.dumps([original, {"id": "concurrent"}]))

    monkeypatch.setattr(registry, "_write_json", changed_after_archive)
    with pytest.raises(ValueError, match="after archival"):
        quarantine_unsupported_negative()
    assert json.loads(archive.read_text())[0]["original_record"] == original
    assert json.loads(active.read_text())[-1]["id"] == "concurrent"


def test_live_registry_excludes_only_the_reviewed_negative():
    active, archive = json.loads(REGISTRY.read_text()), json.loads(ARCHIVE.read_text())
    assert all(row["id"] != NEGATIVE_RESULT_ID for row in active)
    saved = [row for row in archive if row["id"] == NEGATIVE_RESULT_ID]
    assert len(saved) == 1 and saved[0]["original_record"]["id"] == NEGATIVE_RESULT_ID
    assert saved[0]["status"] == "QUARANTINED_OVERBROAD_NO_GO"
