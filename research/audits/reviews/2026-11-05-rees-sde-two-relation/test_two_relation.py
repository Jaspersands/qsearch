"""pytest checks for the 2026-11-05 two-relation / block-refined pass (small, fast)."""
import itertools
import random

from common import F, check_witness, kernel
import brt
import good_threshold as gt
import block_check
import bf_good


def test_scan_matches_bruteforce():
    for (k, E, p) in [(2, 3, 13), (2, 3, 17), (3, 3, 13), (3, 3, 19), (2, 4, 7), (2, 4, 11)]:
        g1 = bf_good.bf(p, k, E)
        ex, g2, _ = gt.scan_prime(p, k, E)
        assert (g1 == 0) == ex
        if not ex:
            assert g1 == g2


def test_kappa2_E3_no_exception_small():
    for p in [3, 5, 7, 11, 13, 101, 199]:
        ex, gmin, _ = gt.scan_prime(p, 2, 3)
        assert not ex and gmin >= 1


def test_weil_lower_bound_holds():
    for (k, E, p) in [(2, 3, 211), (2, 3, 257), (3, 3, 2713)]:
        ex, gmin, _ = gt.scan_prime(p, k, E)
        assert not ex and gmin >= gt.weil_gmin(k, E, p)


def test_block_theorem_exact():
    rng = random.Random(3)
    for (p, k, q, E) in [(13, 2, 2, 3), (13, 2, 3, 3), (37, 3, 2, 3), (29, 2, 3, 4)]:
        r = block_check.check(F(p, k), rng, q, E)
        if r is None:
            continue
        assert r["dim_ok"] and r["mism"] == 0


def test_arity_formula():
    for a in range(1, 30):
        assert brt.arity(a, 2) == (a + 1) * (a + 2) // 2
        if a % 2 == 0:
            assert brt.arity(a, 3) == (a + 2) ** 2 // 4
        m, r = divmod(a, 2)
    # closed form for general E
    for E in range(2, 7):
        for a in range(1, 40):
            m, r = divmod(a, E - 1)
            closed = 1 + m * (a + 1) - (E - 1) * m * (m - 1) // 2 + ((r + 1) if r else 0)
            assert brt.arity(a, E) == closed


def test_brt_random_columns():
    rng = random.Random(11)
    for (p, k, a, E) in [(1009, 2, 6, 3), (1009, 3, 6, 3), (10007, 2, 8, 4)]:
        Fd = F(p, k)
        M = brt.arity(a, E)
        for _ in range(5):
            cols = [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
            x, info = brt.solve(Fd, cols, E, rng)
            assert x is not None and check_witness(Fd, cols, x)


def test_brt_never_returns_wrong_witness_small():
    rng = random.Random(12)
    Fd = F(13, 2)
    for _ in range(30):
        cols = [[rng.randrange(13) for _ in range(2)] for _ in range(4)]
        x, info = brt.solve(Fd, cols, 3, rng, restarts=10)
        if x is not None:
            assert check_witness(Fd, cols, x)


def test_below_cw_instance_unsolvable():
    # (e_j, -g e_j) with g a non-residue: x1 = g x2 forces x1 = x2 = 0 for every odd p
    for p in (7, 11, 13, 19):
        Fd = F(p, 2)
        g = Fd.rep(1)
        cols = [[1, 0], [(-g) % p, 0], [0, 1], [0, (-g) % p]]
        assert all(not check_witness(Fd, cols, x) for x in itertools.product(Fd.Sq, repeat=4))
