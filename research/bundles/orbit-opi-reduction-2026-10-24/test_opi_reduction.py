from collections import Counter
from copy import deepcopy
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import random

from flint import nmod_mat
import numpy as np
import pytest

import opi_reduction as o


def fixture(p=13, K=3, seed=241026):
    g = o.geometry(p, 3, K)
    rng = random.Random(seed)
    nu = next(x for x in range(2, p) if pow(x, (p-1)//2, p) == p-1)
    b = tuple(rng.randrange(1, p) for _ in g.nodes)
    allowed = tuple(tuple(sorted(rng.sample(range(p), (p-1)//2))) for _ in g.nodes)
    return g, b, nu, allowed


@pytest.mark.parametrize("p", [7, 13, 19])
def test_vertex_uniformity_and_original_polynomial_identity(p):
    g, b, nu, _ = fixture(p, 2)
    for a, multiplier in zip(g.representatives[:2], b[:2]):
        counts = Counter()
        for u, v in product(range(p), repeat=2):
            A, B, C, beta = o.local_quadratic(p, g.root, a, multiplier, nu, u, v)
            x0 = (a*u+a*a*v) % p
            y0 = (g.root*a*u+g.root*g.root*a*a*v) % p
            z0 = (g.root*g.root*a*u+g.root*a*a*v) % p
            d, w = (x0-y0) % p, (z0-y0) % p
            alternative = (w-d*pow(1-nu, -1, p)-multiplier*nu*d*d*pow(1-nu, -1, p)
                           -pow(4*multiplier*(1-nu), -1, p)) % p
            assert beta == alternative
            counts[beta] += 1
            for t in range(p):
                native = (t+z0+multiplier*((t+x0)**2-nu*(t+y0)**2)) % p
                assert native == (A*t*t+B*t+C) % p
        assert set(counts.values()) == {p} and len(counts) == p


def test_all_seven_field_halfsets_have_the_exact_second_moment():
    p, h = 7, 3
    for halfset in combinations(range(p), h):
        for A in range(1, p):
            sizes = [sum((A*t*t+beta) % p in halfset for t in range(p)) for beta in range(p)]
            assert sum(sizes) == p*h
            assert sum((size-h)**2 for size in sizes) == h*(p-h)
            for ell in range(1, h+1):
                assert sum(size < ell for size in sizes) <= min(p, h*(p-h)//(h-ell+1)**2)


@pytest.mark.parametrize("K", [2, 3, 4])
def test_evaluation_rank_proves_required_independence(K):
    g = o.geometry(13, 3, K)
    for size in range(1, K+1):
        for subset in combinations(g.nodes, size):
            assert nmod_mat([[pow(z, j, g.p) for j in range(K)] for z in subset], g.p).rank() == size


def test_exact_pairwise_vertex_census_and_nonfull_independence():
    g, b, nu, _ = fixture(13, 2)
    pairs, triples = Counter(), Counter()
    for coefficients in product(range(13), repeat=4):
        betas = tuple(o.local_quadratic(13, g.root, a, v, nu,
                                       o.horner(coefficients[:2], z, 13),
                                       o.horner(coefficients[2:], z, 13))[3]
                      for a, z, v in zip(g.representatives, g.nodes, b))
        pairs[betas[:2]] += 1
        triples[betas[:3]] += 1
    assert len(pairs) == 13**2 and set(pairs.values()) == {13**2}
    assert len(triples) != 13**3 or set(triples.values()) != {13}


@pytest.mark.parametrize("K", [2, 3])
def test_bonferroni_bound_against_limited_independence_census(K):
    g = o.geometry(13, 3, K)
    hits = sum(all(o.horner(q, z, 13) != 0 for z in g.nodes)
               for q in product(range(13), repeat=K))
    actual = F(hits, 13**K)
    bound = o.bonferroni_lower(4, K, F(1, 13))
    assert 0 < bound <= actual
    if K == 2:
        assert actual < F(12, 13)**4  # Full-independence shortcut overstates success.


def test_bonferroni_fully_independent_and_zero_one_endpoints():
    assert o.bonferroni_lower(3, 3, F(1, 7)) == F(6, 7)**3
    assert o.bonferroni_lower(4, 2, F(0)) == 1
    assert o.bonferroni_lower(4, 2, F(1)) == 0
    with pytest.raises(ValueError):
        o.bonferroni_lower(4, 4, F(1, 13), 2)
    with pytest.raises(ValueError):
        o.bonferroni_lower(4, 2, F(1, 13), 3)
    with pytest.raises(ValueError):
        o.bonferroni_lower(4, 2, 0.1)


def frozen_trap():
    g, b, nu, _ = fixture(13, 2)
    halfsets = tuple(tuple(sorted(set(range(13))-{(v*(1-nu)*t*t+t) % 13 for t in range(13)}))
                     for v in b)
    return g, b, nu, halfsets


def test_frozen_zero_components_can_erase_every_reduced_list():
    g, b, nu, halfsets = frozen_trap()
    failed = o.restrict(g, b, nu, halfsets, (0, 0), (0, 0), 1)
    assert failed["status"] == "RETRY_SPARSE_LIST"
    assert failed["counts"] == (0, 0, 0, 0)
    assert failed["lists"] is None
    repaired = o.random_reduction(g, b, nu, halfsets, 2, seed=241026, attempts=4)
    assert repaired["status"] == "REDUCED_TO_SCALAR_OPI"


def test_failed_attempts_are_retained_and_charged(monkeypatch):
    g, b, nu, halfsets = frozen_trap()
    class ZeroCoins:
        def randrange(self, p):
            return 0
    monkeypatch.setattr(o.random, "Random", lambda _: ZeroCoins())
    result = o.random_reduction(g, b, nu, halfsets, 2, seed=0, attempts=3)
    assert result["status"] == "BUDGET_EXHAUSTED"
    assert result["restriction"] is None and len(result["history"]) == 3
    assert all(row["failed_indices"] == (0, 1, 2, 3) for row in result["history"])
    assert result["work"]["native_table_membership_lookups"] == 3*4*13
    assert result["work"]["random_field_draws"] == 3*2*2
    assert not result["native_witness_produced"]


@pytest.mark.parametrize("seed", [41, 42, 43, 44])
def test_small_scalar_solutions_lift_to_the_unchanged_native_relation(seed):
    g, b, nu, allowed = fixture(13, 3, seed)
    run = o.random_reduction(g, b, nu, allowed, 3, seed=24, attempts=10)
    reduced = run["restriction"]
    assert run["status"] == "REDUCED_TO_SCALAR_OPI"
    assert all(len(row) == 3 for row in reduced["lists"])
    witness = next(q for q in product(range(13), repeat=3)
                   if all(o.horner(q, z, 13) in row for z, row in zip(g.nodes, reduced["lists"])))
    lifted = o.lift_and_verify(g, b, nu, allowed, reduced, witness)
    assert lifted["status"] == "VERIFIED_NATIVE_PERFECT"
    assert lifted["scalar_score"] == lifted["native_score"] == 4
    assert lifted["degree"] < 9
    for q0 in ((0,), (1,), (1, 2, 3)):
        partial = o.lift_and_verify(g, b, nu, allowed, reduced, q0)
        assert partial["native_score"] >= partial["scalar_score"]
    assert not run["scalar_OPI_solver_executed"]
    assert run["seeded_replay_is_not_probability_evidence"]


def test_tampered_reduction_and_out_of_range_witness_rejected():
    g, b, nu, allowed = fixture()
    reduced = o.random_reduction(g, b, nu, allowed, 3, seed=24)["restriction"]
    changed = deepcopy(reduced)
    changed["counts"] = (13,)*4
    with pytest.raises(ValueError):
        o.lift_and_verify(g, b, nu, allowed, changed, (1,))
    for q0 in ((13,), (True,), (1, 2, 3, 4)):
        with pytest.raises(ValueError):
            o.lift_and_verify(g, b, nu, allowed, reduced, q0)


def test_finite_certificate_is_positive_without_a_quantum_execution_claim():
    g = o.geometry(2053, 3, 438)
    cert = o.certificate(g, 769)
    exact, B = o.success_lower(2053, 684, 438, 769)
    assert B == 15 and F(1, 200) < F(cert["success_lower_dyadic"]) <= exact < F(1, 100)
    assert F(cert["rate_plus_density_minus_one"]) > 0
    assert not cert["external_OPI_finite_length_threshold_instantiated"]


@pytest.mark.parametrize("case", ["square", "zero_multiplier", "repeated_halfset", "short_halfset",
                                  "bad_coefficient", "overdegree", "bad_ell", "noncubic"])
def test_invalid_native_contracts_rejected(case):
    g, b, nu, allowed = fixture()
    q1, q2, ell = (0,), (1,), 3
    if case == "square":
        nu = 1
    elif case == "zero_multiplier":
        b = (0,)+b[1:]
    elif case == "repeated_halfset":
        allowed = ((0,)*6,)+allowed[1:]
    elif case == "short_halfset":
        allowed = ((0,),)+allowed[1:]
    elif case == "bad_coefficient":
        q1 = (13,)
    elif case == "overdegree":
        q2 = (1, 2, 3, 4)
    elif case == "bad_ell":
        ell = 7
    else:
        g = o.geometry(13, 2, 3)
    with pytest.raises(ValueError):
        o.restrict(g, b, nu, allowed, q1, q2, ell)


def independent_horner(coefficients, x, p):
    total = 0
    for value in coefficients[::-1]:
        total = (total*x+value) % p
    return total


@pytest.mark.parametrize("run_index", [0, 1])
def test_saved_large_restrictions_replay_original_residual_not_quadratic_formula(run_index):
    root = Path(__file__).resolve().parent
    saved = json.loads((root/"receipt.json").read_text())
    for name, expected in saved["source_sha256"].items():
        assert hashlib.sha256((root/name).read_bytes()).hexdigest() == expected
    row = saved["native_restrictions"][run_index]
    parent = json.loads((root.parent/"orbit-norm-flat-2026-10-24/data/cubic-parent.json").read_text())["native"]
    domain = parent["domain"]
    p, nu = domain["p"], domain["eta_nonsquare"]
    restriction = row["result"]["restriction"]
    coefficients = [0]*row["dimension_in_this_run"]
    for residue, key in ((1, "q1"), (2, "q2")):
        for j, value in enumerate(restriction[key]):
            coefficients[3*j+residue] = value
    lists, counts = [], []
    t = np.arange(p, dtype=np.int64)
    with np.load(root.parent/"orbit-norm-flat-2026-10-24/data/native.npz", allow_pickle=False) as data:
        for i, points in enumerate(domain["orbits"]):
            x, y, z = [independent_horner(coefficients, point, p) for point in points]
            b = int(data["residual_coefficients"][i])
            # Adding constant t to P adds t at ALL three ORIGINAL points.
            residuals = (t+z+b*((t+x)**2-nu*(t+y)**2)) % p
            accepted = np.flatnonzero(data["allowed"][i][residuals])
            counts.append(len(accepted))
            lists.append(list(map(int, accepted[:restriction["ell"]])))
    assert counts == restriction["counts"]
    assert len(lists) == 684 and all(len(values) == 769 for values in lists)
    canonical = json.dumps(lists, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(canonical).hexdigest() == row["result"]["materialized_reduced_lists"]["sha256"]
    assert not row["native_polynomial_produced"]


def test_all_saved_small_witnesses_replay_without_reducer():
    root = Path(__file__).resolve().parent
    saved = json.loads((root/"receipt.json").read_text())
    for row in saved["small_lifts"]:
        g, coefficients = row["geometry"], row["witness"]["coefficients"]
        assert len(coefficients) == 3*g["row_length"]
        for i, a in enumerate(g["representatives"]):
            points = [a*pow(g["root"], ell, g["p"]) % g["p"] for ell in range(3)]
            x, y, z = [independent_horner(coefficients, point, g["p"]) for point in points]
            residual = (z+row["b"][i]*(x*x-row["nu"]*y*y)) % g["p"]
            assert residual in row["halfsets"][i]
            assert residual == row["witness"]["native_residuals"][i]
