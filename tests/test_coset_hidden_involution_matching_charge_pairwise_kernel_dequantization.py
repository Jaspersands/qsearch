from fractions import Fraction

from coset_hidden_involution_matching_charge_coherent_label_compiler import (
    matching_charge_term_count,
    matching_charge_term_from_index,
)
from coset_hidden_involution_matching_charge_pairwise_kernel_dequantization import (
    audit_nearest_switch_kernel,
    build_pairwise_kernel_dequantization_report,
    is_matching_charge_term,
    nearest_switch_intersection_formula,
    nearest_switch_kernel_formula,
    nearest_switched_matching,
    pairwise_kernel_scaling_record,
    reference_matching,
    write_pairwise_kernel_dequantization_report,
)


def test_reference_orbit_membership_predicate_accepts_every_indexed_term():
    for half_degree in (4, 5, 6):
        matching = reference_matching(half_degree)
        assert all(
            is_matching_charge_term(
                matching_charge_term_from_index(half_degree, index),
                matching,
            )
            for index in range(matching_charge_term_count(half_degree))
        )


def test_nearest_switch_intersection_has_exact_local_support_formula():
    for half_degree in range(4, 11):
        row = audit_nearest_switch_kernel(half_degree)
        assert row.observed_intersection_count == (
            nearest_switch_intersection_formula(half_degree)
        )
        assert row.expected_intersection_count == row.observed_intersection_count
        assert row.exact_local_support_formula_verified


def test_nearest_switch_kernel_simplifies_to_closed_rational_form():
    for half_degree in range(4, 20):
        expected = Fraction(
            half_degree**2 - 5 * half_degree + 9,
            half_degree * (half_degree - 1),
        )
        assert nearest_switch_kernel_formula(half_degree) == expected
        assert 1 - expected == Fraction(
            4 * half_degree - 9,
            half_degree * (half_degree - 1),
        )


def test_pairwise_kernel_classical_cost_and_near_parallel_scaling():
    rows = [pairwise_kernel_scaling_record(value) for value in (8, 16, 32, 64)]
    assert all(row.classical_time_exponent == 4 for row in rows)
    assert all(row.pairwise_kernel_classically_computable for row in rows)
    assert all(
        row.classical_membership_tests == row.charge_term_count for row in rows
    )
    scaled_deficits = [
        row.half_degree * row.nearest_switch_kernel_deficit for row in rows
    ]
    assert all(3.0 < value < 4.0 for value in scaled_deficits)


def test_report_dequantizes_only_pairwise_Gram_geometry():
    report = build_pairwise_kernel_dequantization_report()
    theorem = report.theorem
    assert theorem.exact_all_rank_nearest_switch_kernel_proved
    assert theorem.arbitrary_pairwise_kernel_polynomial_time_classical
    assert not theorem.charge_orbit_pairwise_fidelity_is_quantum_advantage
    assert not theorem.matrix_valued_spectral_transition_dequantized
    assert not theorem.noncommuting_higher_transition_moments_dequantized
    assert not theorem.all_copy_target_interference_dequantized
    assert not theorem.speedup_claim_allowed
    assert theorem.theorem_verified


def test_live_pairwise_kernel_report_is_json_serializable(tmp_path):
    output = tmp_path / "pairwise-kernel.json"
    payload = write_pairwise_kernel_dequantization_report(output)
    assert output.exists()
    assert payload["status"] == (
        "matching-charge-pairwise-kernel-dequantized-matrix-transition-open"
    )
    assert payload["claim_gate"]["pairwise_charge_kernel_classically_computable"]
    assert not payload["claim_gate"]["matrix_valued_spectral_transition_dequantized"]
    assert not payload["claim_gate"]["speedup_claim_allowed"]
