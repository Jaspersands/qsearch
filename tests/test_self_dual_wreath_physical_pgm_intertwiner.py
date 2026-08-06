import numpy as np
import pytest

from self_dual_wreath_physical_pgm_intertwiner import (
    audit_physical_pgm_intertwiner,
    generalized_fourier_row_copy_isometry,
    physical_pgm_intertwiner_scaling_record,
    run_physical_pgm_intertwiner,
)
from self_dual_wreath_subgroup_twirl_reduction import (
    tuple_left_subgroup_matrices,
)


def test_generalized_fourier_row_copy_is_an_isometry():
    labels = (((3,), (2, 1)),)
    transformed, permutations, partitions = (
        generalized_fourier_row_copy_isometry(
            3,
            tuple_left_subgroup_matrices(labels),
        )
    )

    assert len(permutations) == 6
    assert set(partitions) == {(3,), (2, 1), (1, 1, 1)}
    assert np.linalg.norm(
        transformed.conj().T @ transformed
        - np.eye(transformed.shape[1]),
        ord=2,
    ) < 1e-10


def test_physical_pgm_analysis_factors_through_orientation_ranges():
    record = audit_physical_pgm_intertwiner(
        3,
        (
            ((3,), (2, 1)),
            ((3,), (1, 1, 1)),
            ((2, 1), (1, 1, 1)),
        ),
        control_id="threshold",
    )

    assert record.exact_physical_pgm_intertwiner_verified
    assert record.copy_count == 3
    assert record.orientation_count == 8
    assert record.active_sector_row_count > 0
    assert record.maximum_invariant_range_leakage < 1e-9
    assert record.maximum_orientation_assembly_residual < 1e-9
    assert record.maximum_fourier_gram_residual < 1e-9
    assert record.maximum_polar_transfer_residual < 1e-8


def test_intertwiner_resolves_transfer_but_not_orientation_polar():
    report = run_physical_pgm_intertwiner()

    assert report.headline_metrics["finite_validation_failure_count"] == 0
    assert report.claim_gate["physical_output_intertwiner_compiled"]
    assert report.claim_gate["coherent_cross_sector_transfer_proved"]
    assert not report.claim_gate["kronecker_multiplicity_basis_required"]
    assert not report.claim_gate[
        "synthesis_adjoint_amplitude_amplification_required"
    ]
    assert report.claim_gate[
        "orientation_polar_is_only_remaining_pgm_implementation_gate"
    ]
    assert not report.claim_gate["hierarchical_orientation_polar_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_scaling_schema_uses_only_standard_transfer_operations():
    record = physical_pgm_intertwiner_scaling_record(128)

    assert record.coherent_symmetric_group_qft_polynomial
    assert record.controlled_restriction_action_polynomial
    assert record.coherent_cross_sector_transfer_proved
    assert record.physical_output_intertwiner_compiled
    assert not record.kronecker_multiplicity_basis_required
    assert not record.synthesis_adjoint_amplitude_amplification_required
    assert not record.hierarchical_orientation_polar_proved
    assert not record.polynomial_physical_pgm_circuit_proved


def test_invalid_physical_labels_are_rejected():
    with pytest.raises(ValueError, match="unequal partition pairs"):
        audit_physical_pgm_intertwiner(
            3,
            (((3,), (3,)),),
            control_id="invalid",
        )
