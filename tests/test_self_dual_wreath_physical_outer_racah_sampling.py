from self_dual_wreath_physical_outer_racah_sampling import (
    audit_physical_outer_sampler_normalization,
    conditional_final_distribution,
    sample_physical_outer_racah_couplings,
)


def test_sequential_outer_sampler_normalizes_for_every_s5_source_triple() -> None:
    row = audit_physical_outer_sampler_normalization(5)
    assert row.source_triple_count == 343
    assert row.maximum_dimension_identity_residual == 0
    assert row.maximum_conditional_probability_sum_residual < 1e-14
    assert row.exact_sequential_sampler_verified


def test_final_distribution_uses_dimension_weighted_triple_multiplicity() -> None:
    source = (3, 1, 1)
    finals, probabilities, multiplicities = conditional_final_distribution(
        source,
        source,
        source,
    )
    assert abs(sum(probabilities) - 1.0) < 1e-14
    assert all(
        (probability > 0) == (multiplicity > 0)
        for probability, multiplicity in zip(probabilities, multiplicities)
    )
    assert len(finals) == 7


def test_s5_sampling_recovers_exact_average_inside_rigorous_interval() -> None:
    row = sample_physical_outer_racah_couplings(
        5,
        8,
        random_seed=113,
    )
    assert row.all_sampled_couplings_verified
    assert row.exact_average_inside_mi_confidence_interval is True
    assert row.exact_finite_physical_average_mi_bits is not None
    assert row.asymptotic_inference_allowed is False


def test_s6_sampling_is_physical_average_probe_not_speedup_evidence() -> None:
    row = sample_physical_outer_racah_couplings(
        6,
        3,
        random_seed=127,
    )
    assert row.sample_count == 3
    assert row.all_sampled_couplings_verified
    assert row.exact_finite_physical_average_mi_bits is None
    assert row.mutual_information_hoeffding_radius_bits > 0
    assert row.maximum_natural_to_orthogonal_haar_chi_ratio >= 0
    assert all(
        sample.natural_to_orthogonal_haar_chi_ratio >= 0
        for sample in row.samples
    )
    assert row.maximum_fractional_excess_to_theta_haar_upper_ratio >= 0
    assert row.asymptotic_inference_allowed is False
