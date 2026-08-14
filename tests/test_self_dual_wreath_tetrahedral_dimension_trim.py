from __future__ import annotations

import math

from representation_obstruction import integer_partitions
from self_dual_wreath_tetrahedral_dimension_trim import (
    canonical_dimension_threshold,
    run_tetrahedral_dimension_trim,
    tetrahedral_dimension_trim_record,
    write_tetrahedral_dimension_trim_report,
)


def test_canonical_threshold_satisfies_atom_count_contract() -> None:
    for n in (10, 12, 16, 20, 30):
        threshold = canonical_dimension_threshold(n)
        order = math.factorial(n)
        partitions = len(integer_partitions(n))
        log2_order = math.lgamma(n + 1) / math.log(2)

        assert threshold >= 1
        assert threshold <= math.sqrt(order) / (partitions * log2_order)


def test_trim_bounds_both_physical_and_product_mass() -> None:
    for n in (10, 16, 24, 30, 40, 50):
        row = tetrahedral_dimension_trim_record(n)

        assert row.six_coordinate_removed_mass_upper_bound < 1
        assert row.retained_physical_mass_lower_bound == (
            1 - row.six_coordinate_removed_mass_upper_bound
        )
        assert row.retained_product_mass_lower_bound == (
            row.retained_physical_mass_lower_bound
        )
        assert row.low_dimension_tail_tv_vanishing_certified
        assert row.low_dimension_tail_positive_kl_vanishing_certified


def test_removed_tv_and_positive_kl_bounds_decay() -> None:
    rows = [tetrahedral_dimension_trim_record(n) for n in (10, 20, 30, 40, 50)]

    assert [row.removed_total_variation_contribution_upper_bound for row in rows] == sorted(
        (row.removed_total_variation_contribution_upper_bound for row in rows),
        reverse=True,
    )
    assert [row.removed_positive_kl_contribution_upper_bound_bits for row in rows] == sorted(
        (row.removed_positive_kl_contribution_upper_bound_bits for row in rows),
        reverse=True,
    )
    assert rows[-1].removed_total_variation_contribution_upper_bound < 1e-8
    assert rows[-1].removed_positive_kl_contribution_upper_bound_bits < 1e-5


def test_threshold_is_near_sqrt_group_order_on_log_scale() -> None:
    row = tetrahedral_dimension_trim_record(50)

    assert row.canonical_dimension_threshold_log2 > 80
    assert row.canonical_relative_dimension_threshold_log2 > -30


def test_report_removes_tails_but_keeps_retained_bulk_open(tmp_path) -> None:
    report = run_tetrahedral_dimension_trim()

    assert report.claim_gate[
        "near_maximal_dimension_trim_has_vanishing_physical_mass_cost_proved"
    ]
    assert report.claim_gate[
        "removed_tail_total_variation_contribution_vanishes_proved"
    ]
    assert report.claim_gate[
        "removed_tail_positive_kl_contribution_vanishes_proved"
    ]
    assert report.claim_gate["trivial_sign_parity_tail_removed"]
    assert not report.claim_gate[
        "retained_high_dimension_total_variation_vanishes_proved"
    ]
    assert not report.claim_gate[
        "retained_high_dimension_total_variation_survives_proved"
    ]
    assert not report.claim_gate[
        "retained_high_dimension_conditional_information_survives_proved"
    ]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "dimension-trim.json"
    payload = write_tetrahedral_dimension_trim_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["retained_bulk_tv_kl_theorem_count"] == 0
    assert payload["headline_metrics"]["new_quantum_algorithm_count"] == 0
