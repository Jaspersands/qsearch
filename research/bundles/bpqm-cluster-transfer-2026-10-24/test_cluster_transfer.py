from collections import defaultdict
from copy import deepcopy
from fractions import Fraction as F
from itertools import combinations
from math import comb, sqrt
from pathlib import Path
import random
import sys

import numpy as np
import pytest

import cluster_transfer as t

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "central-rank-2026-10-23"))
from central_rank import row_basis


@pytest.mark.parametrize("seed", range(12))
def test_kernel_independent_exhaustive_and_existing_rref(seed):
    rng, n = random.Random(seed), 6
    rows = tuple(rng.randrange(1 << n) for _ in range(seed))
    basis = t.kernel_basis(rows, n)
    actual = set(t.span(basis))
    expected = {x for x in range(1 << n) if t.image(rows, x) == 0}
    assert actual == expected
    if rows:
        rank = len(row_basis([tuple(row >> j & 1 for j in range(n)) for row in rows], 2))
        assert n-len(basis) == rank
    geometry = t.kernel_geometry(rows, n)
    assert geometry["mean_jump"] == F(sum(x.bit_count() for x in actual), len(actual))


@pytest.mark.parametrize("rows,n", [((1, 2, 3), 2), ((1, 1, 0), 2),
                                    ((0, 0), 1), ((), 3), ((1, 2, 4), 3)])
@pytest.mark.parametrize("c", [F(0), F(1, 3), F(13, 20)])
def test_duality_and_joint_distance_against_gram(rows, n, c):
    laws = t.finite_laws(rows, n, c)
    assert sum(laws["annealed"].values()) == 1
    assert sum(laws["quenched"].values()) == 1
    assert laws["eta"] == laws["joint_tv"]
    columns = tuple(t.image(rows, 1 << i) for i in range(n))
    code = [x for x in range(1 << len(rows)) if t.image(columns, x) == 0]
    gram = np.array([[float(c)**((x ^ y).bit_count()) for y in code] for x in code])
    eigenvalues = np.linalg.eigvalsh(gram)
    assert eigenvalues.min() > -1e-12
    success_gram = (sum(np.sqrt(np.maximum(eigenvalues, 0)))/len(code))**2
    p = laws["coset_probabilities"]
    success_cosets = sum(sqrt(float(a)/len(p)) for a in p)**2
    assert success_gram == pytest.approx(success_cosets, abs=1e-12)
    assert float(laws["eta"]) <= sqrt(max(0, 1-success_cosets))+1e-12
    for j in range(1 << len(rows)):
        assert sum(laws["gibbs"][j, x] for x in range(1 << n)) == 1
        marginal = sum(laws["annealed"][j, x] for x in range(1 << n))
        assert all(laws["annealed"][j, x]/marginal == laws["gibbs"][j, x]
                   for x in range(1 << n))


@pytest.mark.parametrize("rows,n", [((1, 2, 3), 2), ((1, 1, 0), 2), ((3,), 2)])
@pytest.mark.parametrize("c", [F(0), F(1, 2), F(13, 20)])
def test_annealed_step_is_bernoulli_kernel_and_quenched_is_not_assumed(rows, n, c):
    laws = t.finite_laws(rows, n, c)
    displacement, after = defaultdict(F), defaultdict(F)
    for (j, x), mass in laws["annealed"].items():
        for y, chance in t.finite_step(rows, n, c, j, x).items():
            displacement[x ^ y] += mass*chance
            after[j, y] += mass*chance
    assert displacement == t.bernoulli_kernel_law(rows, n, c)
    assert after == laws["annealed"]
    for j in range(1 << len(rows)):
        kernel = [t.finite_step(rows, n, c, j, x) for x in range(1 << n)]
        for x in range(1 << n):
            assert sum(kernel[x].values()) == 1
            for y in range(1 << n):
                assert laws["gibbs"][j, x]*kernel[x].get(y, F(0)) == \
                    laws["gibbs"][j, y]*kernel[y].get(x, F(0))


def test_trajectory_tv_transfer_is_once_not_per_step():
    rows, n, c = (1, 1), 1, F(2, 3)
    laws = t.finite_laws(rows, n, c)
    distance = F(0)
    for j in range(4):
        for x in range(2):
            for y, p in t.finite_step(rows, n, c, j, x).items():
                for z, q in t.finite_step(rows, n, c, j, y).items():
                    distance += abs(laws["annealed"][j, x]-laws["quenched"][j, x])*p*q/2
    assert distance == laws["eta"]


def test_replanting_or_using_uniform_signs_does_not_give_stationary_fixed_instance():
    laws = t.finite_laws((1, 1), 1, F(2, 3))
    masses = [sum(laws["annealed"][j, x] for x in range(2)) for j in range(4)]
    assert masses != [F(1, 4)]*4
    assert laws["joint_tv"] > 0
    # Even at c=0, a gauge repair preserving the coset hits only 2^{-(m-r)}.
    flat = t.finite_laws((1,)*8, 1, F(0))
    assert flat["eta"] == 0
    assert flat["coset_probabilities"] == (F(1, 128),)*128


def test_fixed_start_uniform_signs_has_different_retention_rate():
    rows, n, c = (1, 2, 3), 2, F(13, 20)
    fixed_start = defaultdict(F)
    for j in range(1 << len(rows)):
        for y, chance in t.finite_step(rows, n, c, j, 0).items():
            fixed_start[y] += chance/(1 << len(rows))
    assert fixed_start == t.bernoulli_kernel_law(rows, n, c/(1+c))
    assert fixed_start != t.bernoulli_kernel_law(rows, n, c)


def test_kernel_nullity_is_not_mobility():
    n = 32
    rows = tuple((1 << i) | (1 << (i+1)) for i in range(n-1))
    geometry = t.kernel_geometry(rows, n)
    assert geometry["nullity"] == 1
    assert geometry["mean_jump"] == 16
    assert geometry["active_coordinates"] == 32


@pytest.mark.parametrize("c", [F(0), F(1, 2), F(13, 20)])
def test_socket_first_moment_against_all_marked_slot_positions(c):
    n, h, total = 2, 1, F(0)
    for locations in combinations(range(12), 6):
        marks = set(locations)
        odd = sum(sum(j in marks for j in range(start, start+3)) % 2
                  for start in range(0, 12, 3))
        total += (1-c)**odd
    exact = F(comb(n, h), comb(12, 6))*total
    assert t.expected_weight_count(n, h, c) == exact
    assert t.expected_weight_count(n, 0, c) == 1
    assert t.expected_weight_count(n, n, c) == (1-c)**(2*n)


def test_rational_uniform_entropy_certificate():
    certificate = t.make_certificate()
    assert len(certificate["intervals"]) == 98
    assert t.verify_certificate(certificate)
    assert F(certificate["cutoff"]) == F(1, 50)
    assert t.mobility_bound(4096, certificate) < F(14, 10**11)
    for n in range(1, 9):
        for h in range(1, n+1):
            assert t.expected_weight_count(n, h, F(13, 20)) <= \
                (6*n+1)*F(99, 100)**n


@pytest.mark.parametrize("mutation", ["gap", "truncated", "wrong_z", "wrong_c", "wrong_decay"])
def test_bad_certificate_rejected(mutation):
    certificate = deepcopy(t.make_certificate())
    if mutation == "gap":
        certificate["intervals"][1]["left"] = "1/25"
    elif mutation == "truncated":
        certificate["intervals"].pop()
    elif mutation == "wrong_z":
        certificate["intervals"][0]["z"] = "1"
    elif mutation == "wrong_c":
        certificate["c"] = "1/2"
    else:
        certificate["decay"] = "1/2"
    with pytest.raises(ValueError):
        t.verify_certificate(certificate)


def test_bound_preserves_unknown_and_keeps_precision_direction():
    assert t.conditional_trajectory_bound(F(1, 100), 3, None) is None
    bound = t.conditional_trajectory_bound(F(1, 1000), 10, F(1, 100), bits=20)
    assert F(11, 100) <= bound < F(11, 100)+F(1, 2**20)
    assert t.upward_dyadic(F(1, 3), 16) >= F(1, 3)
    assert t.upward_dyadic(F(0)) == 0


def test_conditional_conductance_bound_not_mixing_admission():
    result = t.bounded_cut_flow(F(1, 3), F(1, 1000), F(1, 1000))
    assert result["conductance_upper"] == F(3, 500)
    assert result["ruled_out_time_upper_exclusive"] == F(125, 3)
    assert t.bounded_cut_flow(F(1, 3), F(0), F(0))["conductance_upper"] == 0


def test_scalable_path_does_not_call_enumeration(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("state enumeration is forbidden")
    monkeypatch.setattr(t, "span", forbidden)
    rng, n, c = random.Random(260024), 512, F(13, 20)
    rows = t.socket_rows(n, rng)
    assert len(rows) == 2*n
    assert all(row.bit_count() in (1, 3) for row in rows)
    signs, x = t.planted_start(rows, n, c, rng)
    y, geometry = t.cluster_step(rows, n, c, signs, x, rng)
    assert 0 <= y < 1 << n
    assert geometry["rank"]+geometry["nullity"] == n


@pytest.mark.parametrize("bad", [-1, F(1), 0.65, True])
def test_invalid_overlap_rejected(bad):
    with pytest.raises(ValueError):
        t.overlap(bad)


def test_reference_caps_and_bad_rows_rejected():
    with pytest.raises(ValueError):
        t.finite_laws((1,)*9, 2, F(1, 2))
    with pytest.raises(ValueError):
        t.expected_weight_count(100, 50, F(1, 2))
    with pytest.raises(ValueError):
        t.kernel_basis((8,), 3)
    with pytest.raises(ValueError):
        t.span((1, 2, 4), cap=4)
