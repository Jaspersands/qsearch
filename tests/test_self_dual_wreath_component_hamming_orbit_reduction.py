import math

import pytest

from self_dual_wreath_component_hamming_orbit_reduction import (
    audit_physical_hamming_orbit,
    audit_source_relabeling_equivariance,
    component_M4_from_hamming_profile,
    run_component_hamming_orbit_reduction,
    typical_hamming_pair_scaling_record,
)


def test_binomial_rescaled_profile_identity_is_exact() -> None:
    profile = {1: 1 / 256, 2: 3 / 512, 3: 1 / 1024}
    direct, binomial = component_M4_from_hamming_profile(3, profile)

    assert direct == pytest.approx(binomial)
    assert direct == pytest.approx(
        4
        * (
            math.comb(3, 1) * profile[1]
            + math.comb(3, 2) * profile[2]
            + math.comb(3, 3) * profile[3]
        )
    )


def test_repeated_source_physical_control_has_exact_hamming_profile() -> None:
    standard = (2, 1)
    row = audit_physical_hamming_orbit(
        "REPEATED",
        standard,
        ((standard, standard),) * 3,
    )

    assert row.child_cube_dimension == 2
    assert row.child_leaf_count == 4
    assert row.common_fiber_dimension == 52
    assert row.maximum_within_hamming_orbit_residual < 1e-12
    assert row.direct_normalized_component_M4 > 0
    assert row.direct_normalized_component_M4 == pytest.approx(
        row.hamming_profile_component_M4
    )
    assert row.direct_normalized_component_M4 == pytest.approx(
        row.binomial_rescaled_profile_component_M4
    )
    assert row.exact_hamming_orbit_counting_verified is True


def test_nonidentical_source_blocks_transform_equivariantly_across_orbit() -> None:
    trivial = (3,)
    standard = (2, 1)
    sign = (1, 1, 1)
    row = audit_source_relabeling_equivariance(
        "NONIDENTICAL",
        standard,
        (
            (trivial, standard),
            (trivial, standard),
            (standard, sign),
        ),
        (0, 1),
    )

    assert row.source_pair_flip_count == 4
    assert row.source_pair_permutation_count == 2
    assert row.maximum_flip_equivariance_residual < 1e-12
    assert row.maximum_permutation_equivariance_residual < 1e-12
    assert row.exact_scalar_component_pair_equivariance_verified is True


def test_typical_hamming_q_inverse_two_profile_gives_inverse_polynomial_M4() -> None:
    row = typical_hamming_pair_scaling_record(
        64,
        target_rescaled_gap_polynomial_degree=2,
    )

    assert row.typical_window_binomial_mass > 0.99
    assert row.target_rescaled_pair_gap_lower_bound == pytest.approx(1 / 64**2)
    assert row.resulting_M4_lower_bound == pytest.approx(
        row.typical_window_binomial_mass / (2 * 64**2)
    )
    assert row.equivalent_pair_gap_log2_lower_bound == pytest.approx(
        -2 * row.child_cube_dimension - 2 * math.log2(64)
    )
    assert row.typical_hamming_profile_suffices_for_M4 is True
    assert row.natural_typical_ridge_pair_gap_proved is False


def test_report_reduces_to_typical_pair_without_promoting_positivity() -> None:
    report = run_component_hamming_orbit_reduction()

    assert report.status == (
        "component-M4-reduced-to-typical-hamming-ridge-pair-gap"
    )
    assert report.headline_metrics[
        "annealed_component_hamming_orbit_reduction_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "binomial_rescaled_pair_M4_identity_theorem_count"
    ] == 1
    assert report.headline_metrics[
        "global_distinct_hamming_profile_transfer_theorem_count"
    ] == 1
    assert report.headline_metrics["physical_control_failure_count"] == 0
    assert report.headline_metrics["relabeling_control_failure_count"] == 0
    assert report.claim_gate[
        "annealed_pair_gap_depends_only_on_hamming_distance"
    ] is True
    assert report.claim_gate[
        "exponential_pair_sum_reduced_to_binomial_profile"
    ] is True
    assert report.claim_gate["natural_typical_hamming_ridge_pair_gap_positive"] is False
    assert report.claim_gate["natural_independent_plancherel_M4_positive"] is False
    assert report.claim_gate["speedup_claim_allowed"] is False
