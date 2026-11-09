"""Shared helpers for the 2026-11-07 subquad-B pass.

Imports (read-only) the exact-arithmetic helpers and the block-refined
triangular solver of the 2026-11-05 two-relation pass.  Nothing in that
folder is modified.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TWO = os.path.join(HERE, "..", "2026-11-05-rees-sde-two-relation")
sys.path.insert(0, os.path.abspath(TWO))

from common import F, inv, rank, rref, kernel, check_witness  # noqa: E402
import brt  # noqa: E402
import brt_tests  # noqa: E402


def coords_in(basis, v, p):
    return brt.solve_basis(basis, v, p)


def backward_target(Fd, cols, rounds, basis, tau, rng, x=None):
    """Back substitution of brt.backward, started from an arbitrary residual tau
    (a vector that must lie in the realised space).  Returns (x, status).
    The returned x satisfies sum x_i cols_i = tau_initial when status == 'ok'."""
    p, k = Fd.p, Fd.k
    M, a = len(cols), len(cols[0])
    x = [0] * M if x is None else list(x)
    tau = [t % p for t in tau]
    levels = [R for R in rounds if R.kind == "level"]
    for R in reversed(levels):
        co = coords_in(basis, tau, p)
        if co is None:
            return None, "not-in-U"
        beta = [0] * len(R.blocks)
        for b, pos in zip(R.added, R.basis_pos):
            beta[b] = co[pos]
        taup = [(tau[j] - sum(beta[b] * R.W[b][j] for b in range(len(R.blocks)))) % p
                for j in range(a)]
        G = brt.good_set(Fd, beta, R.bclass, rng)
        if not G:
            return None, "good-empty"
        s = rng.choice(G)
        for b, blk in enumerate(R.blocks):
            for t in blk:
                x[R.idx[t]] = (R.delta[t] * (beta[b] + s)) % p
        tau = [(taup[j] - s * R.e[j]) % p for j in range(a)]
    if any(tau):
        return None, "residual"
    return x, "ok"


def forward_flag(Fd, cols, E, rng, split="random"):
    """Run brt.forward on cols plus a dummy top column; return (rounds, basis, status)
    where status is 'ok' when the realised space is all of F_p^a."""
    a = len(cols[0])
    rounds, basis, top, used, status = brt.forward(Fd, list(cols) + [[0] * a], E, rng, split)
    if status == "ok":
        return rounds, basis, "ok"
    return rounds, basis, status


def value(cols, x, p):
    a = len(cols[0])
    return [sum(x[i] * cols[i][j] for i in range(len(cols))) % p for j in range(a)]


class BigF:
    """Power classes for a large prime (common.F enumerates F_p and is for small p only)."""

    def __init__(self, p, kappa, rng=None):
        from common import primitive_root, is_prime
        assert (p - 1) % kappa == 0
        self.p, self.k, self.h = p, kappa, (p - 1) // kappa
        self.g = primitive_root(p)
        self.zeta = pow(self.g, self.h, p)
        self.zlog = {pow(self.zeta, j, p): j for j in range(kappa)}
        self._rng = rng or random.Random(0)

    def cls(self, y):
        y %= self.p
        assert y
        return self.zlog[pow(y, self.h, self.p)]

    def in_sq(self, y):
        y %= self.p
        return y == 0 or pow(y, self.h, self.p) == 1

    def rep(self, c):
        return pow(self.g, c % self.k, self.p)

    def randP(self):
        return pow(self._rng.randrange(1, self.p), self.k, self.p)
