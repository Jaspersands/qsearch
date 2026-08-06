from representation_obstruction import integer_partitions
from self_dual_wreath_local_isotypic_filter_no_go import (
    local_filter_no_go_scaling_record,
    retained_irrep_incidence_certificate,
    run_local_isotypic_filter_no_go,
)


def test_double_counting_for_adversarially_varying_retained_sets() -> None:
    n = 8
    partitions = integer_partitions(n)
    rows = tuple(
        frozenset(
            partition
            for index, partition in enumerate(partitions)
            if index % 5 != block % 5
        )
        for block in range(20)
    )
    record = retained_irrep_incidence_certificate(n, rows)
    assert record.exact_double_counting_bound_verified
    assert (
        record.maximum_retaining_block_incidence
        >= record.incidence_lower_bound
    )
    assert record.paired_common_bit_count_lower_bound > 0


def test_constant_retained_mass_gives_linear_paired_bit_rate() -> None:
    record = local_filter_no_go_scaling_record(512, retained_mass=0.5)
    assert record.paired_common_bit_count_lower_bound > 100
    assert record.paired_bit_rate_lower_bound > 0.02
    assert not record.uniform_polynomial_factor_residual_norm_possible


def test_report_closes_local_filters_only() -> None:
    report = run_local_isotypic_filter_no_go()
    assert report.headline_metrics[
        "finite_incidence_validation_failure_count"
    ] == 0
    assert report.claim_gate["retained_irrep_double_counting_proved"]
    assert report.claim_gate[
        "constant_mass_block_local_isotypic_filter_bypassed"
    ]
    assert not report.claim_gate[
        "block_local_filter_can_restore_uniform_polynomial_frame_norm"
    ]
    assert not report.claim_gate["growing_block_nonlocal_filter_ruled_out"]
    assert not report.claim_gate[
        "non_isotypic_coherent_transform_ruled_out"
    ]
    assert not report.claim_gate["global_spectral_trim_measurement_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
