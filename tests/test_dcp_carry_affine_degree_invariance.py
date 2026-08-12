import math

import pytest

from dcp_carry_affine_degree_invariance import (
    audit_affine_degree_invariance,
    audit_carry_coefficient_identity,
    build_carry_affine_degree_report,
    carry_affine_degree_scaling_record,
    carry_anf_coefficient_from_generating_function,
    lucas_bit_from_binomial,
    selected_linear_degree,
    write_carry_affine_degree_report,
)


def test_lucas_identity_extracts_binary_digits():
    for value in range(128):
        for output_bit in range(6):
            assert lucas_bit_from_binomial(value, output_bit) == (
                (value >> output_bit) & 1
            )


def test_generating_function_matches_full_anf_and_exact_degree():
    row = audit_carry_coefficient_identity(
        (1, 3, 5, 7, 9, 11),
        2,
    )
    assert row.generating_function_coefficient_failure_count == 0
    assert row.lucas_truth_identity_failure_count == 0
    assert row.exact_degree_theorem_applicable
    assert row.exact_anf_degree == 4
    assert row.exact_top_degree_monomial_count >= math.comb(6, 4)
    assert row.exact_degree_theorem_verified


def test_target_complement_changes_only_the_constant_coefficient():
    labels = (1, 3, 5, 7, 2, 6)
    zero = audit_carry_coefficient_identity(labels, 2, target_bit=0)
    one = audit_carry_coefficient_identity(labels, 2, target_bit=1)
    assert zero.exact_anf_degree == one.exact_anf_degree == 4
    assert zero.exact_top_degree_monomial_count == (
        one.exact_top_degree_monomial_count
    )
    assert one.exact_degree_theorem_verified


def test_every_four_odd_label_monomial_has_coefficient_one():
    labels = (1, 3, 5, 7, 9, 11)
    for variable_mask in range(1 << len(labels)):
        if variable_mask.bit_count() == 4:
            assert carry_anf_coefficient_from_generating_function(
                labels,
                2,
                variable_mask,
            ) == 1


def test_invertible_affine_maps_preserve_degree():
    row = audit_affine_degree_invariance(
        (1, 3, 5, 7, 9, 11),
        2,
        (0b000011, 0b000110, 0b001100, 0b011000, 0b110000, 0b100000),
        0b101001,
    )
    assert row.linear_rank == row.variable_count
    assert row.original_degree == row.transformed_degree == 4
    assert row.degree_preserved

    with pytest.raises(ValueError, match="invertible"):
        audit_affine_degree_invariance(
            (1, 3, 5, 7),
            1,
            (1, 1, 2, 4),
        )


def test_random_label_scaling_certifies_linear_affine_invariant_degree():
    for modulus_bits in (128, 256, 512, 1024):
        row = carry_affine_degree_scaling_record(modulus_bits)
        assert row.register_count / 12 <= row.certified_anf_degree
        assert row.certified_anf_degree <= row.register_count / 6
        assert row.top_degree_monomial_log2_lower_bound > (
            0.05 * row.register_count
        )
        assert row.high_degree_failure_probability_log2_upper_bound < 0
        assert row.affine_invariant_linear_degree_certified
        assert row.bounded_degree_after_dense_gl_ruled_out

    output_bit, degree = selected_linear_degree(132)
    assert degree == 16
    assert output_bit == 4


def test_report_keeps_hardness_tensor_and_auxiliary_routes_open(tmp_path):
    report = build_carry_affine_degree_report(
        scaling_modulus_bits=(128, 256),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.arbitrary_invertible_affine_degree_reduction_ruled_out
    assert not report.theorem.auxiliary_variable_reformulation_ruled_out
    assert not report.theorem.tensor_rank_collapse_ruled_out
    assert not report.theorem.polynomial_subset_sum_solver_ruled_out
    assert not report.claim_gate["dense_gl_bounded_degree_escape_alive"]
    assert report.claim_gate["dense_gl_tensor_rank_route_alive"]
    assert report.claim_gate["auxiliary_variable_low_degree_lift_route_alive"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_carry_affine_degree_report(
        tmp_path / "carry-affine-degree.json",
        scaling_modulus_bits=(128, 256),
    )
    assert payload["status"] == "dense-affine-bounded-degree-carry-route-closed"
