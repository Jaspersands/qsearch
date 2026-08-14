import math

import pytest

from coset_hidden_involution_branch_erasure_normalization_no_go import (
    audit_branch_erasure_normalization,
    branch_erasure_scaling_record,
    branch_row_normalization_lower_bound,
    build_branch_erasure_normalization_report,
    retained_character_acceptance_bound,
    write_branch_erasure_normalization_report,
)


@pytest.mark.parametrize("spec", ((3, 1, 2), (3, 1, 3), (4, 2, 2)))
def test_labelled_dilation_and_uniform_erasure_are_exact(spec):
    row = audit_branch_erasure_normalization(*spec)
    assert row.exact_branch_erasure_boundary_verified
    assert row.maximum_labelled_isometry_residual < 1e-8
    assert row.uniform_erasure_synthesis_residual < 1e-8
    assert row.exact_success_spectrum_residual < 1e-8
    assert row.uniform_erasure_amplitude == pytest.approx(
        1 / math.sqrt(row.candidate_count)
    )
    assert row.uniform_erasure_success_scale == pytest.approx(
        1 / row.candidate_count
    )


def test_arbitrary_branch_row_coefficient_norm_forces_sqrt_M():
    for candidates in (2, 3, 15, 945, 2_027_025):
        alpha = branch_row_normalization_lower_bound(candidates)
        assert candidates * (1 / alpha) ** 2 == pytest.approx(1.0)
        assert alpha == pytest.approx(math.sqrt(candidates))
    with pytest.raises(ValueError, match="at least two"):
        branch_row_normalization_lower_bound(1)


def test_retaining_few_characters_does_not_erase_candidate_width():
    assert retained_character_acceptance_bound(1024, 1) == pytest.approx(1 / 1024)
    assert retained_character_acceptance_bound(1024, 16) == pytest.approx(1 / 64)
    assert retained_character_acceptance_bound(1024, 512) == pytest.approx(0.5)
    with pytest.raises(ValueError, match="outside"):
        retained_character_acceptance_bound(16, 17)


def test_bulk_success_remains_inverse_candidate_count():
    rows = [branch_erasure_scaling_record(m) for m in (3, 4, 8, 16, 32, 64)]
    assert all(row.retained_alternative_mass_lower_bound > 0.999 for row in rows)
    assert all(not row.branch_only_erasure_polynomial for row in rows)
    assert all(not row.joint_physical_multiplicity_escape_ruled_out for row in rows)
    for row in rows:
        candidates = int(row.candidate_count_decimal)
        assert row.bulk_success_probability_lower_log2 == pytest.approx(
            math.log2(0.5 / candidates)
        )
        assert row.bulk_success_probability_upper_log2 == pytest.approx(
            math.log2(1.5 / candidates)
        )
    assert rows[-1].amplitude_amplification_query_log2_lower_order > 100


def test_report_closes_branch_only_route_without_overclaim(tmp_path):
    report = build_branch_erasure_normalization_report(
        finite_specs=((3, 1, 2), (3, 1, 3)),
        scaling_half_degrees=(3, 4, 8, 16),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.arbitrary_branch_row_sqrt_M_boundary_proved
    assert report.theorem.bulk_inverse_M_success_proved
    assert report.theorem.branch_only_amplification_superpolynomial
    assert not report.theorem.joint_source_physical_transform_ruled_out
    assert not report.theorem.direct_orbit_row_polar_compiled
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_branch_erasure_normalization_report(
        tmp_path / "branch-erasure.json",
        finite_specs=((3, 1, 2),),
        scaling_half_degrees=(3, 4, 8),
    )
    assert payload["status"] == (
        "branch-only-normalization-closed-joint-row-transform-open"
    )
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
