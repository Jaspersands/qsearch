"""Tests for theorems/rees_cover_and_nontransverse_descent_audit.py (Milestone 25)."""
from __future__ import annotations

import json

from theorems.rees_cover_and_nontransverse_descent_audit import (
    JSON_PATH,
    MD_PATH,
    build_rees_cover_and_nontransverse_descent_report,
    render_markdown,
    verify_bezout_sde_fail_closed_and_rank_arity_contract,
    verify_nontransverse_rees_descent_and_translation_order,
    verify_outer_reduction_falsifiers_and_resource_envelopes,
    verify_rees_cover_dimension_optimality_and_associated_graded_loss,
)


def test_rees_cover_dimension_optimality_and_associated_graded_loss() -> None:
    res = verify_rees_cover_dimension_optimality_and_associated_graded_loss()
    assert res["ut4_gamma_dimensions"] == [6, 3, 1]
    assert res["ut4_rees_cover_dimension"] == 10
    assert res["carnot_grade1_generates_all_grades"] is True
    assert res["derived_hidden_subalgebra_dim"] == 2
    assert res["associated_graded_grade1_hidden_dim"] == 0
    assert res["rees_cover_grade1_hidden_dim"] == 2
    assert res["rees_cover_lifted_grade_dims"] == [2, 2, 1]
    assert res["fp_scalars_preserve_fp_subgroup_in_fp2"] is True
    assert res["extension_scalar_preserves_fp_subgroup_in_fp2"] is False
    assert res["class9_witness_rees_cover_dimension"] == 97


def test_bezout_sde_fail_closed_and_rank_arity_contract() -> None:
    res = verify_bezout_sde_fail_closed_and_rank_arity_contract()
    assert res["p5_degree2_bezout_solver_fails_closed"] is True
    assert res["p5_degree3_bijective_arity_rank1"] == 2
    assert res["p7_degree2_required_arity_rank1"] == 4
    assert res["p7_degree2_required_arity_rank2"] == 9
    assert res["p7_degree2_under_arity_fails_closed"] is True
    assert any(res["p7_degree2_rank1_weights"])
    assert any(res["p7_degree2_rank2_weights"])


def test_nontransverse_rees_descent_and_translation_order() -> None:
    res = verify_nontransverse_rees_descent_and_translation_order(p=5)
    assert res["nilpotency_class"] == 2
    assert res["central_descent_stages"] == 1
    assert res["rees_cover_size"] == 625
    assert res["grade1_quotient_size"] == 125
    cases = {c["subgroup_name"]: c for c in res["cases"]}
    assert cases["nonnormal_transverse"]["central_intersection_size_K2"] == 1
    assert cases["nonnormal_transverse"]["positive_mass_label_count"] == 5
    assert cases["pure_central_nontransverse"]["central_intersection_size_K2"] == 5
    assert cases["pure_central_nontransverse"]["positive_mass_label_count"] == 1
    assert cases["mixed_nontransverse"]["central_intersection_size_K2"] == 5
    assert cases["mixed_nontransverse"]["positive_mass_label_count"] == 1
    for c in res["cases"]:
        assert c["max_coefficient_allowed_trace_error"] < 1e-12
        assert c["quotient_coset_frobenius_error"] < 1e-13
        assert c["sde_witness_source"] == "exhaustive_scale_fixture_p5_test_only"
        assert c["recovered_basis_matches_exact_h"] is True
    lr = res["left_vs_right_translation_nonnormal_falsifier"]
    assert lr["right_translation_frobenius_error"] < 1e-13
    assert lr["left_translation_frobenius_error"] > 0.17
    assert lr["left_translation_off_diagonal_frobenius_norm"] < 1e-12
    assert lr["left_translation_breaks_nonnormal_coset_invariance"] is True


def test_outer_reduction_falsifiers_and_resource_envelopes() -> None:
    res = verify_outer_reduction_falsifiers_and_resource_envelopes()
    z25 = res["z25_omega1_once_falsifier"]
    assert z25["omega1_once_recovered_order"] == 5
    assert z25["two_step_outer_enlargement_recovered_order"] == 25
    assert z25["omega1_once_misses_higher_exponent_layers"] is True

    d4 = res["d4_small_prime_omega1_falsifier"]
    assert d4["omega1_element_count"] == 6
    assert d4["d4_omega1_is_subgroup"] is False

    comp = res["class9_witness_four_way_resource_comparison"]
    assert comp["single_image_multivariate_jet"]["original_queries_ceil_log2"] == 1763
    assert comp["whole_recovery_multivariate_jet"]["original_queries_ceil_log2"] == 2922
    assert comp["positive_rees_cover_core"]["original_queries_ceil_log2"] == 1573
    assert comp["positive_rees_cover_core"]["query_dimension_exponent"] == 145
    assert comp["conditional_black_box_large_prime_outer_envelope"]["query_dimension_exponent"] == 147
    assert comp["conditional_black_box_large_prime_outer_envelope"]["outer_reduction_implemented"] is False


def test_written_artifacts_match_report_schema() -> None:
    report = build_rees_cover_and_nontransverse_descent_report()
    assert report["schema_version"] == "rees_cover_and_nontransverse_descent_audit_v1"
    scope = report["scope"]
    assert scope["ut3_rees_descent_is_single_stage"] is True
    assert scope["multistage_rees_descent_tested_in_this_module"] is False
    assert scope["p5_degree2_witness_uses_exhaustive_test_fixture"] is True
    assert scope["bezout_sde_fail_closed_and_rank_arity_verified"] is True
    assert scope["formal_rees_draft_compiler_checked"] is False
    assert scope["coherent_quantum_receiver_implemented"] is False
    assert scope["outer_black_box_reduction_implemented"] is False
    assert scope["accepted_speedup_candidate"] is False
    assert scope["novelty_claim"] is False
    assert scope["speedup_claim_allowed"] is False
    md = render_markdown(report)
    assert "Single-Stage Class-2" in md
    if JSON_PATH.exists():
        on_disk = json.loads(JSON_PATH.read_text(encoding="utf-8"))
        assert on_disk["schema_version"] == "rees_cover_and_nontransverse_descent_audit_v1"
    if MD_PATH.exists():
        assert "accepted_speedup_candidate = False" in MD_PATH.read_text(encoding="utf-8")
