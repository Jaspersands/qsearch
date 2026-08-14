import math
from fractions import Fraction

import pytest

from coset_hyperoctahedral_color_weight_concentration import (
    audit_color_weight_law,
    binary_krawtchouk,
    build_color_weight_concentration_report,
    color_tv_upper_bound,
    color_weight_scaling_record,
    exact_color_character_multiplicity,
    exact_color_weight_probabilities,
    write_color_weight_concentration_report,
)


def test_binary_krawtchouk_orthogonality_control():
    m = 5
    for left in range(m + 1):
        for right in range(m + 1):
            inner = sum(
                Fraction(
                    binary_krawtchouk(m, left, weight)
                    * binary_krawtchouk(m, right, weight),
                    1,
                )
                * math.comb(m, weight)
                for weight in range(m + 1)
            )
            expected = (
                (2**m) * math.comb(m, left)
                if left == right
                else 0
            )
            assert inner == expected

    with pytest.raises(ValueError, match="invalid"):
        binary_krawtchouk(4, 5, 0)


@pytest.mark.parametrize(
    ("half_degree", "copy_count"),
    ((2, 1), (2, 2), (3, 1), (3, 2), (4, 2)),
)
def test_exact_color_weight_law_is_integral_and_normalized(
    half_degree, copy_count
):
    control = audit_color_weight_law(half_degree, copy_count)
    assert control.exact_fourier_weight_law_verified
    assert control.minimum_exact_color_multiplicity >= 0
    assert control.exact_weight_probability_sum == pytest.approx(1.0)
    assert control.maximum_equal_weight_probability_residual == 0.0
    assert control.exact_color_tv_from_uniform <= (
        control.character_tv_upper_bound + 1e-12
    )
    assert sum(exact_color_weight_probabilities(half_degree, copy_count)) == 1
    assert all(
        exact_color_character_multiplicity(half_degree, copy_count, weight) >= 0
        for weight in range(half_degree + 1)
    )


def test_balanced_color_mass_tends_to_one_under_alternative():
    rows = [
        color_weight_scaling_record(m) for m in (4, 8, 16, 32, 64, 128)
    ]
    assert all(row.copy_count >= row.half_degree for row in rows)
    assert all(row.color_weight_asymptotically_balanced for row in rows)
    assert all(row.balanced_little_group_qft_available for row in rows)
    assert all(not row.balanced_matrix_hecke_transfer_compiled for row in rows)
    assert rows[-1].alternative_balanced_mass_lower_bound > 0.999
    assert rows[-1].color_tv_upper_bound < 1e-20
    assert rows[-1].alternative_balanced_mass_lower_bound > rows[2].alternative_balanced_mass_lower_bound

    with pytest.raises(ValueError, match="at least two"):
        color_weight_scaling_record(1)
    with pytest.raises(ValueError, match="at least two"):
        color_tv_upper_bound(1, 2)


def test_report_localizes_without_compiling_residual_fusion(tmp_path):
    report = build_color_weight_concentration_report(
        finite_specs=((2, 1), (3, 1), (4, 2)),
        scaling_half_degrees=(4, 8, 16, 32, 64),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_color_weight_law_proved
    assert report.theorem.exponential_uniform_color_convergence_proved
    assert report.theorem.balanced_source_mass_proved
    assert report.theorem.balanced_alternative_mass_proved
    assert not report.theorem.balanced_residual_fusion_compiled
    assert not report.theorem.full_matrix_hecke_polar_compiled
    assert report.claim_gate[
        "natural_alternative_mass_concentrates_on_balanced_colors"
    ]
    assert not report.claim_gate["balanced_residual_multiplicity_basis_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_color_weight_concentration_report(
        tmp_path / "color-weight.json",
        finite_specs=((2, 1), (3, 1)),
        scaling_half_degrees=(4, 8, 16),
    )
    assert payload["status"] == (
        "balanced-color-alternative-mass-proved-residual-fusion-open"
    )
    assert payload["headline_metrics"][
        "balanced_matrix_hecke_compiler_count"
    ] == 0
