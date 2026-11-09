"""Tests for theorems/rees_coherent_sde_k2.py (coherent kappa_d = 2 SDE solve).

Default run < 60 s. REES_SLOW=1 adds larger exhaustive and sampled checks.
Report: research/audits/reviews/2026-11-04-rees-coherent-sde-k2.md.
"""
import math
import os

import numpy as np
import pytest

from theorems import rees_coherent_sde_k2 as K2
from theorems.rees_coherent_sde import Macro, Prog

SLOW = os.environ.get("REES_SLOW") == "1"
slow = pytest.mark.skipif(not SLOW, reason="set REES_SLOW=1")

CHECK_KEYS = ("output_equals_canonical", "inputs_restored", "workspace_clean",
              "witness_nonzero", "equation_holds", "canonical_padding_free")


def _all_ok(r):
    return all(r[k] for k in CHECK_KEYS)


# ---------------------------------------------------------------- constants and Lemma 1

@pytest.mark.parametrize("p", [q for q in range(3, 400) if K2.is_prime(q)])
def test_contraction_lemma1(p):
    m = K2.least_nonresidue(p)
    mu = m-1
    sq = {x*x % p for x in range(1, p)}
    assert m not in sq and all(t in sq for t in range(1, m))
    assert mu in sq
    alpha, beta = (1, 0), (0, mu)

    def n(y):
        return 0 if (y % p == 0 or y % p in sq) else 1
    # normalised contraction of prop:triangular-sde: alpha_j + beta_i in g^-(i+j) P u {0}
    for i in range(2):
        for j in range(2):
            v = (alpha[j]+beta[i]) % p
            assert v == 0 or n(v) == (i+j) % 2
    for z in range(1, p):
        for dl in range(1, p):
            w = z*dl*(alpha[n(z)]+beta[n(dl)]) % p
            assert w == 0 or w in sq


def test_bezout_exponent_and_refusals():
    for p in (3, 5, 7, 11, 13, 17, 29, 41):
        for d in range(2, 40, 2):
            if math.gcd(d, p-1) == 2:
                u = K2.bezout_exponent(p, d)
                for x in range(1, p):
                    if pow(x, (p-1)//2, p) == 1:
                        r = K2.rho(p, x)
                        assert r % 2 == 0 and r*r % p == x
                        assert pow(pow(r, u, p), d, p) == x
    for p, d in ((7, 3), (5, 4), (13, 4), (7, 1)):
        with pytest.raises(ValueError):
            K2.CoherentSDEK2(p, 1, d)


# ---------------------------------------------------------------- references

@pytest.mark.parametrize("p,a,n", [(3, 1, None), (5, 1, None), (7, 1, None), (13, 1, None),
                                   (3, 2, 400), (5, 2, 400), (13, 2, 300), (5, 3, 300), (7, 3, 200)])
def test_definition_equals_batch_reference(p, a, n):
    A = K2.all_inputs(p, a) if n is None else K2.structured_inputs(p, a, n, seed=7*p+a)
    s, x, K = K2.canonical_witness_k2_batch(p, A, 2)
    for i in range(A.shape[0]):
        cols = [tuple(int(v) for v in A[i, :, c]) for c in range(K2.columns(a))]
        r = K2.canonical_witness_k2(p, cols, 2)
        assert r["s"] == [int(v) for v in s[i]] and r["x"] == [int(v) for v in x[i]] and r["K"] == K[i]
        assert K2.check_witness(p, cols, 2, r["s"])
        assert r["x"][r["istar"]] == 1                   # Theorem 3: weight 1 at i*


def test_first_dependency_matches_kappa1_module():
    from theorems.rees_coherent_sde import canonical_witness
    rng = np.random.default_rng(3)
    for _ in range(300):
        p = int(rng.choice([3, 5, 7]))
        g = int(rng.integers(1, 4))
        cols = [tuple(int(v) for v in rng.integers(0, p, g)) if rng.random() < .7 else (0,)*g
                for _ in range(g+1)]
        _, y, j = canonical_witness(p, cols, 1)
        jj, yy = K2.first_dependency(p, cols)
        assert (j, list(y)) == (jj, yy)


def test_structured_inputs_hit_every_K():
    for p, a in ((5, 2), (5, 3), (3, 4)):
        _, _, K = K2.canonical_witness_k2_batch(p, K2.structured_inputs(p, a, 4096, seed=1), 2)
        assert set(K.tolist()) == set(range(a+1))


# ---------------------------------------------------------------- circuits: exhaustive

@pytest.mark.parametrize("p", [3, 5, 7, 11, 13])
def test_exhaustive_a1(p):
    r = K2.exhaustive_check(p, 1, 2)
    assert _all_ok(r) and r["roots_even"]


@pytest.mark.parametrize("p,d", [(7, 4), (13, 10), (3, 4)])
def test_exhaustive_a1_other_degrees(p, d):
    assert _all_ok(K2.exhaustive_check(p, 1, d))


def test_exhaustive_a2_p3():
    r = K2.exhaustive_check(3, 2, 2)
    assert r["inputs"] == 3**12 and _all_ok(r)
    assert all(v > 0 for v in r["K_hist"])


@pytest.mark.parametrize("p,a", [(5, 2), (7, 2), (11, 2), (13, 2), (3, 3), (5, 3)])
def test_sampled(p, a):
    r = K2.sampled_check(p, a, 2, n=512, seed=p*10+a)
    assert _all_ok(r) and r["roots_even"]


@pytest.mark.parametrize("p,a,n", [(5, 2, 150), (7, 3, 60), (13, 2, 100)])
def test_circuit_equals_definition_reference(p, a, n):
    """The circuit against the DEFINITION-level reference directly (not only the batch one)."""
    c = K2.CoherentSDEK2(p, a, 2)
    A = K2.structured_inputs(p, a, n, seed=p+31*a)
    sim = K2.BitSim(c.nw, n)
    for col in range(c.M):
        for r in range(a):
            sim.load(c.L[col][r], A[:, r, col])
    sim.run(c.flatten())
    s = np.stack([sim.read(c.S[col]) for col in range(c.M)], axis=1)
    for i in range(n):
        cols = [tuple(int(v) for v in A[i, :, col]) for col in range(c.M)]
        assert [int(v) for v in s[i]] == K2.canonical_witness_k2(p, cols, 2)["s"]


@pytest.mark.parametrize("p", [3, 5, 7, 13, 17, 41, 97])
def test_root_circuit_exhaustive(p):
    r = K2.root_check(p)
    assert r["root_ok"] and r["x_restored"] and r["workspace_clean"]


def test_root_circuit_bezout_power():
    for p, d in ((7, 4), (11, 4), (13, 10), (29, 6)):
        assert math.gcd(d, p-1) == 2
        r = K2.root_check(p, d)
        assert r["root_ok"] and r["workspace_clean"]


# ---------------------------------------------------------------- structure

def test_inputs_never_targeted_and_copy_stage_footprint():
    for p, a in ((5, 2), (13, 1), (3, 3)):
        c = K2.CoherentSDEK2(p, a, 2)
        inputs = {w for col in c.L for r in col for w in r}
        outs = {w for r in c.S for w in r}
        xs = {w for r in c.X for w in r}
        for it in c.prog:
            if isinstance(it, Macro):
                assert not set(it.args[0]) & inputs
            else:
                assert it[1][-1] not in inputs
        flips = {}
        for it in c.C:
            if isinstance(it, Macro):
                t = set(it.args[0])
                assert t <= outs or t <= {w for r in c.free for w in r}
            elif it[0] in ("cx", "ccx"):
                assert it[1][-1] not in xs and it[1][-1] not in inputs
            else:
                flips[it[1][0]] = flips.get(it[1][0], 0)+1
        assert all(v % 2 == 0 for w, v in flips.items() if w in xs)   # X on x come in pairs


def test_emitted_counts_equal_program_counts():
    for p, a, d in ((3, 1, 2), (5, 2, 2), (7, 1, 4), (13, 1, 2)):
        c = K2.CoherentSDEK2(p, a, d)
        g = c.flatten()
        cnt = c.counts()
        assert len(g) == cnt["gates"]["total"]
        assert sum(1 for x in g if x[0] == "ccx") == cnt["gates"]["ccx"]


@pytest.mark.parametrize("p,a,d", [(3, 1, 2), (5, 1, 2), (7, 2, 2), (13, 2, 10), (17, 3, 2),
                                   (41, 2, 2), (97, 1, 2), (257, 3, 2), (65537, 2, 2),
                                   (2**31-1, 2, 2), (2**61-1, 2, 2), (5, 8, 2)])
def test_closed_forms(p, a, d):
    r = K2.count_row(p, a, d)
    assert r["toffoli_matches"] and r["macros_match"] and r["qubits_match"]
    m = K2.closed_form_macros(p, a, d)
    assert K2.closed_form_products_poly(a, m["I_p"], m["L_p"], m["T_sqrt"], K2._ell(m["u"])) == r["add_product"]


# ---------------------------------------------------------------- mutations

def _mutant_fails(p, a, mutate=None, drop=None):
    c = K2.CoherentSDEK2(p, a, 2, mutate=mutate)
    if drop is not None:
        F = Prog(c.F)
        idx = drop(F)
        del F[idx]
        c.prog = Prog(F+c.C+c.F.inverse())
    A = K2.all_inputs(p, a) if p**(a*c.M) <= 600000 else K2.structured_inputs(p, a, 2048, seed=5)
    r = K2.check_circuit(c, A)
    return not _all_ok(r)


@pytest.mark.parametrize("p,a,mut", [(5, 2, {"m": 4}), (7, 2, {"m": 5}), (5, 1, {"mu": 2}),
                                     (3, 2, {"tau": 1}), (5, 1, {"out": 2})])
def test_constant_mutations_detected(p, a, mut):
    # each changed constant (back-substitution m, v's mu, tau sign, output sign)
    # breaks the canonical output on the stated input set
    assert _mutant_fails(p, a, mutate=mut)


def test_stop_lemma4_on_references():
    """Report Lemma 4 on the paper-faithful reference: at the stop round no delta is a
    non-residue, v_{K+1} = 0 and the stop-test coordinates y' vanish."""
    for p, a, n in ((3, 2, None), (5, 2, 3000), (7, 3, 1500), (13, 2, 1500)):
        A = K2.all_inputs(p, a) if n is None else K2.structured_inputs(p, a, n, seed=11)
        step = 5 if n is None else 1
        m, mu, offs = K2.least_nonresidue(p), K2.least_nonresidue(p)-1, K2.block_offsets(a)
        for i in range(0, A.shape[0], step):
            cols = [tuple(int(v) for v in A[i, :, c]) for c in range(K2.columns(a))]
            V = []
            for k in range(a+1):
                blk = [list(cols[offs[k]+t]) for t in range(a+1-k)]
                _, y = K2.first_dependency(p, V+blk)
                dl = y[k:]
                nonres = [t != 0 and pow(t, (p-1)//2, p) == p-1 for t in dl]
                v = [mu*sum(t*bl[r] for t, bl, nn in zip(dl, blk, nonres) if nn) % p for r in range(a)]
                fd = K2.first_dependency(p, V+[v])
                assert (fd is not None) == (not any(nonres)) == (not any(v))
                if fd is not None:
                    assert not any(fd[1][:k])
                    break
                V.append(v)


def _nth(kind, frac):
    def pick(F):
        idx = [i for i, it in enumerate(F) if not isinstance(it, Macro) and it[0] == kind]
        return idx[int(frac*(len(idx)-1))]
    return pick


@pytest.mark.parametrize("kind,frac", [("ccx", 0.0), ("ccx", 0.5), ("ccx", 0.97), ("x", 0.0)])
def test_gate_drop_mutations_detected(kind, frac):
    assert _mutant_fails(3, 2, drop=_nth(kind, frac))


def test_macro_drop_mutation_detected():
    def pick(F):
        return [i for i, it in enumerate(F) if isinstance(it, Macro)][-1]   # last x product
    assert _mutant_fails(5, 1, drop=pick)


# ---------------------------------------------------------------- slow

@slow
@pytest.mark.parametrize("p", [17, 19, 23, 29, 31, 37, 41])
def test_slow_exhaustive_a1(p):
    assert _all_ok(K2.exhaustive_check(p, 1, 2))


@slow
def test_slow_exhaustive_a2_p3_d4():
    assert _all_ok(K2.exhaustive_check(3, 2, 4))


@slow
@pytest.mark.parametrize("p,a,d", [(17, 2, 2), (41, 2, 2), (7, 2, 4), (13, 2, 10), (7, 3, 2),
                                   (11, 3, 2), (13, 3, 2), (3, 4, 2), (5, 4, 2)])
def test_slow_sampled(p, a, d):
    assert _all_ok(K2.sampled_check(p, a, d, n=4096, seed=p*100+a*10+d))


@slow
@pytest.mark.parametrize("p", [257, 65537])
def test_slow_root_circuit(p):
    r = K2.root_check(p)
    assert r["root_ok"] and r["workspace_clean"]
