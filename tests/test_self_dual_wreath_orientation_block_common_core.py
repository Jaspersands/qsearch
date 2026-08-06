from self_dual_wreath_orientation_block_common_core import (
    block_common_core_scaling_record,
    run_orientation_block_common_core,
)


def test_n12_block_common_core_is_exact_and_exponential() -> None:
    record = block_common_core_scaling_record(12)
    assert record.copy_count == 29
    assert record.reaches_information_threshold
    assert record.block_count == 9
    assert record.common_orientation_family_size == 512
    assert record.projector_sum_norm_lower_bound == 512
    assert record.norm_lower_bound_to_target_ratio == 256
    assert record.log2_common_core_dimension_lower_bound > 100
    assert record.exact_finite_block_common_core_witness


def test_n12_blocks_form_a_parity_valid_exact_cover() -> None:
    record = block_common_core_scaling_record(12)
    indices = [index for block in record.blocks for index in block.label_indices]
    sign_parity = sum(
        block.one_dimensional_character == "sign" for block in record.blocks
    ) % 2
    assert sorted(indices) == list(range(record.copy_count))
    assert len(indices) == len(set(indices))
    assert sign_parity == 0
    assert all(block.left_multiplicity > 0 for block in record.blocks)
    assert all(block.right_multiplicity > 0 for block in record.blocks)


def test_finite_portfolios_do_not_overclaim_asymptotic_persistence() -> None:
    report = run_orientation_block_common_core()
    assert report.headline_metrics[
        "exact_finite_block_common_core_witness_count"
    ] == 6
    assert report.claim_gate["block_common_core_construction_proved"]
    assert not report.claim_gate["asymptotic_linear_block_rate_proved"]
    assert not report.claim_gate["natural_constant_mass_persistence_proved"]
    assert not report.claim_gate[
        "uniform_polynomial_factor_norm_counterexample_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
