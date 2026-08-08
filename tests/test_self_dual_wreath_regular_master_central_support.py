import math

import numpy as np

from self_dual_wreath_regular_master_central_support import (
    audit_central_support_dilution,
    audit_collision_free_central_support_dilution,
    audit_regular_master_decomposition,
    left_regular_rows,
    regular_master_orientation_projector,
    run_regular_master_central_support,
)


def test_left_regular_rows_form_a_representation() -> None:
    rows = dict(left_regular_rows(3))
    group = tuple(rows)
    for left in group:
        for right in group:
            product = tuple(left[right[index]] for index in range(3))
            assert np.allclose(rows[left] @ rows[right], rows[product])


def test_regular_master_orientation_operators_are_projectors() -> None:
    for mask in (0, 1):
        projector = regular_master_orientation_projector((2, 1), 1, mask)
        assert np.linalg.norm(projector @ projector - projector, ord=2) < 1e-12


def test_master_spectrum_is_exact_union_of_plancherel_blocks() -> None:
    record = audit_regular_master_decomposition(3, (2, 1))
    assert record.regular_master_dimension == 72
    assert record.fourier_block_dimension_sum == 72
    assert record.maximum_spectral_decomposition_residual < 2e-12
    assert record.maximum_normalized_moment_residual < 2e-12
    assert record.exact_regular_master_decomposition_verified


def test_central_support_is_block_event_not_scalar_spectral_mass() -> None:
    record = audit_central_support_dilution()
    assert math.isclose(record.bad_block_plancherel_probability, 4 / 9)
    assert math.isclose(record.scalar_bad_spectral_mass_from_blocks, 1 / 9)
    assert math.isclose(record.scalar_bad_spectral_mass_from_master, 1 / 9)
    assert math.isclose(record.central_support_to_scalar_spectral_mass_ratio, 4.0)
    assert record.central_support_event_identity_verified
    assert record.scalar_spectral_mass_is_strictly_smaller


def test_central_support_dilution_survives_global_distinctness() -> None:
    record = audit_collision_free_central_support_dilution()
    assert record.globally_distinct_plancherel_probability == "89/1536"
    assert record.bad_block_conditional_probability == "54/89"
    assert record.scalar_bad_spectral_mass_conditional == "10/267"
    assert record.central_support_to_scalar_spectral_mass_ratio == "81/5"
    assert record.minimum_bad_projection_relative_rank == "1/18"
    assert record.maximum_bad_projection_relative_rank == "1/9"
    assert record.every_source_tuple_globally_distinct
    assert record.scalar_spectral_mass_is_strictly_smaller


def test_report_opens_center_valued_local_law_gate() -> None:
    report = run_regular_master_central_support()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics[
        "collision_free_central_support_to_scalar_mass_ratio"
    ] == 16.2
    assert report.claim_gate["regular_master_fourier_block_lift_proved"]
    assert report.claim_gate["bad_block_probability_is_central_support_trace"]
    assert not report.claim_gate["center_valued_local_law_proved"]
    assert not report.claim_gate["tight_coherent_master_node_frame_encoding_proved"]
    assert not report.claim_gate["natural_all_depth_frame_edge_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
