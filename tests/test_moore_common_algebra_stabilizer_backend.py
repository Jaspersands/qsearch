"""Tests for the common-matrix-algebra (J^nu = 0, nu <= p) Moore-form stabilizer
generator-recovery backend and polynomial-graph vs positive Rees cover audit.
"""

from __future__ import annotations

import pytest

from theorems.moore_common_algebra_stabilizer_backend import (
    build_moore_common_algebra_stabilizer_backend_report,
    compute_common_nonunital_algebra,
    recover_common_algebra_moore_stabilizer,
    verify_commuting_order_p_common_algebra_falsifier,
    verify_elementary_stabilizer_recovery_controls,
    verify_polynomial_graph_vs_rees_cover_prior_art,
)
from theorems.moore_gradient_filter import moore_circuit, recognize_moore_form
from theorems.ut5_matrix_phase_alignment import _identity


def test_commuting_order_p_common_algebra_falsifier_fails_closed():
    res = verify_commuting_order_p_common_algebra_falsifier()
    assert res["prime"] == 5
    assert res["dimension"] == 25
    assert res["generators_commute"] is True
    assert res["all_generators_order_dividing_p"] is True
    assert res["individual_x_fifth_power_zero"] is True
    assert res["individual_y_fifth_power_zero"] is True
    assert res["common_algebra_dimension"] == 24
    assert res["common_algebra_nilpotency_index"] == 9
    assert res["guard_passed"] is False
    assert res["guard_status"] == "COMMON_ALGEBRA_INDEX_EXCEEDS_PRIME"
    assert res["individual_truncated_logs_additive"] is False
    assert res["solver_fails_closed"] is True


def test_elementary_stabilizer_recovery_controls_ut3_ut4_ut3_sq_and_ut10():
    res = verify_elementary_stabilizer_recovery_controls()

    ut3 = res["ut3_f5"]
    assert ut3["status"] == "STABILIZER_GENERATORS_RECOVERED"
    assert ut3["nilpotency_index"] == 3
    assert ut3["ambient_lie_dimension"] == 3
    assert ut3["stabilizer_lie_dimension"] == 1
    assert ut3["group_order"] == 125
    assert ut3["recovered_subgroup_order"] == 5
    assert ut3["matches_exact_stabilizer_subgroup"] is True
    assert ut3["all_generators_fix_moore_form"] is True

    ut4 = res["conjugated_ut4_f7"]
    assert ut4["status"] == "STABILIZER_GENERATORS_RECOVERED"
    assert ut4["nilpotency_index"] == 4
    assert ut4["ambient_lie_dimension"] == 6
    assert ut4["stabilizer_lie_dimension"] == 2
    assert ut4["stabilizer_lie_is_subalgebra"] is True
    assert ut4["recovered_subgroup_order"] == 49
    assert ut4["all_recovered_elements_fix_moore_form"] is True

    ut3_sq = res["two_block_ut3_f5"]
    assert ut3_sq["status"] == "STABILIZER_GENERATORS_RECOVERED"
    assert ut3_sq["nilpotency_index"] == 3
    assert ut3_sq["ambient_lie_dimension"] == 6
    assert ut3_sq["stabilizer_lie_dimension"] == 2
    assert ut3_sq["group_order"] == 15625
    assert ut3_sq["recovered_subgroup_order"] == 25
    assert ut3_sq["matches_exact_stabilizer_subgroup"] is True

    ut10_m2 = res["two_block_ut10_f43"]
    assert ut10_m2["status"] == "STABILIZER_GENERATORS_RECOVERED"
    assert ut10_m2["algebra_dimension"] == 90
    assert ut10_m2["nilpotency_index"] == 10
    assert ut10_m2["ambient_lie_dimension"] == 90
    assert ut10_m2["stabilizer_lie_dimension"] == 72
    assert ut10_m2["stabilizer_lie_is_subalgebra"] is True
    assert ut10_m2["all_generators_fix_moore_form"] is True

    ut10_m5 = res["five_block_ut10_f43_canonical_lie_basis"]
    assert ut10_m5["proved_orbit_rank"] == 100000
    assert ut10_m5["ambient_lie_dimension"] == 225
    assert ut10_m5["stabilizer_lie_dimension"] == 180
    assert ut10_m5["all_180_exponentiated_generators_fix_moore_form"] is True


def test_nonnilpotent_and_unaccepted_contracts_fail_closed():
    # Diagonal non-unipotent generator g = diag(2, 1, 1) has g - I non-nilpotent
    g = ((2, 0, 0), (0, 1, 0), (0, 0, 1))
    guard = compute_common_nonunital_algebra(5, 3, (g,))
    assert guard.guard_passed is False
    assert guard.status == "COMMON_ALGEBRA_NONNILPOTENT"
    assert guard.nilpotency_index is None

    # Unaccepted recognition (zero circuit) fails closed
    unaccepted = recognize_moore_form(5, 3, [("const", 0)], seed=29)
    with pytest.raises(ValueError, match="accepted MooreRecognition"):
        recover_common_algebra_moore_stabilizer(unaccepted, (_identity(3),))


def test_polynomial_graph_vs_rees_cover_prior_art():
    res = verify_polynomial_graph_vs_rees_cover_prior_art()
    assert res["ambient_lie_dimension"] == 6
    assert res["rees_cover_dimension"] == 10
    assert res["naive_dilation_on_bare_lie_algebra_failures"] > 0
    assert res["naive_dilation_is_lie_automorphism"] is False
    assert res["rees_evaluation_homomorphism_failures"] == 0
    assert res["rees_evaluations_are_exact_lie_homomorphisms"] is True
    assert res["nonhomogeneous_line_recovered_in_rees_grade1"] is True
    assert res["central_line_rees_grade1_dim"] == 1
    assert res["central_line_associated_graded_grade1_dim"] == 0


def test_report_flags_remain_strictly_false():
    report = build_moore_common_algebra_stabilizer_backend_report()
    assert report["schema_version"] == "moore_common_algebra_stabilizer_backend_v1"
    scope = report["scope"]
    assert scope["elementary_common_algebra_backend_executed"] is True
    assert scope["common_j_nilpotency_guard_enforced"] is True
    assert scope["weak_order_p_or_abstract_class_guard_rejected"] is True
    for flag in (
        "quantum_copies_only_covered",
        "general_luks_group_stabilizer_implemented",
        "formal_proof_verified",
        "independently_reviewed",
        "accepted_speedup_candidate",
        "novelty_claim",
        "speedup_claim_allowed",
    ):
        assert scope[flag] is False
