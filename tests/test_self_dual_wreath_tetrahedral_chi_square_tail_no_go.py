from __future__ import annotations

import math
from fractions import Fraction

import pytest

from self_dual_wreath_tetrahedral_chi_square_tail_no_go import (
    all_one_dimensional_physical_mass,
    audit_tetrahedral_class_signature,
    finite_physical_six_label_control,
    parity_tail_chi_square_contribution,
    parity_tail_scaling_record,
    run_tetrahedral_chi_square_tail_no_go,
    tetrahedral_signature_second_moment,
    tetrahedral_support_contributions,
    write_tetrahedral_chi_square_tail_no_go_report,
)


def test_exact_class_signature_chi_square_values() -> None:
    expected = {
        2: Fraction(7),
        3: Fraction(25, 2),
        4: Fraction(3581, 162),
        5: Fraction(805898791, 51840000),
    }
    for n, value in expected.items():
        assert tetrahedral_signature_second_moment(n) - 1 == value


def test_fifteen_support_masks_have_exact_low_support_decomposition() -> None:
    for n in range(3, 6):
        row = audit_tetrahedral_class_signature(n)

        assert row.support_mask_count == 15
        assert row.size_three_mask_count == 4
        assert row.size_four_mask_count == 3
        assert row.size_five_mask_count == 6
        assert row.exact_support_decomposition_verified
        assert row.exact_class_signature_duality_verified
        assert row.exact_decomposition_residual == "0"
        assert len(tetrahedral_support_contributions(n)) == 15


def test_trivial_sign_sector_gives_constant_chi_square_on_vanishing_mass() -> None:
    rows = [parity_tail_scaling_record(n) for n in (6, 8, 10, 20)]

    assert all(row.untrimmed_chi_square_vanishing_falsified for row in rows)
    assert all(not row.positive_mass_signal_certified for row in rows)
    assert rows[-1].exact_restricted_chi_square_contribution == pytest.approx(8.0)
    assert rows[-1].exact_all_one_dimensional_physical_mass < 1e-50
    assert rows[-1].any_one_dimensional_physical_mass_upper_bound < 1e-15


def test_parity_tail_formulas_are_exact() -> None:
    for n in range(2, 10):
        order = math.factorial(n)

        assert parity_tail_chi_square_contribution(n) == (
            Fraction(8) - Fraction(16, order**3) + Fraction(64, order**6)
        )
        assert all_one_dimensional_physical_mass(n) == Fraction(8, order**3)


def test_physical_label_transform_matches_class_signature_duality() -> None:
    for n in range(2, 5):
        row = finite_physical_six_label_control(n)

        assert row.physical_probability_sum_residual < 1e-9
        assert row.minimum_likelihood >= 0
        assert row.chi_square_duality_residual < 1e-9
        assert row.all_one_dimensional_mass_residual < 1e-9
        assert row.physical_mass_with_any_one_dimensional_label <= (
            row.union_bound_for_any_one_dimensional_label + 1e-9
        )


def test_finite_total_variation_does_not_set_an_asymptotic_gate() -> None:
    rows = [finite_physical_six_label_control(n) for n in range(2, 6)]

    assert all(row.total_variation_from_plancherel_product > 0 for row in rows)
    assert all(row.kl_divergence_bits > 0 for row in rows)
    assert rows[-1].total_variation_from_plancherel_product < rows[0].total_variation_from_plancherel_product


def test_report_rejects_raw_chi_square_but_keeps_trimmed_core_open(tmp_path) -> None:
    report = run_tetrahedral_chi_square_tail_no_go()

    assert report.claim_gate["physical_class_signature_chi_square_duality_proved"]
    assert report.claim_gate[
        "untrimmed_six_label_chi_square_vanishing_falsified"
    ]
    assert report.claim_gate[
        "constant_chi_square_witness_has_vanishing_physical_mass_proved"
    ]
    assert not report.claim_gate["untrimmed_chi_square_valid_positive_mass_metric"]
    assert not report.claim_gate["dimension_trimmed_total_variation_vanishes_proved"]
    assert not report.claim_gate["dimension_trimmed_total_variation_survives_proved"]
    assert not report.claim_gate[
        "final_label_conditioned_mutual_information_vanishes_proved"
    ]
    assert not report.claim_gate["algorithm_claim_allowed"]
    assert not report.claim_gate["speedup_claim_allowed"]

    path = tmp_path / "tetrahedral-chi-tail.json"
    payload = write_tetrahedral_chi_square_tail_no_go_report(path)
    assert path.exists()
    assert payload["headline_metrics"]["asymptotic_chi_square_lower_bound"] == 8
    assert payload["headline_metrics"]["positive_mass_measured_signal_count"] == 0
