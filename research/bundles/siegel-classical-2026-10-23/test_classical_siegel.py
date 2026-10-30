from itertools import combinations, product
from random import Random

import pytest
from sympy import GF, Matrix, eye, zeros
from sympy.polys.matrices import DomainMatrix

from classical_siegel import (
    covering_frames, difference_sets, inverse, mod, recover,
    symplectic_form, uniform_symplectic,
)


def subspace_key(k, p):
    rows = DomainMatrix.from_Matrix(mod(k.T, p)).convert_to(GF(p)).rref()[0].to_Matrix()
    return tuple(int(x) % p for x in rows)


def hidden_plane_oracle(k, p, seed):
    rng, labels, used, calls = Random(seed), {}, set(), []
    j = symplectic_form(2)
    def oracle(matrix):
        assert mod(matrix.T*j*matrix-j, p) == zeros(4)
        calls.append(matrix)
        key = subspace_key(matrix*k, p)
        if key not in labels:
            while True:
                label = rng.getrandbits(128)
                if label not in used:
                    break
            labels[key] = label
            used.add(label)
        return labels[key]
    return oracle, calls


def all_lagrangians_three():
    p, j, vectors, seen = 3, symplectic_form(2), [], set()
    for values in product(range(p), repeat=4):
        if not any(values):
            continue
        leading = next(x for x in values if x)
        normalized = tuple(x*pow(leading, -1, p) % p for x in values)
        if normalized not in seen:
            seen.add(normalized)
            vectors.append(Matrix(normalized))
    planes = {}
    for v, w in combinations(vectors, 2):
        if int((v.T*j*w)[0]) % p == 0:
            k = v.row_join(w)
            planes[subspace_key(k, p)] = k
    assert len(planes) == 40
    return tuple(planes.values())


@pytest.mark.parametrize("p", [3, 5, 7, 11, 101])
def test_difference_cover(p):
    aa, bb = difference_sets(p)
    assert {(b-a) % p for a in aa for b in bb} == set(range(p))


def test_all_forty_rank_two_planes_over_three():
    for i, k in enumerate(all_lagrangians_three()):
        oracle, calls = hidden_plane_oracle(k, 3, i+300)
        result = recover(oracle, 3)
        assert result["status"] == "RECOVERED_UNDER_ORACLE_PROMISE"
        assert subspace_key(result["basis"], 3) == subspace_key(k, 3)
        assert result["queries"] == len(calls) <= result["query_bound"]


@pytest.mark.parametrize("p", [5, 7, 13, 101, 257])
@pytest.mark.parametrize("seed", [0, 1, 5])
def test_fresh_native_queries_and_arbitrary_label_values(p, seed):
    k = uniform_symplectic(p, Random(seed+80))[:, [0, 2]]
    oracle, calls = hidden_plane_oracle(k, p, seed+500)
    result = recover(oracle, p)
    assert result["status"] == "RECOVERED_UNDER_ORACLE_PROMISE"
    assert subspace_key(result["basis"], p) == subspace_key(k, p)
    assert result["queries"] == len(calls) <= result["query_bound"]
    assert len(calls) < p*p+100


def test_budget_exhaustion_is_abort_not_a_false_negative():
    results = []
    for seed, k in enumerate(all_lagrangians_three()):
        oracle, _ = hidden_plane_oracle(k, 3, seed)
        result = recover(oracle, 3, chart_budget=1)
        results.append(result)
        assert result["charts_tried"] == 1
        assert not result["full_cover_budget"]
        if result["status"] == "ABORT":
            assert result["basis"] is None
        else:
            assert subspace_key(result["basis"], 3) == subspace_key(k, 3)
    assert any(r["status"] == "ABORT" for r in results)


def test_eight_frames_cover_every_lagrangian_over_three():
    frames = covering_frames(3)
    assert len(frames) == 8
    for k in all_lagrangians_three():
        good = []
        for c in frames:
            assert mod(c.T*symplectic_form(2)*c-symplectic_form(2), 3) == zeros(4)
            transformed = mod(inverse(c, 3)*k, 3)
            bottom = transformed[[1, 3], :]
            if int(bottom.det()) % 3:
                s = mod(transformed[[0, 2], :]*inverse(bottom, 3), 3)
                assert s == s.T
                good.append(bool(s[1, 1]))
        assert any(good)


def test_invalid_parameters_rejected():
    for p, budget in ((2, 1), (9, 1), (5, 0), (5, 9)):
        with pytest.raises(ValueError):
            recover(lambda _: 0, p, chart_budget=budget)
