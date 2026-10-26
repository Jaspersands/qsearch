"""Tests for theorems/full_jet_channel_and_logical_gap_audit.py (Milestone 19)."""
from __future__ import annotations

import json
import numpy as np
import pytest

from theorems.full_jet_channel_and_logical_gap_audit import (
    JSON_PATH,
    MD_PATH,
    audit_logical_gate_access_matched_baselines,
    build_full_jet_channel_and_logical_gap_report,
    certify_population_singular_value_gap,
    render_markdown,
    verify_class_three_partial_fourier_density_contraction,
    verify_full_jet_alignment_spectator_density_branch,
    verify_full_taylor_transport_mixed_branch_density_contraction,
)


def test_class_three_partial_fourier_density_contraction() -> None:
    res = verify_class_three_partial_fourier_density_contraction(p=5)
    assert res["unitarity_frobenius_error"] < 1e-12
    assert res["max_sector_action_frobenius_error"] < 1e-12
    assert res["max_cross_sector_frobenius_error"] < 1e-12
    assert res["sector_marginal_probabilities"] == pytest.approx([0.2] * 5)
    assert res["max_nonzero_lambda_mu_traced_frobenius_norm"] < 1e-12


def test_full_jet_alignment_spectator_density_branch_retains_top_degree() -> None:
    res = verify_full_jet_alignment_spectator_density_branch(p=5, degree=2)
    assert res["class_two_carrier_width_R"] == 8
    assert res["class_two_jet_width_J"] == 6
    assert res["scalar_split_carrier_width_R"] == 4
    assert res["scalar_split_jet_width_J"] == 3
    assert res["scalar_split_spectator_width_S"] == 1
    assert res["includes_top_degree_k_eq_D"] is True
    assert res["spectator_branch_traces"] == pytest.approx([0.2] * 5)
    assert res["max_spectator_branch_frobenius_error"] < 1e-13


def test_full_taylor_transport_mixed_branch_density_contraction_and_fourier_residual() -> None:
    res = verify_full_taylor_transport_mixed_branch_density_contraction(p=5, degree=2)
    assert res["hilbert_dim_V_times_J"] == 625
    assert res["mixed_branch_frobenius_error"] < 1e-14
    assert res["max_fourier_residual_frobenius_error"] < 1e-13
    assert res["max_residual_polynomial_degree"] == 2
    assert res["attains_top_degree_D_on_k_eq_D_fourier_character"] is True


def test_population_singular_value_gap_certifier_and_rejection_guards() -> None:
    d, p = 4, 5
    omega = np.exp(2j * np.pi / p)
    v_bal = np.zeros((d * p, d), dtype=complex)
    for x in range(d):
        v_bal[p * x + (x % 2), x] = 1.0
    a_flag = np.diag([omega ** flag for _ in range(d) for flag in range(p)])
    b_id = np.eye(d, dtype=complex)
    cert = certify_population_singular_value_gap(
        v_bal,
        a_flag,
        b_id,
        alpha=0.5,
        eta=float(abs(omega - 1.0) / 2.0),
    )
    assert cert.bound_satisfied is True
    assert cert.exact_gap_gamma >= cert.population_lower_bound_gamma

    # If we claim an impossibly large singular value threshold eta = 1.99, bound_satisfied is False
    cert_bad = certify_population_singular_value_gap(
        v_bal,
        a_flag,
        b_id,
        alpha=1.0,
        eta=1.99,
    )
    assert cert_bad.bound_satisfied is False

    # Reject non-isometry V
    with pytest.raises(ValueError, match="isometry"):
        certify_population_singular_value_gap(
            2.0 * v_bal,
            a_flag,
            b_id,
            alpha=0.5,
            eta=0.1,
        )

    # Reject out-of-range alpha
    with pytest.raises(ValueError, match="alpha"):
        certify_population_singular_value_gap(
            v_bal,
            a_flag,
            b_id,
            alpha=1.5,
            eta=0.1,
        )


def test_audit_logical_gate_access_matched_baselines() -> None:
    audit = audit_logical_gate_access_matched_baselines(p=5)
    rows = audit["marked_vs_balanced_population_gap_table"]
    assert len(rows) == 3
    # Marked encoder gap shrinks with d, while balanced population-separated gap stays constant!
    assert rows[0]["marked_exact_gamma"] > rows[1]["marked_exact_gamma"] > rows[2]["marked_exact_gamma"]
    assert rows[0]["balanced_exact_gamma"] == pytest.approx(rows[2]["balanced_exact_gamma"])
    assert all(r["balanced_bound_satisfied"] for r in rows)
    assert audit["conjugated_pauli_heisenberg_nilpotency_class"] == 2
    assert audit["pauli_conjugation_raises_nilpotency_class"] is False
    assert audit["nonnormal_diagonal_fiber_vertical_kernel_dim"] == 1


def test_written_artifacts_match_report_schema() -> None:
    report = build_full_jet_channel_and_logical_gap_report()
    assert report["schema_version"] == "full_jet_channel_and_logical_gap_audit_v1"
    assert report["scope"]["accepted_speedup_candidate"] is False
    assert report["scope"]["novelty_claim"] is False
    assert report["scope"]["speedup_claim_allowed"] is False
    md = render_markdown(report)
    assert "Full-Jet Hilbert-Space Channel Contraction" in md
    if JSON_PATH.exists():
        on_disk = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert on_disk["schema_version"] == "full_jet_channel_and_logical_gap_audit_v1"
    if MD_PATH.exists():
        assert "accepted_speedup_candidate" in MD_PATH.read_text(encoding="utf-8")
