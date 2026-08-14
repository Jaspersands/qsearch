import math
from fractions import Fraction

import pytest

from coset_hidden_involution_orbit_synthesis_flatness import (
    alternative_bad_relative_spectrum_mass_upper_bound,
    audit_orbit_synthesis_control,
    build_orbit_synthesis_flatness_report,
    exact_synthesis_centered_second_moment,
    flatness_copy_count,
    orbit_synthesis_scaling_record,
    write_orbit_synthesis_flatness_report,
)


def test_exact_synthesis_moment_and_tail_formulas():
    assert exact_synthesis_centered_second_moment(15, 10) == Fraction(14, 1024)
    bad = alternative_bad_relative_spectrum_mass_upper_bound(15, 10, 0.5)
    assert bad == pytest.approx(6 * 14 / 1024)
    assert flatness_copy_count(15) == math.ceil(math.log2(64 * 15))

    with pytest.raises(ValueError, match="positive"):
        exact_synthesis_centered_second_moment(0, 3)
    with pytest.raises(ValueError, match="delta"):
        alternative_bad_relative_spectrum_mass_upper_bound(3, 3, 1.0)
    with pytest.raises(ValueError, match="positive"):
        flatness_copy_count(3, inverse_variance=0)


@pytest.mark.parametrize(
    ("n", "transpositions", "copies"),
    ((3, 1, 1), (3, 1, 2), (3, 1, 3), (4, 2, 2)),
)
def test_dense_orbit_frames_verify_exact_domain_moments(
    n, transpositions, copies
):
    row = audit_orbit_synthesis_control(n, transpositions, copies)
    assert row.finite_control_verified
    assert row.mean_identity_residual < 1e-10
    assert row.second_moment_identity_residual < 1e-10
    assert row.empirical_domain_mean_squared_singular_value == pytest.approx(1.0)
    assert row.relative_window_bound_respected
    assert row.synthesis_support_rank <= row.synthesis_domain_dimension


def test_six_extra_copies_give_constant_relative_window_mass():
    rows = [orbit_synthesis_scaling_record(n) for n in (6, 8, 16, 32, 64, 128)]
    assert all(row.copy_overhead_beyond_log2_class_size == 6 for row in rows)
    assert all(
        row.exact_domain_centered_second_moment <= 1 / 64 for row in rows
    )
    assert all(
        row.certified_alternative_relative_window_mass >= 29 / 32
        for row in rows
    )
    assert all(row.rescaled_frame_eigenvalue_lower_bound == 0.5 for row in rows)
    assert all(row.rescaled_frame_eigenvalue_upper_bound == 1.5 for row in rows)
    assert all(
        row.unnormalized_synthesis_singular_value_lower_bound
        == pytest.approx(1 / math.sqrt(2))
        for row in rows
    )
    assert all(row.relative_conditioning_constant_on_retained_mass for row in rows)
    assert all(
        not row.constant_normalization_unnormalized_synthesis_access_constructed
        for row in rows
    )
    assert all(not row.polar_label_erasure_compiled for row in rows)


def test_report_preserves_access_and_label_erasure_barriers(tmp_path):
    report = build_orbit_synthesis_flatness_report(
        finite_specs=((3, 1, 2), (4, 2, 2)),
        scaling_n_values=(6, 8, 16, 32),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_pair_overlap_proved
    assert report.theorem.exact_synthesis_moments_proved
    assert report.theorem.alternative_pushforward_proved
    assert report.theorem.constant_mass_relative_flatness_proved
    assert not report.theorem.constant_normalization_synthesis_access_constructed
    assert not report.theorem.polar_label_erasure_compiled
    assert not report.theorem.polynomial_binary_algorithm_constructed
    assert report.claim_gate["orbit_synthesis_relative_flatness_proved"]
    assert not report.claim_gate["standard_orbit_lcu_has_constant_normalization"]
    assert not report.claim_gate["polar_label_erasure_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_orbit_synthesis_flatness_report(
        tmp_path / "orbit-flatness.json",
        finite_specs=((3, 1, 2),),
        scaling_n_values=(6, 8),
    )
    assert payload["status"] == (
        "orbit-synthesis-relative-flatness-proved-label-erasure-open"
    )
    assert payload["headline_metrics"][
        "constant_mass_relative_flatness_theorem_count"
    ] == 1
