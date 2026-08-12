from __future__ import annotations

import math

import pytest

from self_dual_wreath_joint_character_purity_decoupling import (
    _exhaustive_natural_average,
    audit_fixed_tuple_purity,
    audit_natural_purity,
    fixed_tuple_joint_purity,
    natural_annealed_joint_purity,
    partition_number,
    purity_decoupling_scaling_record,
    run_joint_character_purity_decoupling,
    universal_normalized_purity_bound,
)


THRESHOLD_LABELS = (
    ((3,), (2, 1)),
    ((3,), (1, 1, 1)),
    ((2, 1), (1, 1, 1)),
)


@pytest.mark.parametrize(
    "n,labels",
    [
        (3, (((3,), (2, 1)),)),
        (3, THRESHOLD_LABELS),
        (4, (((4,), (3, 1)), ((2, 2), (2, 1, 1)))),
    ],
)
def test_fixed_tuple_character_purity_matches_direct_joint_matrix(
    n: int,
    labels: tuple[tuple[tuple[int, ...], tuple[int, ...]], ...],
) -> None:
    control = audit_fixed_tuple_purity(n, labels, control_id="control")
    assert control.exact_fixed_tuple_purity_verified
    assert control.purity_formula_residual < 1e-9
    assert control.normalized_purity >= 1
    assert control.holevo_upper_bound_bits >= 0


def test_plancherel_formula_matches_exhaustive_small_label_average() -> None:
    for copies in (1, 2):
        exhaustive = _exhaustive_natural_average(3, copies)
        formula, _ = natural_annealed_joint_purity(3, copies)
        assert exhaustive == pytest.approx(formula, abs=1e-12)


def test_exact_class_controls_stay_far_below_universal_partition_bound() -> None:
    for n in range(3, 13):
        control = audit_natural_purity(n)
        assert control.exact_class_formula_verified
        assert control.exact_normalized_annealed_purity <= (
            control.universal_normalized_purity_upper_bound + 1e-8
        )
        assert control.exact_normalized_annealed_purity < 5
        assert control.universal_normalized_purity_upper_bound == pytest.approx(
            universal_normalized_purity_bound(n)
        )


def test_partition_counter_matches_known_values() -> None:
    assert [partition_number(n) for n in range(1, 11)] == [
        1,
        2,
        3,
        5,
        7,
        11,
        15,
        22,
        30,
        42,
    ]


def test_fano_scaling_rules_out_one_block_but_not_polynomial_blocks() -> None:
    record = purity_decoupling_scaling_record(128)
    assert record.one_block_extensive_information_ruled_out
    assert record.holevo_fraction_upper_bound < 0.25
    assert record.bounded_error_fano_block_lower_bound > 1
    assert record.bounded_error_fano_coset_copy_lower_bound > (
        record.information_threshold_copy_count
    )
    assert not record.polynomial_number_of_blocks_ruled_out
    assert not record.carrier_retaining_decoder_ruled_out


def test_report_preserves_multiblock_and_carrier_retaining_escapes() -> None:
    report = run_joint_character_purity_decoupling()
    assert report.headline_metrics["finite_control_failure_count"] == 0
    assert report.claim_gate["exact_joint_purity_class_formula_proved"]
    assert report.claim_gate[
        "typical_one_block_extensive_information_ruled_out"
    ]
    assert not report.claim_gate["polynomial_number_of_joint_blocks_ruled_out"]
    assert not report.claim_gate[
        "adaptive_joint_information_extractor_constructed"
    ]
    assert not report.claim_gate["carrier_retaining_decoder_ruled_out"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_invalid_fixed_tuple_labels_are_rejected() -> None:
    with pytest.raises(ValueError, match="partition pairs"):
        fixed_tuple_joint_purity(3, ())
    with pytest.raises(ValueError, match="partition pairs"):
        fixed_tuple_joint_purity(3, (((2,), (1, 1)),))
