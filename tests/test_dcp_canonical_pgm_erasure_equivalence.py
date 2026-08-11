import pytest

from dcp_canonical_pgm_erasure_equivalence import (
    audit_canonical_analysis,
    audit_outcome_garbage_visibility,
    canonical_analysis_matrix,
    canonical_pgm_erasure_theorem,
    run_canonical_pgm_erasure_equivalence,
)


def test_canonical_analysis_is_exact_fiber_erasure() -> None:
    control = audit_canonical_analysis(16, (0, 1, 4, 7, 11, 15))
    assert control.effect_completeness_residual < 1e-10
    assert control.analysis_isometry_residual < 1e-10
    assert control.qft_erasure_residual < 1e-10
    assert control.inverse_fiber_preparation_residual < 1e-10
    assert control.exact_equivalence_verified


def test_support_contract_rejects_duplicates_and_noncanonical_residues() -> None:
    with pytest.raises(ValueError, match="nonempty"):
        canonical_analysis_matrix(8, ())
    with pytest.raises(ValueError, match="distinct"):
        canonical_analysis_matrix(8, (1, 1))
    with pytest.raises(ValueError, match="canonical"):
        canonical_analysis_matrix(8, (1, 8))


def test_common_garbage_preserves_fourier_erasure() -> None:
    control = audit_outcome_garbage_visibility(8, 3, "common")
    assert control.minimum_pairwise_garbage_overlap == pytest.approx(1.0)
    assert control.target_residue_probability_after_qft == pytest.approx(1.0)
    assert control.target_probability_after_cleanup == pytest.approx(1.0)


def test_orthogonal_garbage_blocks_coherence_until_cleaned() -> None:
    control = audit_outcome_garbage_visibility(8, 3, "orthogonal")
    assert control.maximum_pairwise_garbage_overlap == pytest.approx(0.0)
    assert control.target_residue_probability_after_qft == pytest.approx(1 / 8)
    assert control.target_probability_after_cleanup == pytest.approx(1.0)


def test_theorem_does_not_claim_arbitrary_channel_reduction() -> None:
    theorem = canonical_pgm_erasure_theorem()
    assert theorem.canonical_pgm_erasure_equivalence_proved
    assert theorem.cleanable_rank_one_dilation_equivalence_proved
    assert not theorem.arbitrary_destructive_pgm_reduced
    assert not theorem.inaccessible_environment_recovered
    assert not theorem.polynomial_witness_solver_constructed


def test_report_keeps_noncanonical_boundary_open() -> None:
    report = run_canonical_pgm_erasure_equivalence()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "canonical_coherent_pgm_route_is_solver_equivalent"
    ]
    assert report.claim_gate[
        "cleanable_rank_one_pgm_route_is_solver_equivalent"
    ]
    assert not report.claim_gate["arbitrary_destructive_pgm_route_closed"]
    assert not report.claim_gate["inaccessible_environment_route_closed"]
    assert not report.claim_gate["speedup_claim_allowed"]
