from fractions import Fraction

from self_dual_wreath_pair_core_rank_concentration import (
    audit_pair_core_rank_identity,
    expected_normalized_pair_core_rank,
    pair_core_density_scaling_record,
    run_pair_core_rank_concentration,
)


LABELS = (
    ((6,), (2, 2, 2)),
    ((5, 1), (2, 2, 1, 1)),
    ((4, 2), (2, 1, 1, 1, 1)),
    ((3, 3), (1, 1, 1, 1, 1, 1)),
)


def test_pair_core_rank_factorization_matches_every_w6_pair() -> None:
    record = audit_pair_core_rank_identity(
        "W6-PAIR-RANK", (6,), LABELS
    )

    assert record.orientation_pair_count == 120
    assert record.exact_pair_core_rank_factorization_verified
    assert record.live_pair_core_count == 10
    assert record.finite_live_graph_is_sparse


def test_expected_normalized_pair_rank_is_exact_rational() -> None:
    value = expected_normalized_pair_core_rank(6, (6,))

    assert isinstance(value, Fraction)
    assert value == Fraction(2, 720**3)


def test_balanced_pair_fraction_tends_to_one_and_conditioned_bound_turns_on() -> None:
    early = pair_core_density_scaling_record(32)
    late = pair_core_density_scaling_record(48)

    assert not early.uniform_balanced_pair_rank_concentration_certified
    assert late.uniform_balanced_pair_rank_concentration_certified
    assert late.balanced_ordered_pair_fraction > 0.999
    assert late.log2_conditioned_balanced_pair_failure_upper_bound < -100


def test_report_proves_live_density_not_residual_channel_density() -> None:
    report = run_pair_core_rank_concentration()

    assert report.claim_gate["exact_pair_core_rank_factorization_proved"]
    assert report.claim_gate["natural_live_pair_core_graph_density_one_proved"]
    assert not report.claim_gate[
        "finite_w6_sparse_graph_asymptotically_representative"
    ]
    assert not report.claim_gate["natural_residual_channels_dense_proved"]
    assert not report.claim_gate["natural_shorted_endpoint_comparability_proved"]
    assert not report.claim_gate["speedup_claim_allowed"]
