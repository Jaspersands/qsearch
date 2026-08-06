from self_dual_wreath_paired_block_filter_bypass import (
    paired_block_filter_bypass_scaling_record,
    run_paired_block_filter_bypass,
)


def test_n12_filter_bypass_has_exact_retained_common_family() -> None:
    record = paired_block_filter_bypass_scaling_record(12)
    assert record.copy_count == 29
    assert record.original_block_count == 9
    assert record.paired_bit_count == 4
    assert record.common_orientation_family_size == 16
    assert record.norm_lower_bound_to_target_ratio == 8
    assert record.common_core_dimension_lower_bound > 0
    assert record.exact_filtered_paired_block_witness
    assert all(
        block.retained_irrep_dimension > 1
        and block.survives_one_dimensional_branch_filter
        and block.retained_irrep_square_trivial_multiplicity > 0
        for block in record.paired_blocks
    )


def test_all_finite_portfolios_have_paired_filter_bypass() -> None:
    records = [
        paired_block_filter_bypass_scaling_record(n)
        for n in range(7, 13)
    ]
    assert all(record.exact_filtered_paired_block_witness for record in records)
    assert records[-1].norm_lower_bound_to_target_ratio > 1


def test_report_falsifies_local_filter_not_global_spectral_trim() -> None:
    report = run_paired_block_filter_bypass()
    assert report.headline_metrics[
        "exact_filtered_paired_block_witness_count"
    ] == 6
    assert report.claim_gate["paired_block_filter_bypass_proved"]
    assert report.claim_gate[
        "typical_filtered_exponential_common_family_proved"
    ]
    assert not report.claim_gate[
        "one_dimensional_branch_filter_restores_polynomial_frame_norm"
    ]
    assert not report.claim_gate[
        "branch_controlled_filter_is_viable_norm_strategy"
    ]
    assert not report.claim_gate[
        "abstract_spectral_trimmed_measurement_ruled_out"
    ]
    assert not report.claim_gate["nonlocal_block_filter_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]
