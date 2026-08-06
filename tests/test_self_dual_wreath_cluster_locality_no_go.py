from fractions import Fraction
import math

from self_dual_wreath_cluster_locality_no_go import (
    cluster_locality_scaling_record,
    conservative_copy_lower_bound,
    maximum_certified_locality,
    run_cluster_locality_no_go,
)


def test_copy_lower_bound_is_rigorous_on_finite_degrees() -> None:
    for n in range(4, 200):
        exact = (math.factorial(n) - 1).bit_length()
        assert 0 < conservative_copy_lower_bound(n) <= exact


def test_sqrt_locality_falsifies_fixed_degree_polynomial_bound() -> None:
    n = 1 << 20
    record = cluster_locality_scaling_record(
        n,
        cluster_base_block_locality=math.isqrt(n),
        retained_mass=Fraction(1, 2),
        polynomial_degree=10,
    )
    assert record.cluster_source_label_locality < n
    assert record.paired_common_bit_count_lower_bound > 250
    assert record.degree_d_polynomial_bound_falsified


def test_linear_locality_is_not_overclaimed() -> None:
    n = 1 << 20
    record = cluster_locality_scaling_record(
        n,
        cluster_base_block_locality=n // (64 * 8),
        retained_mass=Fraction(1, 2),
        polynomial_degree=100,
    )
    assert not record.degree_d_polynomial_bound_falsified


def test_n_over_log_n_locality_eventually_beats_every_fixed_degree() -> None:
    n = 1 << 1024
    locality = n // (8 * n.bit_length())
    record = cluster_locality_scaling_record(
        n,
        cluster_base_block_locality=locality,
        retained_mass=Fraction(1, 2),
        polynomial_degree=100,
        n_description="2^1024:n/log(n)",
    )
    assert record.source_label_locality_fraction < 0.001
    assert record.degree_d_polynomial_bound_falsified


def test_maximum_certified_locality_is_a_sharp_finite_threshold() -> None:
    n = 1 << 20
    threshold = maximum_certified_locality(n, polynomial_degree=10)
    assert threshold.maximum_cluster_base_block_locality_certifiably_bypassed > 0
    at_threshold = cluster_locality_scaling_record(
        n,
        cluster_base_block_locality=(
            threshold.maximum_cluster_base_block_locality_certifiably_bypassed
        ),
        polynomial_degree=10,
    )
    above_threshold = cluster_locality_scaling_record(
        n,
        cluster_base_block_locality=(
            threshold.maximum_cluster_base_block_locality_certifiably_bypassed
            + 1
        ),
        polynomial_degree=10,
    )
    assert at_threshold.degree_d_polynomial_bound_falsified
    assert not above_threshold.degree_d_polynomial_bound_falsified


def test_report_preserves_nonlocal_scope_boundary() -> None:
    report = run_cluster_locality_no_go()
    assert report.claim_gate[
        "sublinear_constant_mass_cluster_filters_bypassed"
    ]
    assert not report.claim_gate["overlapping_cluster_filters_ruled_out"]
    assert not report.claim_gate["global_spectral_filter_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
    assert report.headline_metrics[
        "constant_mass_minimum_viable_source_label_locality"
    ] == "Omega(n)"
