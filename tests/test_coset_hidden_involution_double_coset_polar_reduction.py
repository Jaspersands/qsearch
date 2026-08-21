import math

import pytest

from coset_hidden_involution_double_coset_polar_reduction import (
    audit_diagonal_multiplicity,
    audit_double_coset_incidence,
    build_double_coset_polar_report,
    double_coset_scaling_record,
    standard_diagonal_invariant_multiplicity,
)


@pytest.mark.parametrize("copy_count", (1, 2))
def test_double_coset_spaces_and_incidence_are_exact(copy_count: int) -> None:
    row = audit_double_coset_incidence(3, 1, copy_count)
    assert row.physical_coset_count == 6**copy_count
    assert row.source_coset_count == 3 * 3**copy_count
    assert row.diagonal_subgroup_order == 6
    assert row.source_stabilizer_order == 2 ** (copy_count + 1)
    assert row.subgroup_intersection_order == 2
    assert row.physical_incidence_degree == 3
    assert row.source_incidence_degree == 2**copy_count
    assert row.nonzero_coset_overlap == pytest.approx(
        1 / math.sqrt(3 * 2**copy_count)
    )
    assert row.discriminant_top_singular_value == pytest.approx(1.0)
    assert row.exact_homogeneous_space_bijections_verified
    assert row.exact_double_coset_incidence_verified


def test_diagonal_fourier_blocks_are_not_multiplicity_free() -> None:
    assert standard_diagonal_invariant_multiplicity(3, 4) == 3
    assert standard_diagonal_invariant_multiplicity(4, 4) == 4
    for n in (3, 4):
        row = audit_diagonal_multiplicity(n, 4)
        assert row.exact_character_average_verified
        assert not row.scalar_gelfand_multiplicity_free


def test_natural_scaling_preserves_generic_phase_barrier() -> None:
    earlier = double_coset_scaling_record(8)
    later = double_coset_scaling_record(16)
    assert later.generic_reflection_phase_query_log2_lower_order > earlier.generic_reflection_phase_query_log2_lower_order
    assert later.log2_identity_term_invariant_multiplicity_lower_bound > earlier.log2_identity_term_invariant_multiplicity_lower_bound
    assert later.retained_alternative_mass == pytest.approx(29 / 32)
    assert later.efficient_subgroup_reflections_available
    assert not later.scalar_spherical_transform_sufficient
    assert not later.matrix_cosine_sine_transform_compiled


def test_report_localizes_matrix_transform_without_claiming_algorithm() -> None:
    report = build_double_coset_polar_report()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.headline_metrics["matrix_multiplicity_failure_count"] == 0
    assert report.claim_gate["double_coset_incidence_normal_form_proved"] is True
    assert report.claim_gate["row_polar_is_subgroup_cosine_sine_alignment"] is True
    assert report.claim_gate["generic_alternating_reflection_polar_polynomial"] is False
    assert report.claim_gate["scalar_spherical_transform_sufficient"] is False
    assert report.claim_gate["matrix_cosine_sine_transform_compiled"] is False
    assert report.claim_gate["binary_hidden_involution_detector_constructed"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
