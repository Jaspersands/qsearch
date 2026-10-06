from fractions import Fraction
import itertools

import pytest

from dcp_affine_cube_hierarchy import (
    best_cube_gate, cube_free_cap_density, cube_free_cap_exact, cube_source_bound,
    cube_tail_compression_bound, dense_half_width_source_bound, finite_pattern_menu_bound,
    half_width_rank_gate, parity_incidence_matrix, selected_block_polar_certificate,
    phase_separation_countercontrol,
)
from dcp_carry_packets import binary_rank
from dcp_physical_phase_noise import read
from dcp_pivot_span_obstructions import _columns_value, _nullspace, _row_basis


def test_integer_parity_matrix_inverse_accounts_for_all_two_adic_torsion():
    for r in range(1, 7):
        P = parity_incidence_matrix(r)
        for i, row in enumerate(P):
            for j, other in enumerate(P):
                assert sum(a * (2 * b - 1) for a, b in zip(row, other)) == (1 << (r - 1)) * (i == j)


def test_complete_full_pattern_modular_tables_preserve_nonzero_torsion_solutions():
    for r, a, expected in ((2, 3, Fraction(2, 512)), (3, 2, Fraction(32, 16384))):
        P, Q = parity_incidence_matrix(r), 1 << a
        successes = 0
        for sums in itertools.product(range(Q), repeat=len(P)):
            if all(sum(x * s for x, s in zip(row, sums)) % Q == 0 for row in P):
                successes += 1
                assert all((s << (r - 1)) % Q == 0 for s in sums)
        assert Fraction(successes, Q ** len(P)) == expected


def test_partial_nonempty_pattern_sets_have_correct_necessary_divisibility():
    P, Q = parity_incidence_matrix(3), 8
    for patterns in ((0, 1, 3), (0, 1, 2, 3), (0, 2, 4, 6)):
        successes = 0
        for sums in itertools.product(range(Q), repeat=len(patterns)):
            if all(sum(row[p] * s for p, s in zip(patterns, sums)) % Q == 0 for row in P):
                successes += 1
                assert all(4 * s % Q == 0 for s in sums)
        assert Fraction(successes, Q ** len(patterns)) <= Fraction(1, 2 ** len(patterns))


def test_nonempty_pattern_count_entropy_inequality_uses_exact_integer_powers():
    for r in range(2, 17):
        for h in range(r, 129):
            assert (h + 1) ** r <= (r + 1) ** h
        row = cube_source_bound(16, 2080, 65, r)
        p = row["log2_cube_dimension_plus_one_upper_bound_numerator"]
        assert (r + 1) ** 32 <= 1 << p
        assert (r + 1) ** 32 > 1 << (p - 1)


def test_symbolic_geometric_bound_is_never_below_finite_pattern_menu_bound():
    for n, width, a, r in itertools.product((1, 2, 3), (4, 8, 12, 32), (2, 4, 12, 32), (2, 3, 4)):
        for conditioned in (False, True):
            finite = finite_pattern_menu_bound(n, width, a, r, prefix_conditioned=conditioned)
            row = cube_source_bound(n, width, a, r, prefix_conditioned=conditioned)
            assert finite <= Fraction(1, 1 << row["source_mean_incident_point_mass_upper_bound_dyadic_exponent"])


def test_geometric_gap_and_precision_failures_are_inconclusive_not_negative_results():
    row = cube_source_bound(8, 528, 33, 6)
    assert row["per_pattern_probability_gap_bits"] < 0
    assert row["source_mean_incident_point_mass_upper_bound_dyadic_exponent"] == 0
    row = cube_source_bound(16, 100, 3, 5)
    assert row["pattern_sum_divisibility_bits"] == 0
    assert row["source_mean_incident_point_mass_upper_bound_dyadic_exponent"] == 0


def test_cube_free_cap_recurrence_matches_planes_and_bounds_small_subsets():
    from dcp_terminal_affine_fibers import bounded_affine_planes, sidon_cap_bound
    assert all(cube_free_cap_exact(d, 2) == sidon_cap_bound(d) for d in range(2, 65))
    cubes = [sum(1 << x for x in plane) for plane in bounded_affine_planes(4)]
    hyperplanes = [sum(1 << x for x in range(16) if ((x & h).bit_count() & 1) == c)
                   for h in range(1, 16) for c in (0, 1)]
    for r, forbidden in ((2, cubes), (3, hyperplanes), (4, [65535])):
        bound, observed = cube_free_cap_exact(4, r), 0
        for mask in range(65536):
            if mask.bit_count() < observed:
                continue
            if not any(mask & cube == cube for cube in forbidden):
                observed = max(observed, mask.bit_count())
                assert observed <= bound
        assert observed >= 3


def test_integer_cap_density_bound_is_above_exact_recurrence_at_growing_dimensions():
    for d in range(1, 129):
        for r in range(1, min(d + 1, 13) + 1):
            cap = cube_free_cap_exact(d, r)
            bits = cube_free_cap_density(d, r)["cube_free_fiber_density_upper_bound_dyadic_exponent"]
            assert cap * (1 << bits) <= 1 << d
    assert cube_free_cap_density(12_585_984, 17)["cube_free_fiber_density_upper_bound_dyadic_exponent"] > 100


def test_more_original_states_do_not_automatically_escape_physical_affine_tail_geometry():
    cases = ((16, 1300, 65, 3, 62), (16, 2080, 65, 7, 14),
             (32, 8256, 129, 6, 126), (64, 32896, 257, 6, 511),
             (64, 49344, 257, 12, 14))
    for n, m, L, r, bits in cases:
        row = best_cube_gate(n, m, L)["best_deterministic_design_gate"]
        assert row["source"]["cube_dimension"] == r
        assert row["compression"]["conservative_single_dyadic_exponent"] == bits
        assert row["compression"]["uniform_secret_source_mean_acceptance_proved_below_two_thirds"]
        assert not row["compression"]["full_quantum_decoder_ruled_out"]


def test_constant_gap_two_term_bound_is_not_discarded_when_single_dyadic_is_vacuous():
    row = best_cube_gate(32, 12384, 129)["best_deterministic_design_gate"]["compression"]
    assert row["conservative_single_dyadic_exponent"] == 0
    assert row["rank_adjusted_nonincident_probability_dyadic_exponent"] == 1
    assert row["source_exception_probability_dyadic_exponent"] == 1419
    assert row["uniform_secret_source_mean_acceptance_proved_below_two_thirds"]


def _subspaces(width):
    return sorted({basis for d in range(1, width + 1)
                   for rows in itertools.combinations(range(1, 1 << width), d)
                   if len(basis := _row_basis(rows, width)) == d}, key=lambda x: (len(x), x))


def test_all_small_physical_kernel_subspaces_obey_generic_rank_gate():
    checked = 0
    spaces = {k: _subspaces(k) for k in (3, 4)}
    parity_codes = [[(r,) for r in range(1, 32)],
                    sorted({_row_basis((u, v), 5) for u in range(1, 32) for v in range(u + 1, 32)})]
    for codes in parity_codes:
        for R in codes:
            K = _nullspace(R, 5)
            for directions in spaces[len(K)]:
                W = [_columns_value(K, w) for w in directions]
                row = selected_block_polar_certificate(R, 5, W)
                assert max(row["actual_scalar_polar_ranks"]) >= row["all_block_gate"][
                    "some_actual_scalar_carry_polar_rank_lower_bound"]
                checked += 1
    assert checked == 4371


def test_binary_full_support_row_does_not_exist_but_generic_rank_proof_still_applies():
    R = (45, 54)  # Column types10,01,11, repeated; every binary combination has zeros.
    assert all(w != 63 for w in (R[0], R[1], R[0] ^ R[1]))
    K = _nullspace(R, 6)
    row = selected_block_polar_certificate(R, 6, K)
    assert row["all_block_gate"]["zero_binary_columns"] == 0
    assert row["all_block_gate"]["some_actual_scalar_carry_polar_rank_lower_bound"] == 2
    assert max(row["actual_scalar_polar_ranks"]) >= 2


def test_zero_columns_are_real_free_directions_not_false_rank_obstructions():
    row = selected_block_polar_certificate((3,), 6, (4, 8, 16, 32))
    assert row["all_block_gate"]["zero_binary_columns"] == 4
    assert row["actual_scalar_polar_ranks"] == [0]
    assert not row["all_block_gate"]["all_tail_dimensional_physical_affine_full_modulus_fibers_excluded"]


def test_quadratic_rank_bias_bound_covers_every_linear_term_and_can_be_sharp():
    for bits in range(1 << 6):
        edges = [(i, j) for i in range(4) for j in range(i + 1, 4)]
        rows = [0] * 4
        active = [edge for j, edge in enumerate(edges) if bits >> j & 1]
        for i, j in active:
            rows[i] |= 1 << j
            rows[j] |= 1 << i
        rank = binary_rank(rows, 4)
        bound = Fraction(1, 2) + Fraction(1, 1 << (rank // 2 + 1))
        for linear in range(16):
            values = [((linear & x).bit_count() + sum((x >> i & 1) * (x >> j & 1) for i, j in active)) % 2
                      for x in range(16)]
            assert Fraction(max(values.count(0), values.count(1)), 16) <= bound
    R = (15,)
    row = selected_block_polar_certificate(R, 4, _nullspace(R, 4))
    assert row["actual_scalar_polar_ranks"] == [2]
    values = [x.bit_count() // 2 % 2 for x in range(16) if x.bit_count() % 2 == 0]
    assert Fraction(max(values.count(0), values.count(1)), len(values)) == Fraction(3, 4)


def test_native_source_zero_column_budget_is_charged_without_rejecting_all_zeros():
    for n, rho in ((8, 3), (16, 3), (64, 4), (64, 64)):
        L = 4 * n + 1
        row = dense_half_width_source_bound(n, rho * n * L, L)
        assert row["allowed_zero_binary_columns"] > 0
        assert row["uniform_secret_source_mean_acceptance_proved_below_two_thirds"]
        assert read(row["probability_zero_column_budget_exceeded_upper_bound"]) > 0
        assert not row["rank_two_targets_unknown_trash_or_general_decoder_ruled_out"]
    row = dense_half_width_source_bound(16, 2080, 65)
    assert not row["uniform_secret_source_mean_acceptance_proved_below_two_thirds"]


def test_exact_binomial_zero_count_tail_is_below_markov_budget():
    import math
    for n, width, L in ((2, 20, 3), (3, 36, 3)):
        row = dense_half_width_source_bound(n, width, L)
        trials, budget, p = width - n, row["allowed_zero_binary_columns"], Fraction(1, 1 << n)
        exact_tail = sum((math.comb(trials, j) * p ** j * (1 - p) ** (trials - j)
                          for j in range(budget + 1, trials + 1)), Fraction(0))
        assert exact_tail <= read(row["probability_zero_column_budget_exceeded_upper_bound"])


def test_clean_rank_and_geometry_scope_are_not_silently_dropped():
    source = cube_source_bound(16, 1300, 65, 3)
    rank_one = cube_tail_compression_bound(source, 260)
    rank_eight = cube_tail_compression_bound(source, 260, target_rank=8)
    assert rank_eight["rank_adjusted_nonincident_probability_dyadic_exponent"] == rank_one[
        "rank_adjusted_nonincident_probability_dyadic_exponent"] - 3
    assert not cube_tail_compression_bound(source, 2)["uniform_secret_source_mean_acceptance_proved_below_two_thirds"]
    with pytest.raises(ValueError):
        cube_tail_compression_bound(source, 4, target_rank=17)


def test_phase_separated_unknown_junk_can_decode_despite_failed_flat_tail_projection():
    row = phase_separation_countercontrol()
    assert read(row["exact_QFT_success_for_every_secret"]) == 1
    assert read(row["uniform_secret_mean_flat_junk_projection_probability"]) == Fraction(1, 4)
    assert read(row["independent_uniform_target_two_call_witness_baseline"][
        "independent_uniform_target_witness_success"]) == 1
    assert not row["clean_fixed_junk_is_necessary_for_a_DCP_decoder"]
    assert not row["source_prevalence_or_growing_dimension_decoder_proved"]
    assert not row["candidate_record_accepted"]


def test_nonzero_parity_coset_keeps_the_same_quadratic_polar_rank_gate():
    W = _nullspace((15,), 4)
    for origin in (0, 1):
        values = [((_columns_value(W, u) ^ origin).bit_count() - origin) // 2 % 2 for u in range(8)]
        assert Fraction(max(values.count(0), values.count(1)), 8) <= Fraction(3, 4)


@pytest.mark.parametrize("parameters", ((0, 12, 8, 3), (2, 2, 8, 3), (2, 12, 0, 3), (2, 12, 8, True)))
def test_invalid_source_domains_rejected(parameters):
    with pytest.raises(ValueError):
        cube_source_bound(*parameters)


def test_explicit_exponential_controls_have_budgets_and_invalid_parity_charts_fail():
    with pytest.raises(ValueError):
        parity_incidence_matrix(7)
    with pytest.raises(ValueError):
        finite_pattern_menu_bound(2, 1000, 8, 3)
    with pytest.raises(ValueError):
        cube_free_cap_exact(129, 6)
    with pytest.raises(ValueError):
        half_width_rank_gate((3, 3), 6, 4)
    with pytest.raises(ValueError):
        selected_block_polar_certificate((3,), 6, (1,))
