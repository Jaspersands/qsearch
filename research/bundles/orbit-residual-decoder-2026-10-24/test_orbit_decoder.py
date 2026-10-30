from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import random

import numpy as np
import pytest
from flint import nmod_mat

import orbit_decoder as o


@pytest.mark.parametrize("p,width,K", [(7, 2, 2), (13, 3, 3), (17, 4, 3), (19, 3, 4)])
def test_fold_is_only_a_permutation_of_original_syndrome(p, width, K):
    g = o.geometry(p, width, K)
    rng = random.Random(17)
    errors = [[rng.randrange(p) for _ in range(width)] for _ in g.representatives]
    original = [sum(e*pow(x, j, p) for block, points in zip(errors, g.points)
                    for e, x in zip(block, points)) % p for j in range(g.dimension)]
    rows = o.syndrome(g, errors)
    assert [rows[h][j] for j in range(K) for h in range(width)] == original


@pytest.mark.parametrize("p,width,coefficients", [(7, 2, (2,)), (7, 3, (1, 4)),
                                                 (13, 3, (1, 11)), (5, 4, (1, 2, 3))])
def test_fixed_predicate_fourier_law_from_full_amplitudes(p, width, coefficients):
    grid = np.indices((p,)*width, dtype=np.int64)
    residual = (grid[-1]+sum(b*grid[j]**2 for j, b in enumerate(coefficients))) % p
    allowed = tuple(range((p-1)//2))
    rho = len(allowed)/p
    centered = (np.isin(residual, allowed).astype(float)-rho)/np.sqrt(rho*(1-rho))
    actual = np.fft.fftn(centered)/(p**width)
    local = (np.isin(np.arange(p), allowed).astype(float)-rho)/np.sqrt(rho*(1-rho))
    last = np.fft.fft(local)/p
    assert np.allclose(actual[..., 0], 0, atol=1e-13)
    assert np.sum(np.abs(actual)**2) == pytest.approx(1)
    for v in range(1, p):
        assert np.allclose(np.abs(actual[..., v])**2, abs(last[v])**2/p**(width-1), atol=1e-13)


def test_degenerate_quadratic_does_not_grant_uniform_free_frequencies():
    p = 7
    x, y, z = np.indices((p,)*3)
    centered = np.isin((z+x*x) % p, (0, 1, 2)).astype(float)-3/7
    transform = np.fft.fftn(centered)/p**3
    assert np.linalg.norm(transform[:, 1:, :]) < 1e-12
    assert np.linalg.norm(transform[:, 0, 1:]) > .1


def test_truncated_satisfying_source_norm_overlap_and_mean():
    # The triangular residual map has exactly p^(width-1) preimages per
    # residual, so this is its reduced amplitude calculation, not a circuit.
    p, M, cutoff = 7, 4, 2
    residues = np.indices((p,)*M)
    rho = 3/7
    masks = [np.isin(residues[i], [(i+j) % p for j in range(3)]) for i in range(M)]
    centered = [(mask.astype(float)-rho)/np.sqrt(rho*(1-rho)) for mask in masks]
    truncated = np.zeros((p,)*M)
    for flags in product((0, 1), repeat=M):
        if sum(flags) <= cutoff:
            term = np.ones((p,)*M)
            for i, flag in enumerate(flags):
                term *= np.sqrt(1-rho)*centered[i] if flag else np.sqrt(rho)
            truncated += term
    tau = float(o.binomial_tail(M, F(4, 7), cutoff))
    assert np.mean(truncated**2) == pytest.approx(1-tau)
    truncated /= np.sqrt(1-tau)
    satisfying = np.prod(np.array(masks), axis=0)/rho**(M/2)
    assert np.mean(satisfying**2) == pytest.approx(1)
    assert np.mean(satisfying*truncated) == pytest.approx(np.sqrt(1-tau))
    score = sum(mask.astype(float) for mask in masks)/M
    assert np.mean(truncated**2*score) >= 1-np.sqrt(tau)-1e-12


@pytest.mark.parametrize("right", [(1, 1), (2, 7), (0, 0)])
def test_exhaustive_three_row_rank_law_and_forbidden_zero_frequencies(right):
    g = o.geometry(19, 3, 4)
    p, s = g.p, 3
    columns = []
    for points, v in zip(g.points[:2], right):
        columns.append([tuple(sum(e*pow(x, j, p) for e, x in zip((u, w, v), points)) % p
                              for j in range(s)) for u, w in product(range(p), repeat=2)])
    failed = 0
    for x in columns[0]:
        for y in columns[1]:
            failed += all((x[i]*y[j]-x[j]*y[i]) % p == 0
                          for i, j in ((0, 1), (0, 2), (1, 2)))
    actual = F(failed, p**4)
    bound = o.rank_failure_bound(19, 3, 12, 2, 3)
    assert bound == F(20, 19**3)
    if all(right):
        assert actual == F(18, 19**3) <= bound
    else:
        assert actual > bound


@pytest.mark.parametrize("p,n,D,C", [(11, 8, 2, 3), (101, 40, 10, 11), (2053, 204, 67, 68)])
def test_general_projective_bound_reproduces_previous_pair_formula(p, n, D, C):
    s = n-2*C
    old = min(F(1), sum((F(comb(D, t)*(p**(2*t-s)-1), (p-1)*p**t)
                        for t in range(s//2+1, D+1)), F(0)))
    assert o.rank_failure_bound(p, 2, n, D, C) == old
    assert old <= o.rank_failure_bound(p, 2, n, D, C, exact=False)


def test_syndrome_only_decoder_recovers_three_rows_at_large_control():
    g, rng = o.geometry(2053, 3, 68), random.Random(261024)
    support = rng.sample(range(len(g.representatives)), 50)
    errors = [[0]*3 for _ in g.representatives]
    for j, i in enumerate(support):
        errors[i] = [rng.randrange(g.p), rng.randrange(g.p), j+1]
    result = o.decode(g, 51, o.syndrome(g, errors))
    assert result["status"] == "VERIFIED_UNIQUE"
    assert result["errors"] == errors
    assert result["cap_rank"] == 50
    assert result["source_error_or_support_supplied"] is False
    assert result["extra_quantum_copies"] == 0 and result["output_polynomials"] == 1


def test_whole_cap_acceptance_against_exhaustive_competitors():
    g = o.geometry(7, 3, 2)
    fibers = {}
    zero = [[0]*3 for _ in g.representatives]
    for support in range(len(g.representatives)):
        for values in product(range(7), repeat=3):
            error = [row[:] for row in zero]
            error[support] = list(values)
            key = tuple(map(tuple, o.syndrome(g, error)))
            fibers.setdefault(key, set()).add(tuple(map(tuple, error)))
    for key, originals in fibers.items():
        result = o.decode(g, 1, [list(row) for row in key])
        if result["status"] == "VERIFIED_UNIQUE":
            assert originals == {tuple(map(tuple, result["errors"]))}


def test_guard_rejects_a_concrete_mean_alias_but_keeps_zero_label():
    g = o.geometry(19, 3, 4)
    selected = [x for block in g.points[:4] for x in block]+[g.points[4][-1]]
    # Thirteen Vandermonde barycentric weights have zero first12 moments.
    weights = []
    for x in selected:
        denominator = 1
        for y in selected:
            if y != x:
                denominator = denominator*(x-y) % g.p
        weights.append(pow(denominator, -1, g.p))
    assert all(sum(w*pow(x, j, g.p) for w, x in zip(weights, selected)) % g.p == 0
               for j in range(g.dimension))
    e1, e2, shift = ([[0]*3 for _ in g.representatives] for _ in range(3))
    for i in range(2):
        e1[i] = weights[3*i:3*i+3]
        e2[i+2] = [(-w) % g.p for w in weights[3*(i+2):3*(i+3)]]
    shift[4][-1] = weights[-1]
    combined = [[(x+y) % g.p for x, y in zip(a, b)] for a, b in zip(e1, shift)]
    assert o.syndrome(g, combined) == o.syndrome(g, e2)
    assert combined != e2
    for error in (e1, e2):
        result = o.decode(g, 3, o.syndrome(g, error))
        assert result["status"] != "VERIFIED_UNIQUE"
    zero = [[0]*3 for _ in g.representatives]
    assert o.decode(g, 3, o.syndrome(g, zero))["status"] == "VERIFIED_UNIQUE"


def test_public_classical_flat_controls():
    p, nonresidue = 7, 3
    assert pow(nonresidue, (p-1)//2, p) == p-1
    assert [(x, y) for x, y in product(range(p), repeat=2)
            if (x*x-nonresidue*y*y) % p == 0] == [(0, 0)]
    # Every nonconstant affine-line residual is linear or a nonconstant
    # quadratic, hence has at least(p+1)/2 values, too many for a halfset.
    for constant, linear, quadratic in product(range(p), repeat=3):
        if linear or quadratic:
            assert len({(constant+linear*t+quadratic*t*t) % p for t in range(p)}) >= (p+1)//2
    assert all((t*t-t*t) % p == 0 for t in range(p))  # split width3 countercontrol
    for coefficients in ((1, 1, 1), (1, 2, 3), (2, 5, 6)):
        v = o.isotropic_ternary(p, coefficients)
        assert any(v)
        assert sum(c*x*x for c, x in zip(coefficients, v)) % p == 0


@pytest.mark.parametrize("trials,a,b,cutoff", [(4, 1, 2, 2), (7, 3, 7, 0), (9, 5, 11, 9)])
def test_binomial_integer_tail_against_direct_formula(trials, a, b, cutoff):
    q = F(a, b)
    expected = sum((comb(trials, j)*q**j*(1-q)**(trials-j)
                    for j in range(cutoff+1, trials+1)), F(0))
    assert o.binomial_tail(trials, q, cutoff) == expected


def test_perfect_search_bound_pays_both_heralds_and_no_execution_is_claimed():
    row = o.perfect_search_certificate()
    tau = o.binomial_tail(4096, F(6145, 12289), 2375)
    epsilon = o.rank_failure_bound(12289, 3, 9828, 2375, 2376, exact=False)
    actual_bound = tau+4096*(epsilon+o.sqrt_upper(tau)+o.sqrt_upper(epsilon))
    assert F(row["one_attempt_perfect_failure_upper_dyadic"]) >= actual_bound
    assert F(row["one_attempt_perfect_failure_upper_dyadic"]) < F(1, 10**7)
    assert F(row["source_truncation_preparation_success_lower"]) <= 1-tau
    assert row["quantum_circuit_executed"] is False and row["native_witness_produced"] is False
    assert row["classical_separation_or_novelty_claimed"] is False


@pytest.mark.parametrize("kwargs", [{"p": 21}, {"width": 4, "dimension": 12},
                                    {"width": 0}, {"degree": 3300}, {"dimension": 9827}])
def test_invalid_certificate_contracts_fail_closed(kwargs):
    with pytest.raises(ValueError):
        o.perfect_search_certificate(**kwargs)


def test_geometry_and_syndrome_contracts_fail_closed():
    with pytest.raises(ValueError):
        o.Geometry(19, 3, 1, (1, 2), 2)
    with pytest.raises(ValueError):
        o.Geometry(19, 3, 7, (1, 7), 2)
    g = o.geometry(19, 3, 4)
    with pytest.raises(ValueError):
        o.decode(g, 4, [[0]*4]*3)
    with pytest.raises(ValueError):
        o.decode(g, 3, [[0.]*4]*3)
