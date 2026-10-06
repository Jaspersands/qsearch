import cmath
from fractions import Fraction
import itertools
import math

import pytest

from dcp_terminal_affine_fibers import (
    _source_control, affine_tail_compression_bound, bounded_affine_planes,
    bounded_fiber_incidence, charged_packet_menu_bound, direction_pair_counts,
    exact_plane_expectation, high_probability_point_mass_bound, native_affine_fiber_bound, sidon_cap_bound,
)


def test_direction_pair_classes_and_sixfold_plane_basis_count():
    for width in range(2, 7):
        actual = [0, 0]
        for u in range(1, 1 << width):
            for v in range(1, 1 << width):
                if u != v:
                    mask = (1 << width) - 1
                    categories = (u & ~v & mask, v & ~u & mask, u & v)
                    actual[all(categories)] += 1
        assert tuple(actual) == direction_pair_counts(width)
        assert len(bounded_affine_planes(width)) * 4 == sum(actual) * (1 << width) // 6


def test_overlap_two_torsion_is_not_missed_by_a_rank_three_probability():
    # All three direction-pattern classes are nonempty; their sums are q/2.
    row = bounded_fiber_incidence(((2, 2, 2),), 2)
    assert (0, 3, 5, 6) in row["constant_planes"]
    successes = 0
    for A in itertools.product(range(4), repeat=3):
        f = lambda x: sum(a for j, a in enumerate(A) if x >> j & 1) % 4
        successes += len({f(x) for x in (0, 3, 5, 6)}) == 1
    assert Fraction(successes, 4 ** 3) == Fraction(2, 4 ** 3)


def test_degenerate_pairs_have_rank_two_law_and_independent_rows_multiply():
    for n in (1, 2):
        successes = 0
        for entries in itertools.product(range(4), repeat=3 * n):
            f = lambda x: tuple(sum(entries[3 * l + j] for j in range(3) if x >> j & 1) % 4
                                for l in range(n))
            successes += len({f(x) for x in (0, 1, 6, 7)}) == 1
        assert Fraction(successes, 4 ** (3 * n)) == Fraction(1, 4 ** (2 * n))


def test_complete_source_laws_include_prefix_conditioning_and_uniform_kernel_points():
    for parameters in ((1, 3, 1), (1, 3, 2), (1, 3, 3), (2, 3, 1), (1, 4, 2)):
        row = _source_control(*parameters)
        assert row["complete_label_tables"] > row["prefix_accepted_tables"]
        assert not row["source_ledger"]["no_affine_plane_exists_anywhere_in_the_packet_proved"]


def test_fixed_anchor_covariance_under_all_physical_sign_patterns():
    planes = bounded_affine_planes(3)
    expected = exact_plane_expectation(1, 3, 2)
    counts = [0] * 8
    for A in itertools.product(range(4), repeat=3):
        values = [sum(a for j, a in enumerate(A) if x >> j & 1) % 4 for x in range(8)]
        for plane in planes:
            if len({values[x] for x in plane}) == 1:
                for x in plane:
                    counts[x] += 1
    assert all(Fraction(count, 4 ** 3) == expected for count in counts)


def test_typical_point_not_incident_does_not_imply_global_plane_absence():
    row = bounded_fiber_incidence(((1, 1, 1, 1),), 2)
    assert 0 not in row["incident_points"]
    assert row["constant_planes"]
    assert all(x.bit_count() == 2 for x in row["incident_points"])


def test_positive_signed_trade_family_is_preserved_not_declared_impossible():
    row = bounded_fiber_incidence(((1, 7, 2, 6),), 3)
    assert (0, 3, 12, 15) in row["constant_planes"]
    assert 0 in row["incident_points"]


def test_scaling_bound_is_symbolic_nonvacuous_and_not_an_empirical_seed_claim():
    expected = {4: 0, 8: 70, 16: 372, 32: 1591, 64: 6487}
    for n, bits in expected.items():
        row = native_affine_fiber_bound(n, n * (4 * n + 1) + 16, 4 * n + 1)
        assert row["source_mean_incident_point_mass_upper_bound_dyadic_exponent"] == bits
        assert row["every_public_label_adaptive_affine_chart_within_this_packet_covered"]
        assert not row["every_particular_packet_classified"]
        assert not row["nonlinear_charts_or_interblock_quantum_mixing_excluded"]
        assert not row["candidate_record_accepted"]
    # A very large exponent is retained without underflowing to zero or huge decimal strings.
    row = native_affine_fiber_bound(1024, 1024 * 4097 + 16, 4097)
    assert row["source_mean_incident_point_mass_upper_bound"].startswith("2^-")


def test_dyadic_source_bound_rounds_up_against_exact_counts():
    for n, width, a in itertools.product((1, 2, 3), range(3, 12), range(1, 12)):
        mean = exact_plane_expectation(n, width, a)
        for conditioned in (False, True):
            ledger = native_affine_fiber_bound(n, width, a, prefix_conditioned=conditioned)
            prefix = math.prod(1 - Fraction(1, 1 << j) for j in range(1, n + 1))
            exact_union = min(Fraction(1), mean * (1 << n) / prefix) if conditioned else min(Fraction(1), mean)
            assert exact_union <= Fraction(1, 1 << ledger[
                "source_mean_incident_point_mass_upper_bound_dyadic_exponent"])


def test_partial_precision_gate_is_vacuous_early_and_stronger_late():
    bits = [native_affine_fiber_bound(16, 1056, a)[
        "source_mean_incident_point_mass_upper_bound_dyadic_exponent"] for a in (32, 48, 56, 60, 65)]
    assert bits[:2] == [0, 0]
    assert 0 < bits[2] < bits[3] < bits[4]


def test_increased_state_supply_can_defeat_this_density_scoped_obstruction():
    assert native_affine_fiber_bound(16, 1248, 65)[
        "source_mean_incident_point_mass_upper_bound_dyadic_exponent"] == 65
    for width in (1300, 2080):
        assert native_affine_fiber_bound(16, width, 65)[
            "source_mean_incident_point_mass_upper_bound_dyadic_exponent"] == 0


def test_high_probability_packet_gate_is_markov_not_instance_classification():
    row = high_probability_point_mass_bound(native_affine_fiber_bound(32, 4144, 129))
    assert row["incident_point_fraction_threshold"] == "2^-795"
    assert row["packet_probability_of_exceeding_threshold_upper_bound"] == "2^-796"
    assert not row["this_particular_packet_classified"]
    assert not row["no_global_affine_plane_exists_in_good_packets_proved"]


def test_zero_secret_does_not_obey_the_uniform_secret_compression_ceiling():
    # On the even-parity physical chart x=(0,r0,r1), effective phases are r0+2r1 mod4.
    probabilities = [abs(sum(cmath.exp(2j * math.pi * s * r / 4) for r in range(4)) / 4) ** 2
                     for s in range(4)]
    assert probabilities[0] == 1
    assert sum(probabilities) / 4 == pytest.approx(0.25)


def test_sidon_cap_count_is_exhaustively_challenged_in_small_binary_blocks():
    for d in (2, 3, 4):
        size, cap, observed = 1 << d, sidon_cap_bound(d), 0
        for mask in range(1 << size):
            if mask.bit_count() > cap + 1:
                continue
            subset = [x for x in range(size) if mask >> x & 1]
            sums = [x ^ y for x, y in itertools.combinations(subset, 2)]
            if len(sums) == len(set(sums)):
                assert len(subset) <= cap
                observed = max(observed, len(subset))
        assert observed == cap
    assert sidon_cap_bound(16) == 362


def test_arbitrary_within_block_rank_projection_is_limited_by_fiber_eigenvalues():
    N, Q = 16, 4
    for A in ((1, 1, 1, 1), (1, 2, 3, 0), (0, 0, 0, 0), (1, 3, 2, 2)):
        row = bounded_fiber_incidence((A,), 2)
        values = [v[0] for v in row["values"]]
        counts = sorted((values.count(t) for t in set(values)), reverse=True)
        exceptions = len(row["incident_points"])
        for rank in (1, 2, 3):
            eigenvalue_mass = Fraction(sum(counts[:rank]), N)
            ceiling = min(Fraction(1), Fraction(rank * sidon_cap_bound(4) + exceptions, N))
            assert eigenvalue_mass <= ceiling
            # Known Walsh target subspaces, not targets allowed to depend on the secret.
            probability = sum(sum(abs(sum(((-1) ** ((x & target).bit_count())) *
                                         cmath.exp(2j * math.pi * s * values[x] / Q)
                                         for x in range(N)) / N) ** 2 for target in range(rank))
                              for s in range(Q)) / Q
            assert probability <= float(eigenvalue_mass) + 1e-12


def test_terminal_tail_gate_has_constant_gap_even_with_negligible_exception():
    ledger = native_affine_fiber_bound(8, 280, 33)
    row = affine_tail_compression_bound(ledger, 16)
    assert row["plane_free_fiber_size_upper_bound"] == "362"
    assert row["source_mean_exception_mass_upper_bound"] == "2^-70"
    assert not row["global_interblock_branch_mixing_or_nonlinear_physical_charts_covered"]
    assert not row["uniform_secret_mean_is_a_per_secret_guarantee"]
    assert not row["unrestricted_reset_or_secret_dependent_discarded_trash_covered"]


def test_packet_and_adaptive_pool_menu_costs_are_not_silently_ignored():
    row = native_affine_fiber_bound(16, 1056, 65)
    fixed_menu = charged_packet_menu_bound(row, packet_choices=16 ** 4)
    assert fixed_menu["selected_packet_source_mean_incident_point_mass_upper_bound_dyadic_exponent"] == 356
    pool = charged_packet_menu_bound(row, original_pool_states=16 ** 4)
    assert pool["vacuous_is_not_a_negative_result"]
    assert pool["menu_log2_upper_bound"] == 1056 * 16
    assert not pool["selection_independence_assumed"]


@pytest.mark.parametrize("parameters", ((0, 8, 4), (2, 1, 3), (2, 8, 0), (True, 8, 3)))
def test_invalid_native_source_parameters_rejected(parameters):
    with pytest.raises(ValueError):
        native_affine_fiber_bound(*parameters)


def test_exponential_controls_and_invalid_tail_models_are_explicitly_blocked():
    with pytest.raises(ValueError):
        bounded_affine_planes(8)
    with pytest.raises(ValueError):
        exact_plane_expectation(2, 257, 4)
    with pytest.raises(ValueError):
        affine_tail_compression_bound(native_affine_fiber_bound(2, 4, 4), 3)
    with pytest.raises(ValueError):
        affine_tail_compression_bound(native_affine_fiber_bound(2, 8, 4), 1)
    with pytest.raises(ValueError):
        charged_packet_menu_bound(native_affine_fiber_bound(2, 8, 4), packet_choices=2, original_pool_states=16)
