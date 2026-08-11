import numpy as np

from coset_arbitrary_covariant_measurement_reduction import (
    _mixed_purification_control,
    _pure_control,
    arbitrary_covariant_measurement_theorem,
    run_arbitrary_covariant_measurement_reduction,
)


def test_pure_noncovariant_measurement_becomes_exact_intertwiner() -> None:
    control = _pure_control(seed=109, multiplicity=2)
    assert control.initially_noncovariant_measurement
    assert not control.mixed_state_purification_control
    assert control.symmetrized_success_spread <= 1e-10
    assert control.effect_covariance_residual <= 1e-10
    assert control.intertwiner_residual <= 1e-10
    assert control.homogeneous_fourier_block_residual is not None
    assert control.homogeneous_fourier_block_residual <= 1e-10
    assert control.exact_homogeneous_measurement_reduction_verified


def test_inverse_fourier_row_average_dominates_decoder_success() -> None:
    control = _pure_control(seed=211, multiplicity=3)
    assert (
        control.average_inverse_row_preparation_probability + 1e-10
        >= control.source_average_success
    )
    assert np.isclose(
        control.average_inverse_row_preparation_probability,
        control.cleaned_reference_norm_squared,
        atol=1e-10,
    )
    assert control.success_to_average_row_preparation_residual <= 1e-10


def test_mixed_covariant_purification_has_same_reduction() -> None:
    control = _mixed_purification_control(seed=307)
    assert control.mixed_state_purification_control
    assert control.matching_garbage_normalization_residual <= 1e-10
    assert control.intertwiner_residual <= 1e-10
    assert control.average_inverse_row_preparation_probability >= (
        control.source_average_success - 1e-10
    )
    assert control.exact_homogeneous_measurement_reduction_verified


def test_theorem_does_not_assume_pgm_or_promote_row_states() -> None:
    theorem = arbitrary_covariant_measurement_theorem()
    assert theorem.arbitrary_measurement_to_intertwiner_reduced
    assert theorem.mixed_covariant_orbits
    assert not theorem.pgm_structure_used
    assert not theorem.multiplicity_row_verifier_constructed
    assert not theorem.polynomial_decoder_constructed


def test_report_keeps_nonabelian_algorithm_gates_closed() -> None:
    report = run_arbitrary_covariant_measurement_reduction()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate[
        "arbitrary_measurement_reduces_to_multiplicity_row_preparation"
    ]
    assert not report.claim_gate[
        "multiplicity_row_state_is_classically_verifiable_witness"
    ]
    assert not report.claim_gate["polynomial_hidden_involution_decoder_constructed"]
    assert not report.claim_gate["speedup_claim_allowed"]
