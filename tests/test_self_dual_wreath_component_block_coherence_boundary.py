import numpy as np
import pytest

from self_dual_wreath_component_block_coherence_boundary import (
    audit_block_coherence_boundary,
    block_coherence_boundary_theorem,
    commuting_codimension_one_naimark_isometry,
    commuting_coherence_scaling_record,
    haar_isometry,
    run_component_block_coherence_boundary,
)


def test_commuting_counterfamily_has_extensive_unsigned_block_mass() -> None:
    r = 12
    control = audit_block_coherence_boundary(
        "COMMUTING",
        commuting_codimension_one_naimark_isometry(r),
        (1,) * (3 * r),
    )
    assert control.exact_block_coherence_boundary_verified
    assert control.block_coherence_positive
    assert control.distinct_noncrossing_positive
    assert control.minimum_positive_block_eigenvalue >= 0.25
    assert control.off_block_frobenius_energy > r / 2
    assert control.ordered_distinct_noncrossing_mass > r / 100
    assert control.crossing_cancels_noncrossing
    assert abs(control.ordered_commutator_gap) < 1e-10
    assert abs(control.direct_ordered_commutator_mass) < 1e-10


def test_haar_control_has_positive_crossing_gap() -> None:
    isometry = haar_isometry(24, 9, seed=41)
    control = audit_block_coherence_boundary(
        "HAAR",
        isometry,
        (4, 4, 4, 4, 4, 4),
    )
    assert control.exact_block_coherence_boundary_verified
    assert control.ordered_distinct_noncrossing_mass > 0
    assert control.ordered_distinct_crossing_mass > 0
    assert control.ordered_commutator_gap > 1e-4
    assert control.direct_ordered_commutator_mass > 1e-4


def test_off_block_and_commutator_identities_hold_for_unequal_blocks() -> None:
    isometry = haar_isometry(19, 7, seed=97)
    control = audit_block_coherence_boundary(
        "UNEQUAL",
        isometry,
        (2, 3, 5, 4, 5),
    )
    assert control.exact_block_coherence_boundary_verified
    assert control.off_block_energy_identity_residual < 1e-10
    assert control.maximum_pair_noncrossing_norm_residual < 1e-10
    assert control.edge_lower_bound_residual < 1e-10
    assert control.commutator_identity_residual < 1e-10
    assert control.maximum_pair_zero_equivalence_failure == 0


def test_commuting_scaling_keeps_mass_but_zero_gap() -> None:
    rows = [commuting_coherence_scaling_record(r) for r in (4, 16, 64, 256)]
    assert all(row.off_block_coherence_extensive for row in rows)
    assert all(row.distinct_noncrossing_extensive for row in rows)
    assert all(not row.component_M4_positive for row in rows)
    assert rows[-1].normalized_off_block_frobenius_energy > 0.65
    assert rows[-1].normalized_ordered_distinct_noncrossing_mass > 0.06
    assert abs(rows[-1].normalized_commutator_gap) < 1e-12


def test_report_keeps_crossing_and_speedup_gates_closed() -> None:
    report = run_component_block_coherence_boundary()
    assert report.headline_metrics["block_coherence_identity_theorem_count"] == 1
    assert report.headline_metrics["off_block_coherence_sufficiency_no_go_count"] == 1
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert not report.claim_gate["natural_off_block_coherence_sufficient"]
    assert not report.claim_gate["natural_distinct_noncrossing_mass_sufficient"]
    assert not report.claim_gate["natural_crossing_separation_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_isometry_and_blocks_are_rejected() -> None:
    with pytest.raises(ValueError, match="orthonormal"):
        audit_block_coherence_boundary("BAD", np.ones((4, 2)), (2, 2))
    with pytest.raises(ValueError, match="sum"):
        audit_block_coherence_boundary("BAD", np.eye(4, 2), (1, 1, 1))
    with pytest.raises(ValueError, match="positive"):
        audit_block_coherence_boundary("BAD", np.eye(4, 2), (2, 0, 2))


def test_theorem_names_signed_crossing_gap_as_minimal_target() -> None:
    theorem = block_coherence_boundary_theorem()
    assert theorem.theorem_verified
    assert theorem.off_block_coherence_characterized
    assert theorem.distinct_noncrossing_characterized
    assert not theorem.off_block_coherence_implies_component_M4
    assert "does not lower-bound" in theorem.scope_limit
