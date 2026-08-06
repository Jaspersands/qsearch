import math

from representation_obstruction import hook_length_dimension
from self_dual_wreath_subgroup_twirl_reduction import (
    audit_twirl_tuple,
    multiplicity_scaling_record,
    restriction_multiplicity_profile,
    run_subgroup_twirl_reduction,
)


W4_LABELS = (
    ((4,), (3, 1)),
    ((2, 2), (2, 1, 1)),
)


def test_restriction_multiplicities_recover_full_dimension() -> None:
    profile = restriction_multiplicity_profile(4, W4_LABELS)
    expected_dimension = math.prod(
        2
        * hook_length_dimension(left)
        * hook_length_dimension(right)
        for left, right in W4_LABELS
    )
    recovered_dimension = sum(
        hook_length_dimension(target) * multiplicity
        for target, multiplicity in profile.items()
    )
    assert recovered_dimension == expected_dimension
    assert all(multiplicity > 0 for multiplicity in profile.values())


def test_subgroup_twirl_and_isotypic_localization_are_exact() -> None:
    record = audit_twirl_tuple(4, W4_LABELS)
    assert record.exact_finite_twirl_validation
    assert record.maximum_bridge_conjugacy_residual < 1e-10
    assert record.direct_frame_twirl_residual < 1e-10
    assert record.maximum_frame_subgroup_commutator_residual < 1e-10
    assert record.restriction_multiplicity_mismatch_count == 0
    assert record.top_eigenvalue_localization_residual < 1e-10
    assert record.direct_frame_top_eigenvalue <= (
        record.target_two_to_one_minus_k + 1e-10
    )


def test_threshold_scaling_exposes_large_multiplicity_space() -> None:
    record = multiplicity_scaling_record(11)
    assert record.reaches_information_threshold
    assert record.restriction_dimension_identity_verified
    assert record.maximum_restriction_multiplicity_log2 > 400
    assert not record.uniform_partial_trace_delocalization_proved


def test_report_proves_reduction_but_blocks_norm_claim() -> None:
    report = run_subgroup_twirl_reduction()
    assert (
        report.headline_metrics[
            "complete_w4_collision_free_twirl_validation_count"
        ]
        == 15
    )
    assert report.headline_metrics["finite_twirl_validation_failure_count"] == 0
    assert report.claim_gate["subgroup_twirl_identity_proved"]
    assert report.claim_gate["isotypic_partial_trace_reduction_proved"]
    assert report.claim_gate["dense_mask_two_cores_resummed_exactly"]
    assert not report.claim_gate[
        "uniform_partial_trace_delocalization_proved"
    ]
    assert not report.claim_gate["speedup_claim_allowed"]
