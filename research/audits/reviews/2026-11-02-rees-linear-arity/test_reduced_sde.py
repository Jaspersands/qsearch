"""Exact checks for reduced_sde.py (run from this folder with pytest)."""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reduced_sde as R  # noqa: E402


def _two(p, k):
    Fd = R.Field(p, k)
    ab = R.two_level_contraction(Fd)
    assert ab is not None
    F = R.F_from_two_level(Fd, *ab)
    assert R.check_contraction(Fd, 2, F)
    return Fd, F


def test_two_level_triangular_and_product():
    for p, k, a in [(3, 2, 4), (7, 3, 3), (41, 4, 3), (191, 5, 2), (1009, 3, 4)]:
        Fd, F = _two(p, k)
        for scheme in ("triangular", "product"):
            r, M, res = R.run(Fd, 2, F, a, 3, scheme, R.FAMILIES, seed=11)
            assert r == [1, 1]
            assert M == ((a + 1) * (a + 2) // 2 if scheme == "triangular" else (a + 1) ** 2)
            assert all(z[3] for z in res), res


def test_sparse_variant():
    for p, k, a in [(3, 2, 6), (5, 2, 5), (7, 3, 5)]:
        Fd, F = _two(p, k)
        M = R.sparse_bound(p, a)
        rng = random.Random(3)
        for fam in R.FAMILIES:
            cols = R.family(fam, rng, p, a, M)
            x, used = R.solve_triangular_sparse(Fd, F, cols, a)
            assert used <= M
            assert R.check_witness(Fd, cols, x)[0]


def test_exceptional_primes_detected():
    for p, k in [(5, 4), (13, 4), (11, 5), (7, 6)]:
        assert R.two_level_contraction(R.Field(p, k)) is None


def test_no_universal_scheme_with_one_active_level():
    # If all H_t but one vanish, F is constant along that axis, impossible for kappa >= 2.
    Fd, F = _two(7, 3)
    Hs = R.telescoped(F, 2, 3, 7)
    ranks = [len(R.functionals(Hs[t], t, 2, 3, 7)) for t in range(2)]
    assert ranks == [1, 1]
