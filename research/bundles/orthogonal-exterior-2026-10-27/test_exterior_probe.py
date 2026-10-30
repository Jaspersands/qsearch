from fractions import Fraction
from itertools import product
import random

from flint import fmpz_mat
import pytest

import exterior_probe as ep
from exterior_controls import (all_maximal, all_subspaces, fixture_kernel, native_fixture,
                               fixed_singular_line_fraction, universal_collision)

op = ep.op


@pytest.mark.parametrize("n,p", [(2, 3), (3, 3), (4, 3), (4, 5)])
def test_schubert_cells_count_exactly_and_are_singular(n, p):
    count = sum(ep.gaussian_binomial(n, j, p)*p**((n-j)*(n-j-1)//2)
                for j in range(n+1))
    expected = 2
    for i in range(1, n):
        expected *= p**i+1
    assert count == expected
    if n <= 3:
        spaces = tuple(all_maximal(n, p))
        assert len(set(spaces)) == count
        assert all(op.is_maximal_singular(s, n, p) for s in spaces)
    for j in range(n+1):
        assert sum(1 for _ in all_subspaces(n, j, p)) == ep.gaussian_binomial(n, j, p)


@pytest.mark.parametrize("n,p", [(3, 3), (4, 5), (6, 2**127-1)])
def test_public_probe_group_law_and_special_orthogonal_legality(n, p):
    rng = random.Random(11)
    maximal = ep.sample_maximal(n, p, rng)
    probe = ep.make_probe(maximal, p)
    a, b = [tuple(rng.randrange(p) for _ in range(probe.width)) for _ in range(2)]
    ga, gb = probe.matrix(a), probe.matrix(b)
    assert op.is_orthogonal(ga, p) and int(fmpz_mat(ga).det()) % p == 1
    assert op.mm(ga, gb, p) == probe.matrix(op.add(a, b, p))
    assert probe.matrix((0,)*probe.width) == op.eye(2*n)


@pytest.mark.parametrize("k", [1, 2, 3])
def test_every_fiber_and_image_screen_over_all_80_maximal_spaces(k):
    n, p = 3, 3
    hidden = op.eye(6)[:k]
    for maximal in all_maximal(n, p):
        probe, oracle = ep.make_probe(maximal, p), op.OpaqueFixtureOracle(hidden, p)
        kernel = fixture_kernel(probe, hidden)
        support = probe.image_support(kernel)
        x = op.intersection(hidden, maximal, 6, p)
        if x:
            assert support == maximal
        elif n-k >= 2:
            assert support == op.intersection(maximal, ep.polar_complement(hidden, 6, p), 6, p)
            assert len(support) == n-k
        else:
            assert not kernel and not support
        origin = oracle(probe.matrix((0,)*probe.width))
        labels = {}
        for point in product(range(p), repeat=probe.width):
            label = oracle(probe.matrix(point))
            in_kernel = len(op.basis(kernel+(point,), p)) == len(kernel)
            assert (label == origin) == in_kernel
            if label in labels:
                delta = op.add(point, op.scale(-1, labels[label], p), p)
                assert len(op.basis(kernel+(delta,), p)) == len(kernel)
            else:
                labels[label] = point
        assert len(labels) == p**(probe.width-len(kernel))


def test_exact_good_support_distribution_and_all_hyperplane_escape_counts():
    n, k, p = 3, 1, 3
    hidden, counts = op.eye(6)[:1], {}
    ambient = ep.polar_complement(hidden, 6, p)
    for maximal in all_maximal(n, p):
        probe = ep.make_probe(maximal, p)
        support = probe.image_support(fixture_kernel(probe, hidden))
        if 0 < len(support) < n:
            counts[support] = counts.get(support, 0)+1
    assert len(counts) == 72 and set(counts.values()) == {1}
    assert Fraction(sum(counts.values()), 80) >= Fraction(5, 6)
    for functional in all_subspaces(len(ambient), 1, p):
        hyperplane_coordinates = op.nullspace(functional, len(ambient), p)
        hyperplane = op.basis(tuple(op.span_coordinates(v, ambient, p)
                                   for v in hyperplane_coordinates), p)
        hits = sum(m for space, m in counts.items()
                   if len(op.basis(hyperplane+space, p)) == len(hyperplane))
        contains_u = len(op.basis(hyperplane+hidden, p)) == len(hyperplane)
        assert Fraction(hits, 72) in ({Fraction(0), Fraction(1, 4)} if contains_u
                                       else {Fraction(1, 9)})


def test_rank_two_supports_have_three_good_extensions_each():
    n, p, hidden, counts, total = 4, 3, op.eye(8)[:2], {}, 0
    for maximal in all_maximal(n, p):
        total += 1
        probe = ep.make_probe(maximal, p)
        support = probe.image_support(fixture_kernel(probe, hidden))
        if 0 < len(support) < n:
            assert len(support) == 2
            counts[support] = counts.get(support, 0)+1
    assert total == 2240
    assert len(counts) == 648 and set(counts.values()) == {3}
    assert Fraction(sum(counts.values()), total) >= Fraction(5, 6)


@pytest.mark.parametrize("n,k,p", [(4, 1, 5), (4, 2, 3), (5, 3, 7),
                                   (6, 2, 2**127-1)])
def test_large_field_rotated_kernel_screen(n, k, p):
    rng = random.Random(57)
    hidden_frame = op.hyperbolic_frame(ep.sample_maximal(n, p, rng), p)
    hidden = op.image(hidden_frame, op.eye(2*n)[:k], p)
    for _ in range(8):
        maximal = ep.sample_maximal(n, p, rng)
        probe = ep.make_probe(maximal, p)
        kernel = fixture_kernel(probe, hidden)
        support = probe.image_support(kernel)
        if op.intersection(hidden, maximal, 2*n, p):
            assert support == maximal
        else:
            assert len(kernel) == (n-k)*(n-k-1)//2
            assert support == op.intersection(maximal, ep.polar_complement(hidden, 2*n, p), 2*n, p)


@pytest.mark.parametrize("n,k,seed", [(3, 1, 81), (4, 1, 82), (4, 2, 83)])
def test_opaque_native_controller_has_no_hidden_rank(n, k, seed):
    record = native_fixture(n, k, 3, seed)
    assert record["inferred_rank"] == k
    assert not record["hidden_rank_supplied"] and not record["quantum_algorithm_executed"]
    assert record["classical_oracle_queries"] >= 3**(n*(n-1)//2)


@pytest.mark.parametrize("n,p,bits", [(3, 3, 8), (4, 5, 40), (64, 2**127-1, 80)])
def test_full_budget_accounts_for_sampling_ranks_geometry_and_precision(n, p, bits):
    budget = ep.recovery_budget(n, p, bits)
    epsilon = Fraction(budget["error_target"])
    for key in ("geometry_failure_bound", "all_rank_failure_bound", "row_sampler_failure_bound"):
        assert Fraction(budget[key]) <= epsilon/4
    assert (Fraction(budget["row_sampler_failure_bound"])
            + Fraction(budget["integer_sampler_failure_bound"])) <= epsilon/4
    assert Fraction(budget["error_per_complete_instrument"])*budget["original_oracle_query_cap"] == epsilon/4
    assert budget["original_oracle_query_cap"] == budget["probe_cap"]*budget["fourier_samples_per_probe"]
    assert not budget["hidden_rank_required"] and not budget["all_ranks_classical_lower_bound_proved"]


def test_dense_and_field_contracts_and_blind_boundary():
    with pytest.raises(ValueError, match="dimension cap"):
        ep.recover_reference(lambda _: 0, 8, 127)
    with pytest.raises(ValueError, match="prime"):
        ep.sample_maximal(4, 9, random.Random(1))
    with pytest.raises(ValueError, match="width"):
        ep.skew_matrix((1,), 4, 3)
    n, p = 4, 3
    probe = ep.make_probe(op.eye(8)[:4], p)
    for k in (n-1, n):
        hidden = op.eye(8)[n:n+k]
        assert not fixture_kernel(probe, hidden)
        assert not probe.image_support(())


def test_undersampled_kernel_can_pollute_support_so_rank_error_must_be_charged():
    n, p = 4, 3
    probe = ep.make_probe(op.eye(8)[:4], p)
    hidden = op.eye(8)[4:6]
    actual_kernel = fixture_kernel(probe, hidden)
    fake_kernel = actual_kernel+(op.eye(probe.width)[1],)
    assert len(op.basis(fake_kernel, p)) > len(actual_kernel)
    fake_support = probe.image_support(fake_kernel)
    assert 0 < len(fake_support) < n
    assert any(op.polar(v, hidden[0], p) for v in fake_support)
    # A possible undersampled superspace passes the image screen but is
    # polluted. Unlike the old receiver, exact-sample soundness alone is
    # insufficient here: the theorem must charge every rank failure.


def test_random_integer_cap_is_explicit_not_unbounded_rejection():
    class RejectingBits:
        def getrandbits(self, width):
            return 2**width-1
    with pytest.raises(RuntimeError, match="integer sampler cap"):
        ep._randbelow(RejectingBits(), 3, 2)
    assert ep._randbelow(RejectingBits(), 1, 2) == 0


@pytest.mark.parametrize("p", [5, 7])
def test_exact_fixed_line_counts_for_classical_comparator(p):
    n, width = 3, 6
    identity = op.eye(width)
    v = op.add(identity[0], identity[n], p)
    jv = v[n:]+v[:n]
    reflection = tuple(tuple((int(i == j)-v[i]*jv[j]) % p for j in range(width))
                       for i in range(width))
    probe = ep.make_probe(identity[:n], p)
    root = probe.matrix(op.eye(probe.width)[0])
    jordan = ((1, 1, 0), (0, 1, 1), (0, 0, 1))
    dual = op.transpose(op.inverse(jordan, p))
    levi = tuple(tuple(jordan[i][j] if i < n and j < n else
                       dual[i-n][j-n] if i >= n and j >= n else 0
                       for j in range(width)) for i in range(width))
    frame = op.hyperbolic_frame(ep.sample_maximal(n, p, random.Random(69)), p)
    for matrix in (reflection, root, levi, frame):
        if universal_collision(identity, matrix, p):
            continue
        assert fixed_singular_line_fraction(matrix, p) <= Fraction(3, p)
    d = (p**n-1)*(p**(n-1)+1)
    assert fixed_singular_line_fraction(reflection, p) == Fraction(p**(2*n-2)-1, d)


def test_central_collisions_have_no_hidden_line_information():
    identity = op.eye(6)
    negative = tuple(op.scale(-1, row, 3) for row in identity)
    assert universal_collision(identity, negative, 3)
    assert fixed_singular_line_fraction(negative, 3) == 1
    probe = ep.make_probe(identity[:3], 3)
    noncentral = probe.matrix(op.eye(probe.width)[0])
    assert not universal_collision(identity, noncentral, 3)
    for maximal in all_maximal(3, 3):
        hidden = maximal[:1]
        oracle = op.OpaqueFixtureOracle(hidden, 3)
        assert oracle(identity) == oracle(negative)
