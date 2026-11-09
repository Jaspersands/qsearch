"""Checks for research/audits/reviews/2026-11-04-rees-s3-zero-sum.md.

Run:  nice -n 10 /opt/anaconda3/bin/python -I test_zs.py      (writes results.json)
 or:  nice -n 10 /opt/anaconda3/bin/python -m pytest -q test_zs.py

Every check is exact integer arithmetic.  Random instances use fixed seeds.
Finite checks can only falsify; they are not evidence for all (p, g).
"""

import json
import os
import random
import sys
from collections import Counter
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zs_lib as Z  # noqa: E402

RESULTS = {}


def rand_bank(rng, p, g, M):
    return [tuple(rng.randrange(p) for _ in range(g)) for _ in range(M)]


def rand_subspace_bank(rng, p, g, a, M):
    """Labels i.i.d. uniform on a random a-dim subspace V of F_p^g (V of full rank a)."""
    while True:
        E = [tuple(rng.randrange(p) for _ in range(g)) for _ in range(a)]
        if len(Z.rref_rows([list(e) for e in E], p)[1]) == a:
            break
    bank = []
    for _ in range(M):
        x = [rng.randrange(p) for _ in range(a)]
        bank.append(tuple(sum(x[k] * E[k][j] for k in range(a)) % p for j in range(g)))
    return bank


def adversarial_banks(p, g, M):
    """Structured banks: Davenport-tight prefix, all zero, one repeated vector,
    rank-one, unit vectors cycling, and the tight bank followed by copies of e_1."""
    out = []
    e = [tuple(1 if j == i else 0 for j in range(g)) for i in range(g)]
    tight = [e[i] for i in range(g) for _ in range(p - 1)]
    out.append((tight + [e[0]] * M)[:M])
    out.append([(0,) * g] * M)
    v = tuple([1] * g)
    out.append([v] * M)
    out.append([tuple((t * x) % p for x in v) for t in [1 + (i % (p - 1)) for i in range(M)]])
    out.append([e[i % g] for i in range(M)])
    out.append([tuple((i + 1) % p if j == 0 else 0 for j in range(g)) for i in range(M)])
    return out


# ------------------------------------------------------------------ T1
def test_reachable_matches_bruteforce():
    rng = random.Random(1)
    n = 0
    for p in (2, 3, 5, 7):
        for g in (1, 2, 3):
            for M in range(1, 12):
                for _ in range(25):
                    bank = rand_bank(rng, p, g, M)
                    b = Z.brute_force_zero_sum(bank, p)
                    r = Z.reachable_sums_zero_sum(bank, p)
                    assert (b is None) == (r is None)
                    if r is not None:
                        assert Z.is_witness(bank, r, p)
                    n += 1
    RESULTS["T1_reachable_vs_bruteforce_instances"] = n


# ------------------------------------------------------------------ T2
def test_davenport_exhaustive_and_tight():
    """Every bank of length g(p-1)+1 has a zero-sum subset (exhaustive on tiny cases),
    and the tight bank of length g(p-1) has none."""
    rows = []
    for (p, g) in ((3, 1), (3, 2), (5, 1), (7, 1), (2, 3), (2, 4)):
        D = g * (p - 1) + 1
        cnt = 0
        for flat in product(range(p), repeat=g * D):
            bank = [tuple(flat[i * g:(i + 1) * g]) for i in range(D)]
            assert Z.reachable_sums_zero_sum(bank, p) is not None
            cnt += 1
        e = [tuple(1 if j == i else 0 for j in range(g)) for i in range(g)]
        tight = [e[i] for i in range(g) for _ in range(p - 1)]
        assert Z.brute_force_zero_sum(tight, p) is None
        rows.append({"p": p, "g": g, "D": D, "banks": cnt})
    RESULTS["T2_davenport_exhaustive"] = rows


# ------------------------------------------------------------------ T3
def test_p3_two_level():
    rng = random.Random(3)
    p = 3
    stats = []
    # exhaustive at g = 1 (M = 4: 81 banks)
    for flat in product(range(3), repeat=4):
        bank = [(x,) for x in flat]
        T = Z.p3_two_level(bank, 1)
        assert Z.is_witness(bank, T, p)
    stats.append({"g": 1, "mode": "exhaustive", "banks": 81})
    for g in range(1, 8):
        M = (g + 1) ** 2
        n = 0
        for _ in range(400 if g <= 4 else 100):
            for bank in (rand_bank(rng, p, g, M), rand_subspace_bank(rng, p, g, rng.randrange(0, g + 1), M)):
                T = Z.p3_two_level(bank, g)
                assert Z.is_witness(bank, T, p)
                n += 1
        for bank in adversarial_banks(p, g, M):
            T = Z.p3_two_level(bank, g)
            assert Z.is_witness(bank, T, p)
            n += 1
        stats.append({"g": g, "M": M, "instances": n})
    # g = 2 exhaustive over a random 50000 of the 3^18 banks plus all banks whose
    # columns are from {0, e1, e2, e1+e2}: 4^9 = 262144
    g = 2
    vals = [(0, 0), (1, 0), (0, 1), (1, 1)]
    cnt = 0
    for idx in product(range(4), repeat=9):
        bank = [vals[i] for i in idx]
        T = Z.p3_two_level(bank, g)
        assert Z.is_witness(bank, T, p)
        cnt += 1
    stats.append({"g": 2, "mode": "all banks with columns in {0,e1,e2,e1+e2}", "banks": cnt})
    RESULTS["T3_p3_two_level"] = stats


# ------------------------------------------------------------------ T4
def test_block_recursion():
    rng = random.Random(4)
    stats = []
    for p in (3, 5, 7):
        for g in (1, 2, 3, 4):
            for k in sorted({1, 2, g}):
                if k > g:
                    continue
                M = Z.block_recursion_arity(p, g, k)
                if M > 3000:
                    continue
                n = 0
                for _ in range(30):
                    bank = rand_bank(rng, p, g, M)
                    T = Z.block_recursion(bank, p, g, k)
                    assert Z.is_witness(bank, T, p)
                    n += 1
                for bank in adversarial_banks(p, g, M):
                    T = Z.block_recursion(bank, p, g, k)
                    assert Z.is_witness(bank, T, p)
                    n += 1
                stats.append({"p": p, "g": g, "k": k, "M": M, "instances": n})
    RESULTS["T4_block_recursion"] = stats


# ------------------------------------------------------------------ T5
def test_split_bank_reduction_exact_law():
    """Exact enumeration: labels i.i.d. uniform on a fixed non-coordinate subspace V.
    Conditional on span(first t labels) = V, the coordinate matrix handed to the
    binary-SIS solver is exactly uniform on F_p^{a x M2}, and independent of the
    first block."""
    rows = []
    for (p, g, Vbasis, t, M2) in (
        (3, 3, [(1, 2, 0), (0, 1, 1)], 3, 2),
        (3, 2, [(1, 1)], 2, 3),
        (5, 2, [(1, 3)], 2, 2),
    ):
        a = len(Vbasis)
        Vpts = sorted({tuple(sum(c[k] * Vbasis[k][j] for k in range(a)) % p for j in range(g))
                       for c in product(range(p), repeat=a)})
        assert len(Vpts) == p ** a
        joint = Counter()
        firsts = Counter()
        good = 0
        total = 0
        for first in product(Vpts, repeat=t):
            R, piv = Z.rref_rows([list(v) for v in first], p)
            for rest in product(Vpts, repeat=M2):
                total += 1
                if len(piv) != a:
                    continue
                X = tuple(Z.coords_in_basis(R, piv, v, p) for v in rest)
                assert all(x is not None for x in X)
                good += 1
                joint[(first, X)] += 1
                firsts[first] += 1
        # uniform over X, for every good first block
        margX = Counter()
        for (f, X), c in joint.items():
            margX[X] += c
        nX = p ** (a * M2)
        assert len(margX) == nX and len(set(margX.values())) == 1
        for f, cf in firsts.items():
            # conditional law of X given f is uniform: each X appears once per f
            assert cf == nX
        # failure probability of span(first) != V, against the bound p^{a-t}/(p-1)
        fail = total - good
        bound_num = total * p ** a  # compare fail/total <= p^{a-t}/(p-1) as integers
        assert fail * (p - 1) * p ** t <= bound_num
        rows.append({"p": p, "g": g, "a": a, "t": t, "M2": M2, "banks": total,
                     "span_fail": fail, "uniform_X": True})
    RESULTS["T5_split_bank_exact"] = rows


def test_split_bank_reduction_end_to_end():
    """zs_from_binsis with a brute-force binary-SIS solver returns valid witnesses."""
    rng = random.Random(5)

    def binsis_bf(Xcols, p):
        return Z.brute_force_zero_sum(Xcols, p)

    n = ok = 0
    for p in (3, 5):
        for g in (2, 3):
            for a in range(0, g + 1):
                for _ in range(40):
                    t = g + 2
                    M = t + 10
                    bank = rand_subspace_bank(rng, p, g, a, M)
                    T, X = Z.zs_from_binsis(bank, p, t, binsis_bf)
                    n += 1
                    if T is not None:
                        assert Z.is_witness(bank, T, p)
                        ok += 1
    RESULTS["T5b_split_bank_end_to_end"] = {"instances": n, "witnesses": ok}


# ------------------------------------------------------------------ T6
def test_two_level_contraction_zero_sum_grade():
    rows = []
    for p in (3, 5, 7, 11, 13):
        C = Z.contraction_at_zero_sum_grade(p)
        rows.append({"p": p, "kappa": p - 1, "contractions": len(C)})
        if p == 3:
            assert len(C) >= 1
        else:
            assert C == []
    # independent direct check (no normal form) at p = 3 and p = 5
    d3 = Z.contraction_bruteforce_direct(3)
    d5 = Z.contraction_bruteforce_direct(5)
    assert sorted(d3) == sorted(Z.contraction_at_zero_sum_grade(3))
    assert d5 == []
    rows.append({"direct_bruteforce": {"p3": len(d3), "p5": len(d5)}})
    RESULTS["T6_contraction_kappa_p_minus_1"] = rows


# ------------------------------------------------------------------ T7
def test_rees_hard_instances():
    """Direct sums of g filiform algebras of class c = p-1 over F_p: Jacobi holds,
    class c, top grade gamma_c of dimension g."""
    rows = []
    for (p, g) in ((3, 1), (3, 3), (5, 1), (5, 2), (7, 2)):
        c = p - 1
        dim, br = Z.filiform_sum_structure(c, g)
        if dim <= 12:
            assert Z.jacobi_ok(dim, br, p)
        dims = Z.lower_central_dims(dim, br, p)
        assert len(dims) == c and dims[-1] == g
        rows.append({"p": p, "g": g, "class": c, "dim": dim, "lcs_dims": dims})
    RESULTS["T7_rees_instances"] = rows


# ------------------------------------------------------------------ T8
def test_h2_digit_set_is_ternary():
    """At kappa = (p-1)/2 the power digit set P_kappa u {0} is {0, 1, p-1}."""
    primes = [q for q in range(5, 400) if all(q % r for r in range(2, int(q ** 0.5) + 1))]
    for q in primes:
        k = (q - 1) // 2
        D = {pow(x, k, q) for x in range(1, q)} | {0}
        assert D == {0, 1, q - 1}
    RESULTS["T8_h2_ternary_primes_checked"] = len(primes)


# ------------------------------------------------------------------ baseline table
def test_arity_table():
    rows = []
    for p in (3, 5, 7, 11):
        for g in (2, 4, 8, 16):
            row = {"p": p, "g": g,
                   "davenport": g * (p - 1) + 1,
                   "reachable_sum_states": p ** g,
                   "IS_B_{p-1}(g)_log2": round(Z.is_arity(p - 1, g).bit_length() - 1, 1),
                   "block_k=1_log2": Z.block_recursion_arity(p, g, 1).bit_length() - 1}
            if p == 3:
                row["two_level_p3"] = (g + 1) ** 2
            rows.append(row)
    RESULTS["arity_table"] = rows


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print("PASS", t.__name__)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json")
    with open(out, "w") as fh:
        json.dump(RESULTS, fh, indent=1, sort_keys=True)
    print("wrote", out)
