"""Exact witness checks for the deterministic Ivanyos-Santha SDE solver."""
from itertools import product
from math import gcd
import random

import pytest

from theorems.rees_is_sde_solver import (
    Classifier, PiParts, _Restart, _anchor_witness, _prime_divisors, collision_arity, columns_required, is_arity,
    is_sde_solve, reduced_degree, selective_root, theorem11, verify,
    zero_sum_of_powers,
)

SMALL = (3, 5, 7, 13, 17, 41, 73, 97, 113, 193, 257)
P30 = dict(k2=536870951, k2b=536871017, k3=536870923, k4=536871001, k4b=536871029)


def _primes(limit):
    return [n for n in range(3, limit) if all(n % f for f in range(2, int(n**0.5)+1))]


def _random_columns(rng, p, g, M, nonzero=True):
    return [tuple(rng.randrange(1 if nonzero else 0, p) for _ in range(g)) for _ in range(M)]


def _repeated_basis(g, M):
    return [tuple(int(j == i % g) for j in range(g)) for i in range(M)]


def _omega(n):
    count, f = 0, 2
    while n > 1:
        while n % f == 0:
            n //= f
            count += 1
        f += 1
    return count


def _exists_nonzero(p, kappa, columns):
    """Exhaustive Chevalley-Warning check over the values s_i^kappa."""
    values = sorted({pow(x, kappa, p) for x in range(p)})
    g = len(columns[0])
    for choice in product(values, repeat=len(columns)):
        if any(choice) and not any(sum(c*col[r] for c, col in zip(choice, columns)) % p
                                   for r in range(g)):
            return True
    return False


def _check(p, d, columns, **options):
    w = is_sde_solve(p, d, columns, **options)
    assert verify(p, d, columns, w.s)
    assert any(w.s) and len(w.s) == len(columns)
    assert w.columns_required <= len(columns)
    if w.reduced_degree > 1 and w.rank:
        assert w.columns_required <= is_arity(w.reduced_degree, w.rank) <= is_arity(d, w.rank)
        assert w.restarts <= _omega(PiParts(p, w.reduced_degree).n_pi)
    return w


def test_arity_formulas_and_chevalley_warning_counts():
    assert [is_arity(2, a) for a in range(4)] == [4*(a+1)**4 for a in range(4)]
    assert [is_arity(3, a) for a in range(4)] == [729*(a+1)**6 for a in range(4)]
    assert [is_arity(4, a) for a in range(3)] == [4096**3*(a+1)**12 for a in range(3)]
    assert is_arity(1, 5) == 6
    for d in range(1, 10):
        for a in range(13):
            G = d**(d*(d-1)//2)*(a+1)**d
            assert collision_arity(d, a) == G
            assert is_arity(d, a) == G**(d).bit_length()
            # Chevalley-Warning: more than d*a variables force a nonzero zero.
            assert is_arity(d, a) > d*a and G > d*a
    for p in SMALL+tuple(P30.values()):
        for d in range(1, 10):
            kappa, _ = reduced_degree(p, d)
            for a in range(1, 4):
                need = columns_required(p, d, a)
                assert kappa*a < need <= is_arity(kappa, a) <= is_arity(d, a)


@pytest.mark.parametrize("p", SMALL+tuple(P30.values()))
def test_gcd_reduction_bezout_exponent(p):
    for d in range(1, 13):
        kappa, t = reduced_degree(p, d)
        assert kappa == gcd(d, p-1) and t > 0 and (t*d-kappa) % (p-1) == 0
        for x in (range(1, p) if p < 300 else (2, 3, p-1, 12345)):
            assert pow(pow(x, t, p), d, p) == pow(x, kappa, p)


@pytest.mark.parametrize("p", (5, 7, 13, 17, 41, 73, 97, 193, 257))
def test_classifier_restarts_and_writes_every_element(p):
    for d in (2, 3, 4, 6, 8):
        if (p-1) % d:
            continue
        parts = PiParts(p, d)
        assert parts.n_pi*parts.n_rest == p-1 and gcd(d, parts.n_rest) == 1
        natural = list(range(1, p))
        # Increasing pi-part order forces one restart per prime factor of |H_pi|.
        slow = sorted(natural, key=lambda x: parts.order(parts.split(x)[0]))
        for order, exact in ((natural, False), (slow, True)):
            eta, restarts = 1, 0
            while True:
                classifier = Classifier(parts, eta)
                try:
                    for alpha in order:
                        r, beta = classifier.classify(alpha)
                        assert 0 <= r < d and alpha == classifier.zeta(r)*pow(beta, d, p) % p
                    break
                except _Restart as restart:
                    eta = parts.join(eta, restart.element)
                    restarts += 1
            assert parts.order(eta) == parts.n_pi
            assert restarts <= _omega(parts.n_pi)
            if exact:
                assert restarts == _omega(parts.n_pi)


@pytest.mark.parametrize("p", _primes(400))
def test_van_de_woestijne_zero_sums(p):
    for kappa in range(2, 13):
        if (p-1) % kappa:
            continue
        for shorten in (False, True):
            z = zero_sum_of_powers(p, kappa, shorten=shorten)
            assert z == zero_sum_of_powers(p, kappa, shorten=shorten)
            assert 2 <= len(z) <= kappa+1 and all(z)
            assert sum(pow(x, kappa, p) for x in z) % p == 0
            if pow(p-1, (p-1)//kappa, p) != 1:
                assert len(z) >= 3
        if kappa == p-1:
            assert len(zero_sum_of_powers(p, kappa)) == p


def test_selective_root_extraction():
    rng = random.Random(11)
    for p in (13, 17, 97, 65537, P30["k4"], P30["k3"]):
        for d in (2, 3, 4, 8):
            if (p-1) % d:
                continue
            for _ in range(20):
                values = [rng.randrange(1, p) for _ in range(d+1)]
                i, j, beta = selective_root(p, d, values)
                assert i < j and values[i] == pow(beta, d, p)*values[j] % p
                hit = selective_root(p, d, values[:2])
                assert hit is None or values[hit[0]] == pow(hit[2], d, p)*values[hit[1]] % p
    # Below d+1 values a collision is certified only inside <eta>: 1/4 is a
    # square in F_13 but not in <eta> = {1, -1}, so no pair is returned.
    assert selective_root(13, 2, [1, 4]) is None
    assert selective_root(13, 2, [5, 5]) == (0, 1, 1)
    with pytest.raises(ValueError):
        selective_root(13, 2, [0, 1, 2])


@pytest.mark.parametrize("p,d,m", [(5, 2, 2), (13, 2, 3), (7, 3, 2), (13, 3, 1),
                                   (P30["k3"], 3, 2), (13, 4, 1), (P30["k4"], 4, 1)])
def test_theorem11_colliding_representations(p, d, m):
    rng = random.Random(p+d+m)
    parts = PiParts(p, d)
    vectors = list(enumerate(_random_columns(rng, p, m, collision_arity(d, m))))
    for spread in (False, True):
        eta = 1
        while True:
            try:
                side_i, side_j, w = theorem11(Classifier(parts, eta), vectors,
                                              dict(kernels=0, spread=spread))
                break
            except _Restart as restart:
                eta = parts.join(eta, restart.element)
        assert side_i and not {k for k, _ in side_i} & {k for k, _ in side_j}
        for side in (side_i, side_j):
            total = [0]*m
            for k, gamma in side:
                assert gamma % p
                total = [(x+pow(gamma, d, p)*y) % p for x, y in zip(total, vectors[k][1])]
            assert tuple(total) == w


CASES = [
    # (p, d, g): kappa = gcd(d, p-1); full arity B_kappa(g) supplied when feasible
    (3, 2, 2), (5, 2, 3), (7, 2, 3), (13, 2, 3), (41, 2, 2), (5, 6, 3),
    (7, 3, 1), (13, 3, 1), (7, 3, 2), (7, 9, 1), (13, 9, 1),
    (P30["k2"], 2, 3), (P30["k2b"], 2, 3), (P30["k2"], 4, 2), (P30["k2"], 6, 2),
    (P30["k2"], 8, 2), (P30["k3"], 3, 1), (P30["k3"], 9, 2), (P30["k2b"], 3, 5),
]


@pytest.mark.parametrize("p,d,g", CASES)
def test_random_columns_at_is_arity(p, d, g):
    rng = random.Random(1000*p+d+g)
    kappa, _ = reduced_degree(p, d)
    M = is_arity(kappa, g)
    assert M >= columns_required(p, d, g)
    columns = _random_columns(rng, p, g, M)
    for spread in (False, True):
        w = _check(p, d, columns, spread=spread)
        assert w.reduced_degree == kappa and w.rank == g
    assert w == is_sde_solve(p, d, columns, spread=True)


@pytest.mark.parametrize("p,d,g", [(3, 2, 2), (5, 2, 3), (7, 2, 2), (7, 3, 1), (13, 3, 1),
                                   (P30["k2b"], 2, 3), (P30["k3"], 9, 1)])
def test_adversarial_repeated_basis_and_rank_deficient_columns(p, d, g):
    kappa, _ = reduced_degree(p, d)
    M = is_arity(kappa, g)
    for spread in (False, True):
        w = _check(p, d, _repeated_basis(g, M), spread=spread)
        assert w.rank == g
        same = [tuple(range(1, g+1))]*M
        assert _check(p, d, same, spread=spread).rank == 1
        rng = random.Random(p*g)
        basis = _random_columns(rng, p, g+3, g)
        mixed = [tuple(sum(c*b[r] for c, b in zip(row, basis)) % p for r in range(g+3))
                 for row in _random_columns(rng, p, g, M)]
        assert _check(p, d, mixed, spread=spread).rank == g


@pytest.mark.parametrize("p", (17, 41, 97, P30["k4"]))
def test_quartic_end_to_end_when_deterministic_zero_sum_has_two_terms(p):
    assert reduced_degree(p, 4)[0] == 4 and len(zero_sum_of_powers(p, 4)) == 2
    M = columns_required(p, 4, 1)
    assert M == collision_arity(4, 1) == 65536 < is_arity(4, 1)
    columns = _random_columns(random.Random(p), p, 1, M)
    w = _check(p, 4, columns, spread=True)
    assert w.levels == 1 and w.theorem11_calls == 1


def test_zero_sum_family_and_chevalley_warning_sharpness():
    # main.tex thm:power-sde (iii): p=5, d=4, a=2, e1 x4, e2 x4 has no solution.
    family = _repeated_basis(2, 8)
    assert not _exists_nonzero(5, 4, family)
    assert _exists_nonzero(5, 4, family+[(1, 1)])
    for p, kappa, g in [(3, 2, 3), (7, 6, 1), (5, 4, 1), (13, 12, 1)]:
        assert kappa == p-1
        assert not _exists_nonzero(p, kappa, _repeated_basis(g, kappa*g))
    # Chevalley-Warning at kappa*a+1 columns, exhaustively, on random tuples.
    rng = random.Random(7)
    for p, kappa, g in [(5, 2, 2), (5, 4, 2), (7, 3, 1), (7, 2, 2), (13, 3, 1), (13, 4, 1)]:
        for _ in range(5):
            assert _exists_nonzero(p, kappa, _random_columns(rng, p, g, kappa*g+1, nonzero=False))
    # The deterministic run needs far more: here G(4,2)^3 columns, and it refuses below.
    need = columns_required(5, 4, 2)
    assert len(zero_sum_of_powers(5, 4)) == 5 and need == collision_arity(4, 2)**3
    with pytest.raises(ValueError):
        is_sde_solve(5, 4, family+[(1, 1)])
    # p=3, d=2 is the same kappa=p-1 subset-sum regime and runs at full arity.
    for g in (1, 2, 3):
        _check(3, 2, _repeated_basis(g, is_arity(2, g)), spread=True)


def test_shortcuts_refusals_and_linear_case():
    w = is_sde_solve(13, 2, [(1, 2), (0, 0), (3, 4)])
    assert w.s == (0, 1, 0) and w.early_zero and w.rank == 2
    assert is_sde_solve(13, 2, [(0, 0)]*3).s == (1, 0, 0)
    for p, d in [(5, 3), (17, 3), (P30["k2"], 3)]:
        assert reduced_degree(p, d)[0] == 1
        columns = _random_columns(random.Random(d), p, 4, 5)
        assert _check(p, d, columns).columns_required == 5
        with pytest.raises(ValueError):
            is_sde_solve(p, d, columns[:4])
    with pytest.raises(ValueError):
        is_sde_solve(7, 2, _random_columns(random.Random(1), 7, 2, is_arity(2, 2)-1))
    with pytest.raises(ValueError):
        is_sde_solve(15, 2, [(1,)]*10)


@pytest.mark.parametrize("p,d,g", [(3, 2, 2), (7, 2, 2), (41, 2, 2), (P30["k2"], 2, 3),
                                   (P30["k2b"], 6, 2), (7, 3, 2), (P30["k3"], 3, 1),
                                   (P30["k4"], 4, 1)])
def test_full_accumulation_and_fact2_without_early_exits(p, d, g):
    # With early exits, random runs at L=2 always stop at some zero collision.
    kappa, _ = reduced_degree(p, d)
    M = columns_required(p, d, g)
    columns = _random_columns(random.Random(3*p+g), p, g, M)
    for spread in (False, True):
        w = _check(p, d, columns, spread=spread, early_exit=False)
        t = len(w.zero_sum)
        assert not w.early_zero and 2**w.levels >= t >= 2
        assert w.theorem11_calls == sum(collision_arity(kappa, g)**j for j in range(w.levels))
        if kappa == 2 and pow(p-1, (p-1)//2, p) != 1:
            assert t == 3 and w.levels == 2


def test_unshortened_zero_sum_and_degenerate_degrees():
    rng = random.Random(73)
    for p, d, g in [(73, 2, 1), (73, 2, 2), (13, 2, 2), (P30["k2b"], 2, 2), (7, 3, 1)]:
        for shorten in (False, True):
            M = columns_required(p, d, g, shorten=shorten)
            columns = _random_columns(rng, p, g, M)
            w = _check(p, d, columns, shorten=shorten, spread=True)
            assert w.columns_required == M
            assert len(w.zero_sum) == len(zero_sum_of_powers(p, w.reduced_degree, shorten=shorten))
    assert columns_required(73, 2, 1) == 8 < columns_required(73, 2, 1, shorten=False) == 64
    # d = p, d = c(p-1) and d > p-1, through the gcd reduction
    for p, d, g in [(3, 3, 2), (3, 4, 2), (3, 100, 2), (7, 7, 2), (7, 14, 1), (13, 39, 1), (5, 8, 1)]:
        kappa, _ = reduced_degree(p, d)
        M = columns_required(p, d, g)
        if M > 10**5:
            continue
        columns = _random_columns(rng, p, g, M)
        assert _check(p, d, columns).reduced_degree == kappa
        assert is_sde_solve(p, d, columns) == is_sde_solve(p, d, columns)


# ---- collapse=True: the restart-collapsing variant (2026-11-05-rees-is-restarts.md) ----

def _order_n_element(p, n):
    for x in range(2, p):
        y = pow(x, (p-1)//n, p)
        if all(pow(y, n//q, p) != 1 for q in _prime_divisors(n)):
            return y
    raise ValueError


def _check_collapse(p, d, columns, **options):
    w = _check(p, d, columns, collapse=True, **options)
    assert w == is_sde_solve(p, d, columns, collapse=True, **options)
    assert not is_sde_solve(p, d, columns, **options).collapsed
    kappa = w.reduced_degree
    if kappa > 1 and w.rank and len(_prime_divisors(kappa)) == 1:
        assert w.restarts <= _omega(kappa)-1          # Lemma 1(ii): at most Omega(kappa) runs
    if w.collapsed:
        assert all(i <= w.rank for i, x in enumerate(w.s) if x)
    return w


@pytest.mark.parametrize("p,d,g", CASES)
def test_collapse_variant_on_random_columns(p, d, g):
    rng = random.Random(7*p+d+g)
    columns = _random_columns(rng, p, g, columns_required(p, d, g))
    for spread in (False, True):
        for early_exit in (True, False):
            _check_collapse(p, d, columns, spread=spread, early_exit=early_exit)


def test_collapse_variant_on_adversarial_anchors():
    rng = random.Random(5)
    collapsed = 0
    for p in (13, 17, 41, 97, 257, 65537):          # kappa = 2, anchor (-1, 1), H_1 = {+-1}
        for g in (1, 2):
            head = [(1,), (1,)] if g == 1 else [(1, 0), (1, 0), (0, 1)]
            columns = head+_random_columns(rng, p, g, columns_required(p, 2, g)-len(head))
            w = _check_collapse(p, 2, columns, spread=True)
            assert w.restarts == 0
            collapsed += w.collapsed
    for p in (7, 11, 19, 23):                         # p = 3 mod 4: H_1 trivial, no run at all
        columns = [(1,), (p-9,)]+_random_columns(rng, p, 1, columns_required(p, 2, 1)-2)
        w = _check_collapse(p, 2, columns)
        assert w.collapsed and w.classifications == 0 and w.s[2:] == (0,)*(len(columns)-2)
    for p in (19, 37, 73, 109):                       # kappa = 3, anchor (omega, 1), |H_1| = 3
        columns = [(1,), (p-_order_n_element(p, 3),)]+_random_columns(
            rng, p, 1, columns_required(p, 3, 1)-2)
        w = _check_collapse(p, 3, columns, spread=True)
        assert w.restarts == 0
        collapsed += w.collapsed
    assert collapsed >= 10


def test_anchor_collapse_on_worst_case_enlargement_chains():
    # kappa = l^e: the anchor collapses exactly when |<eta>| >= kappa |H_1|, i.e. at trigger e.
    for p, kappa in ((65537, 2), (65537, 4), (65537, 8), (65537, 16), (1459, 3), (1459, 9)):
        parts = PiParts(p, kappa)
        ell, n = _prime_divisors(kappa)[0], parts.n_pi
        gen = next(parts.split(x)[0] for x in range(2, p)
                   if parts.order(parts.split(x)[0]) == n)
        for j1 in range(1, _omega(n)):
            h1 = ell**j1
            anchor = [(0, (pow(gen, n//h1, p), 1)), (1, (1, 1))]
            eta, h, triggers = pow(gen, n//h1, p), h1, 0
            while h < n:
                h *= ell
                eta, triggers = parts.join(eta, pow(gen, n//h, p)), triggers+1
                hit = _anchor_witness(parts, eta, anchor)
                assert (hit is not None) == (h >= kappa*h1)
                if hit is not None:
                    assert triggers == _omega(kappa)
                    break
    # kappa = 6 (two primes): a 3-part anchor never collapses under 2-part growth alone.
    p = 43777                                         # p - 1 = 2^8 * 3^2 * 19
    parts = PiParts(p, 6)
    gen = next(parts.split(x)[0] for x in range(2, p)
               if parts.order(parts.split(x)[0]) == parts.n_pi)
    g2, g3 = pow(gen, 9, p), pow(gen, 256, p)
    eta, anchor = g3, [(0, (g3, 1)), (1, (1, 1))]
    for j in range(1, 9):
        eta = parts.join(eta, pow(g2, 2**(8-j), p))
        assert _anchor_witness(parts, eta, anchor) is None


def test_collapse_variant_quartic():
    p = 17
    columns = _random_columns(random.Random(p+1), p, 1, columns_required(p, 4, 1))
    w = _check_collapse(p, 4, columns, spread=True)
    assert w.restarts <= 1
