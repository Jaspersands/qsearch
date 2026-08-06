import numpy as np

from self_dual_wreath_common_core_polar_bypass import (
    _common_core_projector_family,
    audit_common_core_tree,
    block_core_polar_bypass_record,
    run_common_core_polar_bypass,
)


def test_noncommuting_common_core_is_half_balanced_at_every_tree_level():
    projectors = _common_core_projector_family(8)
    common = np.zeros((len(projectors[0]), 1))
    common[0, 0] = 1.0
    record = audit_common_core_tree("eight", projectors, common)

    assert record.noncommuting_leaf_pair_count > 0
    assert record.internal_merge_count == 7
    assert record.tree_depth == 3
    assert record.maximum_common_core_half_balance_residual < 1e-9
    assert record.exact_balanced_common_core_tree_verified


def test_existing_exponential_block_witness_is_not_a_polar_tree_obstruction():
    record = block_core_polar_bypass_record(12)

    assert record.exponential_absolute_spike_present
    assert record.common_orientation_family_size == 512
    assert record.projector_sum_spike_lower_bound == 512
    assert record.balanced_polar_tree_depth == 9
    assert record.relative_effect_on_witness_core == 0.5
    assert not record.factorial_or_exponential_amplification_on_witness_core_required
    assert not record.block_common_core_is_hierarchical_polar_obstruction
    assert not record.quotient_coset_interactions_resolved


def test_report_blocks_old_common_core_no_go_but_not_speedup_claim():
    report = run_common_core_polar_bypass()

    assert report.headline_metrics["finite_validation_failure_count"] == 0
    assert report.headline_metrics["block_core_witness_bypassed_count"] == 6
    assert report.claim_gate[
        "block_common_core_balanced_by_aligned_relative_tree"
    ]
    assert not report.claim_gate[
        "recurring_block_incidence_is_hierarchical_polar_no_go"
    ]
    assert not report.claim_gate["quotient_coset_interactions_classified"]
    assert not report.claim_gate["speedup_claim_allowed"]
