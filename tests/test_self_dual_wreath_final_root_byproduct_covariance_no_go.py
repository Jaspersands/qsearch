from __future__ import annotations

import math

import numpy as np
import pytest

from self_dual_wreath_final_root_byproduct_covariance_no_go import (
    _rotated_effect,
    audit_byproduct_covariance,
    audit_labelled_weyl_rigidity,
    canonical_endpoint,
    effect_commutant_dimension,
    endpoint_byproduct_blocks,
    natural_byproduct_covariance_record,
    run_final_root_byproduct_covariance_no_go,
    write_final_root_byproduct_covariance_no_go_report,
)
from self_dual_wreath_final_root_purification_naimark_program_boundary import (
    weyl_unitary_error_basis,
)


def test_canonical_endpoint_and_explicit_byproduct_blocks() -> None:
    effect = _rotated_effect([0.2, 0.5, 0.8])
    endpoint = canonical_endpoint(effect)
    error = weyl_unitary_error_basis(3)[3]
    direct = endpoint @ error @ endpoint.conj().T
    explicit = endpoint_byproduct_blocks(effect, error)

    assert np.linalg.norm(endpoint.conj().T @ endpoint - np.eye(3), ord=2) < 1e-10
    assert np.linalg.norm(direct - explicit, ord=2) < 1e-10


@pytest.mark.parametrize(
    "effect,distinct,commutant",
    [
        (0.4 * np.eye(3), 1, 9),
        (np.diag([0.2, 0.5, 0.8]), 3, 3),
        (np.diag([0.2, 0.2, 0.8, 0.8]), 2, 8),
    ],
)
def test_effect_commutant_dimension(effect, distinct: int, commutant: int) -> None:
    observed_distinct, observed_commutant = effect_commutant_dimension(effect)
    assert observed_distinct == distinct
    assert observed_commutant == commutant


@pytest.mark.parametrize(
    "control_id,effect,full_possible",
    [
        ("scalar", 0.4 * np.eye(3), True),
        ("diagonal", np.diag([0.2, 0.5, 0.8]), False),
        ("rotated", _rotated_effect([0.2, 0.5, 0.8]), False),
        ("degenerate", _rotated_effect([0.2, 0.2, 0.8, 0.8]), False),
    ],
)
def test_unitary_basis_covariance_boundary(
    control_id: str,
    effect: np.ndarray,
    full_possible: bool,
) -> None:
    row = audit_byproduct_covariance(control_id, effect)

    assert row.exact_byproduct_and_covariance_boundary_verified
    assert row.full_branch_preserving_error_basis_possible is full_possible
    assert row.average_normalized_commutator_square == pytest.approx(
        2 * row.effect_variance,
        abs=1e-10,
    )
    assert row.maximum_byproduct_block_formula_residual < 1e-10
    assert row.maximum_correction_identity_residual < 1e-10
    assert row.child_transport_conjugation_residual < 1e-10


def test_diagonal_nonflat_effect_has_only_phase_weyls_in_commutant() -> None:
    row = audit_byproduct_covariance(
        "diagonal",
        np.diag([0.2, 0.5, 0.8]),
    )

    assert row.selected_weyl_basis_exact_commuting_error_count == 3
    assert row.effect_commutant_complex_dimension == 3
    assert row.universal_average_branch_preserving_residual_square_lower_bound > 0


def test_labelled_shift_and_clock_pair_is_rigid_but_one_generator_is_not() -> None:
    row = audit_labelled_weyl_rigidity(4)

    assert row.one_generator_does_not_fix_endpoint
    assert row.labelled_weyl_pair_fixes_endpoint_up_to_phase
    assert row.joint_weyl_commutant_complex_dimension == 1
    assert row.common_endpoint_range_residual < 1e-10
    assert row.shift_conjugate_single_generator_residual < 1e-10
    assert row.clock_conjugate_second_generator_gap > 1e-3
    assert row.nontrivial_gauge_distance_from_global_phase > 1e-3
    with pytest.raises(ValueError):
        audit_labelled_weyl_rigidity(2)


@pytest.mark.parametrize("alpha", [2.0, 2.5, 3.0, 3.5, 4.0])
def test_natural_free_jacobi_variance_gives_constant_covariance_error(alpha: float) -> None:
    row = natural_byproduct_covariance_record(alpha)

    assert row.limiting_effect_variance == pytest.approx(1 / (8 * alpha))
    assert row.annealed_average_branch_preserving_residual_square_lower_bound == pytest.approx(
        1 / (16 * alpha)
    )
    assert row.quantitative_event_probability_lower_bound == pytest.approx(
        1 / (4 * alpha - 1)
    )
    assert row.quantitative_event_average_residual_square_lower_bound == pytest.approx(
        1 / (32 * alpha)
    )
    assert row.annealed_average_branch_preserving_residual_square_lower_bound >= 1 / 64
    assert row.quantitative_event_probability_lower_bound >= 1 / 15
    assert row.quantitative_event_average_residual_square_lower_bound >= 1 / 128
    assert not row.full_branch_preserving_unitary_error_basis_asymptotically_possible


def test_invalid_effects_and_aspects_are_rejected() -> None:
    with pytest.raises(ValueError):
        canonical_endpoint(np.diag([-0.1, 0.5]))
    with pytest.raises(ValueError):
        canonical_endpoint(np.diag([0.5, 1.1]))
    with pytest.raises(ValueError):
        endpoint_byproduct_blocks(np.eye(2), np.eye(3))
    with pytest.raises(ValueError):
        natural_byproduct_covariance_record(1.9)


def test_report_rejects_only_branch_preserving_covariance_shortcut() -> None:
    report = run_final_root_byproduct_covariance_no_go()

    assert report.theorem.theorem_verified
    assert report.headline_metrics["exact_control_failure_count"] == 0
    assert report.claim_gate["exact_endpoint_conjugated_weyl_block_formula_proved"]
    assert report.claim_gate[
        "branch_preserving_correction_exists_iff_error_commutes_with_effect"
    ]
    assert report.claim_gate[
        "full_branch_preserving_unitary_error_basis_requires_scalar_effect"
    ]
    assert not report.claim_gate["unitary_error_basis_choice_evades_covariance_obstruction"]
    assert not report.claim_gate[
        "existing_branch_preserving_row_copy_covariance_supplies_bell_corrections"
    ]
    assert not report.claim_gate["C_dependent_branch_mixing_weyl_generators_compiled"]
    assert not report.claim_gate["arbitrary_branch_mixing_correction_circuit_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics["uniform_annealed_residual_square_floor"] == pytest.approx(
        1 / 64
    )


def test_writer_emits_artifact_without_registry_mutation(tmp_path) -> None:
    path = tmp_path / "byproduct-covariance.json"
    payload = write_final_root_byproduct_covariance_no_go_report(
        path,
        write_registry=False,
    )

    assert path.exists()
    assert payload["theorem"]["theorem_verified"]
    assert payload["headline_metrics"]["C_dependent_branch_mixing_generator_compiler_count"] == 0
