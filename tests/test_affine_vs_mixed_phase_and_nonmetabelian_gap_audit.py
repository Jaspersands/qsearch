"""Tests for theorems/affine_vs_mixed_phase_and_nonmetabelian_gap_audit.py (Milestone 26)."""
from __future__ import annotations

import json

from theorems.affine_vs_mixed_phase_and_nonmetabelian_gap_audit import (
    JSON_PATH,
    MD_PATH,
    build_affine_vs_mixed_phase_and_nonmetabelian_gap_report,
    render_markdown,
    verify_metabelian_vs_nonmetabelian_orbit_gap_scope,
    verify_mixed_coherence_diagonal_blindness_vs_parallel_affine_erasure,
    verify_pure_affine_support_reduction_and_unidentifiability,
)


def test_pure_affine_support_reduction_and_unidentifiability() -> None:
    res = verify_pure_affine_support_reduction_and_unidentifiability(p=7)
    assert res["ambient_nonconstant_monomials"] == 19
    assert res["restricted_nonconstant_monomials"] == 9
    assert res["f1_and_f2_agree_on_affine_support"] is True
    assert res["f1_and_f2_differ_on_outside_points"] == 294
    assert res["pure_state_trace_distance_between_f1_and_f2"] == 0.0
    assert res["learned_support_basis_matches_exact_u"] is True
    assert res["learning_frame_eliminated_parameters"] == 9
    assert res["learning_frame_recovered_restricted_polynomial_exactly"] is True


def test_mixed_coherence_diagonal_blindness_vs_parallel_affine_erasure() -> None:
    res = verify_mixed_coherence_diagonal_blindness_vs_parallel_affine_erasure(p=11)
    assert res["computational_measurement_tvd_from_uniform"] == 0.0
    assert res["u_zero_trace_distance_across_distinct_f"] == 0.0
    assert res["final_erased_packet_degree"] == 0
    assert res["final_state_phase_spread_on_u"] < 1e-12
    assert res["qft_support_matches_u_perp"] is True
    assert res["recovered_u_basis_matches_exact_u"] is True


def test_metabelian_vs_nonmetabelian_orbit_gap_scope() -> None:
    res = verify_metabelian_vs_nonmetabelian_orbit_gap_scope(p=7)
    assert res["translation_phase_derived_translations_all_zero"] is True
    assert res["translation_phase_derived_is_abelian"] is True
    assert res["ut5_derived_dimension"] == 6
    assert res["ut5_second_derived_dimension"] == 1
    assert res["ut5_derived_is_abelian"] is False
    assert res["analytic_cauchy_schwarz_gap_fraction"] == "3/14"
    assert res["empirical_gap_exceeds_analytic_bound"] is True


def test_written_artifacts_match_report_schema() -> None:
    report = build_affine_vs_mixed_phase_and_nonmetabelian_gap_report()
    assert report["schema_version"] == "affine_vs_mixed_phase_and_nonmetabelian_gap_audit_v1"
    scope = report["scope"]
    assert scope["promotes_polynomial_phase_as_rees_application"] is False
    assert scope["classical_dequantization_claim"] is False
    assert scope["coherent_quantum_receiver_implemented"] is False
    assert scope["accepted_speedup_candidate"] is False
    assert scope["novelty_claim"] is False
    assert scope["speedup_claim_allowed"] is False
    md = render_markdown(report)
    assert "Pure-Affine vs Mixed-Coherence" in md
    if JSON_PATH.exists():
        on_disk = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert on_disk["schema_version"] == "affine_vs_mixed_phase_and_nonmetabelian_gap_audit_v1"
    if MD_PATH.exists():
        assert "accepted_speedup_candidate = False" in MD_PATH.read_text(encoding="utf-8")
