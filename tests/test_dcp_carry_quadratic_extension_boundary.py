import math

import pytest

from dcp_carry_quadratic_extension_boundary import (
    audit_carry_extension,
    audit_natural_primal_graph,
    build_carry_quadratic_extension_report,
    carry_bit_width,
    carry_column_residuals,
    carry_extension_scaling_record,
    derive_carry_witness,
    primal_clique_failure_log2_upper_bound,
    write_carry_quadratic_extension_report,
)


def test_carry_recurrence_exactly_characterizes_modular_fiber():
    row = audit_carry_extension(4, (1, 2, 4, 7, 9, 13), 11)
    assert row.assignment_count == 64
    assert row.exact_fiber_size == row.extension_acceptance_count
    assert row.projection_mismatch_count == 0
    assert row.nonunique_carry_witness_count == 0
    assert row.maximum_observed_carry < row.register_count
    assert row.exact_projection_verified


def test_derived_witness_satisfies_every_integer_column_equation():
    labels = (3, 5, 7, 11, 13)
    modulus_bits = 4
    for assignment in range(1 << len(labels)):
        target = sum(
            label
            for index, label in enumerate(labels)
            if (assignment >> index) & 1
        ) % (1 << modulus_bits)
        carries = derive_carry_witness(
            labels,
            target,
            modulus_bits,
            assignment,
        )
        assert carries is not None
        assert not any(
            carry_column_residuals(
                labels,
                target,
                modulus_bits,
                assignment,
                carries,
            )
        )


def test_polynomial_extension_size_uses_logarithmic_carry_width():
    assert carry_bit_width(1) == 1
    assert carry_bit_width(7) == 3
    assert carry_bit_width(8) == 4
    with pytest.raises(ValueError, match="positive"):
        carry_bit_width(0)

    row = carry_extension_scaling_record(128)
    assert row.carry_bit_width == math.ceil(
        math.log2(row.register_count + 1)
    )
    assert row.auxiliary_carry_bit_count == (
        row.modulus_bits * row.carry_bit_width
    )
    assert row.polynomial_size_degree_two_extension_certified


def test_natural_column_factors_make_original_variables_a_clique():
    row = audit_natural_primal_graph(4, (3, 5, 7, 9, 11))
    assert row.shared_one_pair_count == row.original_variable_pair_count
    assert row.missing_shared_one_pair_count == 0
    assert row.original_variable_clique_verified
    assert row.natural_primal_treewidth_lower_bound == row.register_count - 1

    nonclique = audit_natural_primal_graph(3, (1, 2, 4))
    assert not nonclique.original_variable_clique_verified
    assert nonclique.missing_shared_one_pair_count == 3


def test_random_primal_clique_union_bound_is_exponentially_small():
    rows = [
        carry_extension_scaling_record(bits)
        for bits in (64, 128, 256, 512)
    ]
    assert all(row.random_natural_linear_treewidth_certified for row in rows)
    assert all(
        row.natural_primal_treewidth_lower_bound == row.register_count - 1
        for row in rows
    )
    assert all(
        row.primal_clique_failure_probability_log2_upper_bound
        <= -0.1 * row.modulus_bits
        for row in rows
    )
    assert primal_clique_failure_log2_upper_bound(256, 260) < -90


def test_report_refutes_degree_lower_bound_without_claiming_solver(tmp_path):
    report = build_carry_quadratic_extension_report(
        scaling_modulus_bits=(64, 128),
    )
    assert report.theorem.theorem_verified
    assert report.theorem.exact_degree_two_extension_constructed
    assert report.theorem.high_anf_degree_as_representation_lower_bound_refuted
    assert report.theorem.natural_column_factor_linear_treewidth_proved
    assert not report.theorem.every_auxiliary_decomposition_high_width_proved
    assert not report.theorem.polynomial_witness_solver_constructed
    assert report.claim_gate[
        "polynomial_size_degree_two_carry_extension_exists"
    ]
    assert report.claim_gate["alternative_auxiliary_low_width_route_alive"]
    assert not report.claim_gate["speedup_claim_allowed"]

    payload = write_carry_quadratic_extension_report(
        tmp_path / "carry-extension.json",
        scaling_modulus_bits=(64, 128),
    )
    assert payload["status"] == (
        "low-degree-carry-extension-exact-natural-width-linear"
    )
