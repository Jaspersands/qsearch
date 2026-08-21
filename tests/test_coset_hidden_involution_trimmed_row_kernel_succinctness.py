import itertools

import pytest

from coset_hidden_involution_binary_decision_reduction import symmetric_group
from coset_hidden_involution_trimmed_row_kernel_succinctness import (
    audit_rooted_pairwise_kernel,
    brute_force_pairwise_kernel_support,
    build_trimmed_row_kernel_report,
    generated_action_is_transitive,
    polynomial_pairwise_kernel_support,
    product_plus_overlap,
    robust_seed_scaling_record,
    robust_transitive_seed,
    rooted_ordered_pair_conjugators,
    write_trimmed_row_kernel_report,
)
from coset_hyperoctahedral_free_orbit_canonicalization_boundary import (
    canonical_plus_cosets,
)
from coset_hyperoctahedral_trivial_color_mass_no_go import (
    canonical_matching_involution,
)


def _first_robust_pair(half_degree):
    hidden = canonical_matching_involution(half_degree)
    cosets = canonical_plus_cosets(half_degree)
    return next(
        pair
        for pair in itertools.product(cosets, repeat=2)
        if robust_transitive_seed(pair, hidden)
    )


def test_rooted_conjugators_equal_bruteforce_for_transitive_pairs():
    right = _first_robust_pair(2)
    left = tuple(reversed(right))
    rooted = rooted_ordered_pair_conjugators(right, left)
    brute = tuple(
        item
        for item in symmetric_group(4)
        if all(
            tuple(item[source[item.index(index)]] for index in range(4))
            == target
            for source, target in zip(right, left)
        )
    )
    assert generated_action_is_transitive(right)
    assert set(rooted) == set(brute)
    assert len(rooted) <= 4


@pytest.mark.parametrize("half_degree", (2, 3))
def test_polynomial_pairwise_support_matches_full_group_enumeration(half_degree):
    hidden = canonical_matching_involution(half_degree)
    right = _first_robust_pair(half_degree)
    cosets = canonical_plus_cosets(half_degree)
    left = (cosets[-1], cosets[len(cosets) // 3])
    polynomial = polynomial_pairwise_kernel_support(left, right, hidden)
    brute = brute_force_pairwise_kernel_support(left, right, hidden)
    assert set(polynomial) == set(brute)
    assert len(polynomial) <= 16 * (2 * half_degree)
    assert all(
        product_plus_overlap(left, right, item, hidden) > 0
        for item in polynomial
    )


def test_exact_finite_controls_verify_sparse_fourier_kernel():
    for half_degree, count in ((2, 4), (3, 5)):
        row = audit_rooted_pairwise_kernel(
            half_degree,
            control_pair_count=count,
        )
        assert row.rooted_pairwise_kernel_reconstruction_verified
        assert row.maximum_bruteforce_support_size > 0
        assert row.maximum_polynomial_support_size > 0
        assert row.maximum_support_set_mismatch_count == 0
        assert row.maximum_polynomial_support_size <= row.theorem_support_upper_bound
        assert row.maximum_rooted_conjugator_count_per_orientation <= row.degree
        assert row.maximum_fourier_matrix_residual < 1e-10
        assert not row.factorial_group_enumeration_needed_for_pairwise_kernel


def test_robust_trim_has_asymptotically_full_alternative_mass():
    rows = [robust_seed_scaling_record(value) for value in (5, 8, 16, 32, 64, 128)]
    assert all(row.pairwise_kernel_classically_polynomial for row in rows)
    assert all(not row.global_orbit_row_polar_compiled for row in rows)
    assert rows[-1].robust_trim_alternative_failure_upper_bound < 1e-40
    assert all(
        row.robust_trim_alternative_failure_log2_upper_bound < 0.0
        for row in rows
    )
    assert rows[-1].robust_trim_alternative_failure_log2_upper_bound < -1000.0
    assert all(
        right.total_robust_trim_failure_log2_upper_bound
        < left.total_robust_trim_failure_log2_upper_bound
        for left, right in zip(rows, rows[1:])
    )


def test_report_redirects_subduction_without_claiming_global_polar(tmp_path):
    report = build_trimmed_row_kernel_report()
    theorem = report.theorem
    assert theorem.theorem_verified
    assert theorem.regular_G_reduction_supersedes_generic_K_subduction_on_trimmed_mass
    assert theorem.polynomial_pairwise_conjugator_reconstruction_proved
    assert theorem.asymptotically_full_robust_trimmed_mass_proved
    assert theorem.pairwise_fourier_kernel_succinct
    assert not theorem.global_orbit_copy_transform_compiled
    assert not theorem.unnormalized_likelihood_fast_forward_compiled
    assert not theorem.speedup_claim_allowed
    assert not report.claim_gate["generic_K_subduction_required_on_trimmed_mass"]
    assert not report.claim_gate["pairwise_kernel_evaluation_is_quantum_advantage"]

    payload = write_trimmed_row_kernel_report(tmp_path / "row-kernel.json")
    assert payload["status"] == (
        "regular-row-pairwise-kernel-succinct-global-polar-open"
    )
    assert not payload["claim_gate"]["speedup_claim_allowed"]
