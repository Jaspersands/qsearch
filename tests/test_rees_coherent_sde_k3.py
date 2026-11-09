"""Tests for theorems/rees_coherent_sde_kappa.py (coherent SDE solve at kappa_d >= 2,
checked mainly at kappa_d = 3).

Default run < 60 s. REES_SLOW=1 adds larger exhaustive, row-space and sampled checks.
Report: research/audits/reviews/2026-11-04-rees-coherent-sde-k3.md.
"""
import math
import os

import numpy as np
import pytest

from theorems import rees_coherent_sde_kappa as KK
from theorems import rees_coherent_sde_k2 as K2
from theorems.rees_coherent_sde import Macro, Prog

SLOW = os.environ.get("REES_SLOW") == "1"
slow = pytest.mark.skipif(not SLOW, reason="set REES_SLOW=1")


def _all_ok(r):
    return all(r[k] for k in KK.CHECK_KEYS)


# ---------------------------------------------------------------- constants

@pytest.mark.parametrize("p", [7, 13, 19])
def test_contraction_is_lex_least_bruteforce(p):
    assert KK.contraction_bruteforce(p, 3) == KK.canonical_contraction(p, 3)


def test_contraction_pruned_equals_unpruned_and_valid():
    for kappa, hi in ((2, 120), (3, 200), (4, 120)):
        for p in KK.primes_1_mod(kappa, 3, hi):
            c = KK.canonical_contraction(p, kappa)
            assert c == KK._canonical_contraction_lazy(p, kappa)
            if c is not None:
                assert KK.contraction_valid(p, kappa, KK.coset_generator(p, kappa), *c)
                assert all(b != 0 for b in c[1][1:])          # Lemma 3: beta_nu != 0, nu != 0


def test_known_exceptional_sets():
    # E_2(3) empty below 400; E_2(4) below 60 equals main.tex's {5, 13, 17, 29, 37, 53}
    assert all(KK.canonical_contraction(p, 3) is not None for p in KK.primes_1_mod(3, 3, 400))
    assert [p for p in KK.primes_1_mod(4, 3, 60) if KK.canonical_contraction(p, 4) is None] == \
        [5, 13, 17, 29, 37, 53]
    assert KK.canonical_contraction(11, 5) is None


def test_kappa2_contraction_is_the_k2_one():
    for p in [q for q in range(3, 300) if KK.is_prime(q)]:
        m = K2.least_nonresidue(p)
        assert KK.coset_generator(p, 2) == m
        assert KK.canonical_contraction(p, 2) == ((1, 0), (0, m-1))


def test_bezout_and_refusals():
    for p in (7, 13, 19, 31, 37, 43):
        for d in range(3, 60, 3):
            if math.gcd(d, p-1) == 3:
                u = KK.bezout_exponent_kappa(p, d)
                tab = KK.least_root_table(p, 3)
                for x, r in tab.items():
                    assert pow(r, 3, p) == x and all(pow(t, 3, p) != x for t in range(r))
                    assert pow(pow(r, u, p), d, p) == x
    for p, d in ((7, 1), (7, 5), (13, 6), (5, 4), (11, 5)):      # kappa = 1, or p in E_2(kappa)
        with pytest.raises(ValueError):
            KK.CoherentSDEKappa(p, 1, d)


# ---------------------------------------------------------------- references

@pytest.mark.parametrize("p,a,d,n", [(7, 1, 3, None), (13, 1, 3, None), (13, 1, 9, None),
                                     (7, 2, 3, 400), (13, 2, 3, 300), (7, 3, 3, 200),
                                     (41, 2, 4, 150), (211, 1, 5, 150)])
def test_definition_equals_batch_reference(p, a, d, n):
    A = KK.all_inputs(p, a) if n is None else KK.structured_inputs(p, a, n, seed=7*p+a)
    s, x, K = KK.canonical_witness_kappa_batch(p, A, d)
    for i in range(A.shape[0]):
        cols = [tuple(int(v) for v in A[i, :, c]) for c in range(KK.columns(a))]
        r = KK.canonical_witness_kappa(p, cols, d)
        assert r["s"] == [int(v) for v in s[i]] and r["x"] == [int(v) for v in x[i]] and r["K"] == K[i]
        assert KK.check_witness(p, cols, d, r["s"])
        assert r["x"][r["istar"]] == 1                   # Theorem 2
        assert not r["y_prime_nonzero"]                  # Lemma 4'


def test_lemma4prime_on_references():
    """Lemma 4': stop test <=> every nonzero delta_i in P <=> v_{k+1} = 0, and y' = e_K."""
    for p, a, d, n in ((7, 1, 3, None), (13, 1, 3, None), (7, 2, 3, 3000), (7, 3, 3, 800),
                       (41, 2, 4, 500), (211, 2, 5, 200)):
        A = KK.all_inputs(p, a) if n is None else KK.structured_inputs(p, a, n, seed=11)
        C = KK.kappa_constants(p, d)
        cs = KK.Cos(p, C["kappa"], C["g"])
        offs = KK.block_offsets(a)
        for i in range(A.shape[0]):
            cols = [tuple(int(v) for v in A[i, :, c]) for c in range(KK.columns(a))]
            V = []
            for k in range(a+1):
                blk = [list(cols[offs[k]+t]) for t in range(a+1-k)]
                _, y = KK.first_dependency(p, V+blk)
                dl = y[k:]
                v = [sum(C["beta"][cs(t)]*t*bl[r] for t, bl in zip(dl, blk) if t) % p for r in range(a)]
                fd = KK.first_dependency(p, V+[v])
                allp = all(t == 0 or cs(t) == 0 for t in dl)
                assert (fd is not None) == allp == (not any(v))
                if fd is not None:
                    assert not any(fd[1][:k])
                    break
                V.append(v)


def test_kappa2_weights_match_k2():
    """At kappa = 2 the general definition gives the kappa = 2 module's weights x."""
    for p, a, n in ((5, 2, 400), (7, 2, 300), (13, 3, 150), (3, 2, None)):
        A = KK.all_inputs(p, a) if n is None else KK.structured_inputs(p, a, n, seed=3)
        _, x, K = KK.canonical_witness_kappa_batch(p, A, 2)
        _, x2, K2_ = K2.canonical_witness_k2_batch(p, A, 2)
        assert np.array_equal(x, x2) and np.array_equal(K, K2_)


def test_row_space_invariance():
    """Lemma 5: the witness of g.lambda equals that of lambda (g in GL_a)."""
    rng = np.random.default_rng(4)
    for p, a in ((7, 2), (13, 2), (7, 3)):
        A = KK.structured_inputs(p, a, 300, seed=p)
        s, _, _ = KK.canonical_witness_kappa_batch(p, A, 3)
        G = []
        while len(G) < 300:
            g = rng.integers(0, p, size=(a, a))
            if round(np.linalg.det(g)) % p:
                G.append(g)
        GA = np.einsum("nij,njc->nic", np.array(G), A) % p
        s2, _, _ = KK.canonical_witness_kappa_batch(p, GA, 3)
        assert np.array_equal(s, s2)


def test_rref_representatives_count():
    for p, a, n in ((3, 2, 4), (5, 1, 3), (7, 2, 3)):
        R = KK.rref_representatives(p, a, n)
        assert len(R) == KK.rref_count(p, a, n)
        assert sum(len(c) for c in KK.rref_iter_chunks(p, a, n, 50)) == len(R)


# ---------------------------------------------------------------- circuits: exhaustive

@pytest.mark.parametrize("p,d,stop", [(7, 3, "power"), (13, 3, "power"), (19, 3, "power"),
                                      (37, 3, "power"), (13, 9, "power"), (31, 9, "power"),
                                      (7, 3, "general"), (13, 3, "general"), (19, 3, "general"),
                                      (5, 2, "power"), (13, 2, "power")])
def test_exhaustive_a1(p, d, stop):
    c = KK.CoherentSDEKappa(p, 1, d, stop=stop)
    assert _all_ok(KK.check_circuit(c, KK.all_inputs(p, 1)))


@pytest.mark.parametrize("p,a,d,stop", [(7, 2, 3, "power"), (13, 2, 3, "power"), (19, 2, 3, "power"),
                                        (7, 3, 3, "power"), (7, 2, 3, "general"), (13, 2, 3, "general"),
                                        (41, 2, 4, "power"), (7, 2, 2, "power")])
def test_sampled(p, a, d, stop):
    c = KK.CoherentSDEKappa(p, a, d, stop=stop)
    r = KK.check_circuit(c, KK.structured_inputs(p, a, 384, seed=p*10+a))
    assert _all_ok(r)


@pytest.mark.parametrize("p,a,n", [(7, 2, 120), (13, 2, 80), (7, 3, 40)])
def test_circuit_equals_definition_reference(p, a, n):
    c = KK.CoherentSDEKappa(p, a, 3)
    A = KK.structured_inputs(p, a, n, seed=p+31*a)
    sim = KK.BitSim(c.nw, n)
    for col in range(c.M):
        for r in range(a):
            sim.load(c.L[col][r], A[:, r, col])
    sim.run(c.flatten())
    s = np.stack([sim.read(c.S[col]) for col in range(c.M)], axis=1)
    for i in range(n):
        cols = [tuple(int(v) for v in A[i, :, col]) for col in range(c.M)]
        assert [int(v) for v in s[i]] == KK.canonical_witness_kappa(p, cols, 3)["s"]


def test_rref_representatives_a2_p7_partial():
    """The circuit on the first 4096 row-space representatives at (7, 2) (all in slow)."""
    c = KK.CoherentSDEKappa(7, 2, 3)
    A = next(KK.rref_iter_chunks(7, 2, c.M, 4096))
    assert _all_ok(KK.check_circuit(c, A))


@pytest.mark.parametrize("p,d", [(7, 3), (13, 3), (19, 3), (37, 3), (109, 3), (163, 3), (13, 9),
                                 (31, 9), (41, 4), (13, 6), (37, 6), (211, 5), (31, 10)])
def test_root_circuit_exhaustive(p, d):
    r = KK.root_check(p, d)
    assert r["root_ok"] and r["x_restored"] and r["workspace_clean"]


# ---------------------------------------------------------------- structure and counts

def test_inputs_never_targeted_and_copy_stage_footprint():
    for p, a, d in ((7, 2, 3), (19, 1, 3), (13, 1, 9)):
        c = KK.CoherentSDEKappa(p, a, d)
        inputs = {w for col in c.L for r in col for w in r}
        outs = {w for r in c.S for w in r}
        xs = {w for r in c.X for w in r}
        pool = {w for r in c.free for w in r} | set(c.free_bits) | set(c.anc.all) | set(c.tmp)
        for it in c.prog:
            if isinstance(it, Macro):
                assert not set(it.args[0]) & inputs
            else:
                assert it[1][-1] not in inputs
        flips = {}
        for it in c.C:
            if isinstance(it, Macro):
                t = set(it.args[0])
                assert t <= outs or t <= pool
            elif it[0] in ("cx", "ccx"):
                assert it[1][-1] not in xs and it[1][-1] not in inputs
            else:
                flips[it[1][0]] = flips.get(it[1][0], 0)+1
        assert all(v % 2 == 0 for w, v in flips.items() if w in xs)


def test_emitted_counts_equal_program_counts():
    for p, a, d, stop in ((7, 1, 3, "power"), (7, 2, 3, "general"), (13, 1, 9, "power"),
                          (41, 1, 4, "power")):
        c = KK.CoherentSDEKappa(p, a, d, stop=stop)
        g = c.flatten()
        cnt = c.counts()
        assert len(g) == cnt["gates"]["total"]
        assert sum(1 for x in g if x[0] == "ccx") == cnt["gates"]["ccx"]


@pytest.mark.parametrize("p,a,d,stop", [(7, 1, 3, "power"), (7, 2, 3, "power"), (13, 3, 3, "power"),
                                        (19, 2, 3, "power"), (109, 1, 3, "power"), (163, 2, 3, "power"),
                                        (31, 2, 9, "power"), (7, 8, 3, "power"), (2**31-1, 2, 3, "power"),
                                        (2**61-1, 1, 3, "power"), (41, 2, 4, "power"), (3, 2, 2, "power"),
                                        (7, 2, 3, "general"), (37, 3, 3, "general"), (41, 2, 4, "general")])
def test_closed_forms(p, a, d, stop):
    r = KK.count_row(p, a, d, stop)
    assert r["toffoli_matches"] and r["macros_match"] and r["qubits_match"]
    m = KK.closed_form_macros(p, a, d, stop=stop)
    assert KK.closed_form_products_poly(a, m["I_p"], m["L_h"], m["T_root"], KK._ell(m["u"]),
                                        stop) == r["add_product"]


# ---------------------------------------------------------------- mutations

def _mutant_fails(p, a, d=3, mutate=None, drop=None, stop="power", n=2048):
    c = KK.CoherentSDEKappa(p, a, d, mutate=mutate, stop=stop)
    if drop is not None:
        F = Prog(c.F)
        del F[drop(F)]
        c.prog = Prog(F+c.C+c.F.inverse())
    A = KK.all_inputs(p, a) if p**(a*c.M) <= 600000 else KK.structured_inputs(p, a, n, seed=5)
    return not _all_ok(KK.check_circuit(c, A))


@pytest.mark.parametrize("p,a,mut", [(7, 2, {"alpha": (1, 0, 4)}), (13, 2, {"alpha": (1, 1, 10)}),
                                     (7, 1, {"beta": (0, 3, 6)}), (7, 1, {"beta": (0, 2, 5)}),
                                     (7, 2, {"tau1": 1}), (7, 1, {"out": 2}),
                                     (13, 1, {"omega_min": True}), (19, 1, {"omega_min": True})])
def test_constant_mutations_detected(p, a, mut):
    assert _mutant_fails(p, a, mutate=mut)


def test_lemma4prime_equivalent_mutant_general_mode():
    """In the general-stop circuit the y' term is 0 on every input (Lemma 4'): flipping its sign
    is undetectable, exhaustively at (7, 1) and (13, 1) and on samples at (7, 2)."""
    for p, a in ((7, 1), (13, 1), (7, 2)):
        assert not _mutant_fails(p, a, mutate={"tau2": 1}, stop="general")


def _nth(kind, frac):
    def pick(F):
        idx = [i for i, it in enumerate(F) if not isinstance(it, Macro) and it[0] == kind]
        return idx[int(frac*(len(idx)-1))]
    return pick


@pytest.mark.parametrize("kind,frac", [("ccx", 0.0), ("ccx", 0.5), ("ccx", 0.97), ("cx", 0.99),
                                       ("x", 0.0)])
def test_gate_drop_mutations_detected(kind, frac):
    assert _mutant_fails(7, 1, drop=_nth(kind, frac))


def test_macro_drop_mutation_detected():
    def pick(F):
        return [i for i, it in enumerate(F) if isinstance(it, Macro)][-1]
    assert _mutant_fails(7, 1, drop=pick)


# ---------------------------------------------------------------- slow

@slow
@pytest.mark.parametrize("p", [31, 43, 61, 67, 73, 79, 97, 103, 109])
def test_slow_exhaustive_a1(p):
    assert _all_ok(KK.exhaustive_check(p, 1, 3))


@slow
@pytest.mark.parametrize("p,d", [(41, 4), (61, 4), (37, 15), (7, 9)])
def test_slow_exhaustive_a1_other(p, d):
    assert _all_ok(KK.exhaustive_check(p, 1, d))


@slow
def test_slow_rref_all_row_spaces_p7_a2():
    r = KK.rref_check(7, 2, 3, log=lambda *a, **k: None)
    assert r["row_spaces"] == r["expected"] and _all_ok(r)


@slow
@pytest.mark.parametrize("p,a,d", [(7, 2, 3), (13, 2, 3), (19, 2, 3), (37, 2, 3), (7, 3, 3),
                                   (13, 3, 3), (7, 4, 3), (41, 2, 4), (211, 2, 5)])
def test_slow_sampled(p, a, d):
    assert _all_ok(KK.sampled_check(p, a, d, n=4096, seed=p*100+a*10+d))


@slow
@pytest.mark.parametrize("p,d", [(487, 3), (1459, 3), (97, 4), (1009, 6)])
def test_slow_root_circuit(p, d):
    r = KK.root_check(p, d)
    assert r["root_ok"] and r["workspace_clean"]
