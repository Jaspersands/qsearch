import itertools
import json
import math

from self_dual_wreath_branch_character_cyclic_quadrant_overlap import (
    alternating_interval_lower_bound_verified,
    audit_multiplier_correlations,
    audit_proper_subgroup_mass,
    cyclic_multiplier_correlation_numerator,
    cyclic_multiplier_range_overlap,
    cyclic_subgroup_fourier_mass,
    cyclic_subgroup_fourier_mass_formula,
    natural_contraction_scaling,
    quadrant_symbol,
    quotient_coset_symbol_sum,
    quotient_coset_symbol_sum_formula,
    run_cyclic_quadrant_overlap,
    write_cyclic_quadrant_overlap_report,
)
from self_dual_wreath_branch_character_natural_frobenius_word_map import (
    regular_range_overlap,
)


def test_quotient_coset_identity_is_exact_for_even_and_odd_indices() -> None:
    for order in range(2, 65):
        for index in range(1, order + 1):
            if order % index:
                continue
            subgroup_order = order // index
            for residue in range(subgroup_order):
                assert abs(
                    quotient_coset_symbol_sum(order, index, residue)
                    - quotient_coset_symbol_sum_formula(
                        order,
                        index,
                        residue,
                    )
                ) < 1e-12


def test_proper_subgroup_fourier_mass_is_zero_or_inverse_square() -> None:
    for order in range(2, 49):
        for index in range(2, order + 1):
            if order % index:
                continue
            assert math.isclose(
                cyclic_subgroup_fourier_mass(order, index),
                float(cyclic_subgroup_fourier_mass_formula(index)),
                rel_tol=1e-9,
                abs_tol=1e-9,
            )


def test_half_interval_proof_bound_holds_for_all_checked_units() -> None:
    for order in range(3, 513):
        for multiplier in range(2, order):
            if math.gcd(multiplier, order) == 1:
                assert alternating_interval_lower_bound_verified(
                    order,
                    multiplier,
                )


def test_integer_correlation_formula_matches_direct_four_ray_sum() -> None:
    for order in range(3, 65):
        for multiplier in range(2, order):
            if math.gcd(multiplier, order) != 1:
                continue
            direct = sum(
                (
                    quadrant_symbol(order, exponent).conjugate()
                    * quadrant_symbol(order, multiplier * exponent)
                ).real
                for exponent in range(order)
            )
            assert math.isclose(
                direct,
                cyclic_multiplier_correlation_numerator(order, multiplier),
                abs_tol=1e-12,
            )


def test_order_eight_multiplier_three_is_the_sharp_control() -> None:
    assert cyclic_multiplier_correlation_numerator(8, 3) == 4
    assert math.isclose(cyclic_multiplier_range_overlap(8, 3), 0.75)
    audit = audit_multiplier_correlations()
    assert audit.three_quarter_bound_verified
    assert audit.sharp_order_eight_control_verified
    assert audit.maximizing_order == 8
    assert audit.maximizing_multiplier == 3


def test_finite_nonabelian_regular_controls_obey_the_all_group_bound() -> None:
    for n in (3, 4):
        group = tuple(itertools.permutations(range(n)))
        for left in group:
            for right in group:
                if left != right:
                    assert regular_range_overlap(left, right) <= 0.75 + 1e-10


def test_natural_copy_scale_has_a_strictly_negative_power_exponent() -> None:
    rows = [natural_contraction_scaling(n) for n in (8, 16, 32, 64)]
    assert all(row.asymptotic_power_exponent < 0 for row in rows)
    assert all(row.conditioned_expected_residual_tends_to_zero for row in rows)
    assert all(
        right.log2_unconditioned_expected_residual_upper_bound
        < left.log2_unconditioned_expected_residual_upper_bound
        for left, right in zip(rows, rows[1:])
    )


def test_report_closes_frobenius_gate_but_not_access_or_speedup() -> None:
    subgroup = audit_proper_subgroup_mass()
    report = run_cyclic_quadrant_overlap()
    assert subgroup.maximum_proper_subgroup_coefficient_mass <= 1 / 9 + 1e-9
    assert report.theorem.theorem_verified
    assert report.claim_gate[
        "all_finite_group_three_quarters_range_overlap_proved"
    ]
    assert report.claim_gate[
        "collision_free_source_typical_frobenius_contraction_proved"
    ]
    assert not report.claim_gate["uniform_minimum_singular_value_proved"]
    assert not report.claim_gate["normalization_one_dense_transform_compiled"]
    assert not report.claim_gate["physical_pgm_decoder_compiled"]
    assert not report.claim_gate["speedup_claim_allowed"]


def test_writer_emits_live_artifact(tmp_path) -> None:
    path = tmp_path / "cyclic-quadrant-overlap.json"
    payload = write_cyclic_quadrant_overlap_report(path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["status"] == payload["status"]
    assert (
        loaded["headline_metrics"][
            "all_finite_group_three_quarter_range_overlap_theorem_count"
        ]
        == 1
    )
