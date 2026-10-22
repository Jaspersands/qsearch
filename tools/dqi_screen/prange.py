"""Best-of-N Prange completion over a prime field: the finite-length classical baseline for DQI.

    from tools.dqi_screen.prange import prange_restarts
    prange_restarts(B, accepted, q, restarts=100, seed=0)["best"]

A max-LINSAT instance is an m x n matrix B over F_q and, for each row i, the accepted set
accepted[i]. One restart permutes the rows, takes the first r = rank(B) linearly independent
ones, draws a target from each of their accepted sets, solves for x and scores the fraction of
rows whose (Bx)_i lands in its accepted set. The rows chosen are always satisfied, so the
expected score is the screen's Q_Pr = rho + (1 - rho) alpha with alpha = r/m (n/m at full
rank); the best of N restarts is the finite-length number DQI has to beat (rule "restarts").
A rank-deficient B (duplicated columns, the incidence matrix of a graph) runs on its image:
the r rows chosen span the row space, so they fix Bx.

Entries of B and of the accepted sets must be integers (a float or a string raises; it is
never truncated). Accepted sets are read mod q. A step-1 range is an arc of residues (range(-1, 2) is
{q-1, 0, 1}) and is never materialised, so large arcs are cheap when q = 2^61 - 1; it may not
be longer than q. Any other collection is reduced to a set of residues.

Arithmetic is on Python ints, so q up to 2^61 - 1 does not overflow int64.
"""

from __future__ import annotations

import numbers
from collections.abc import Collection, Sequence

import numpy as np


class _Arc:
    """A step-1 range read mod q: the residues start, start + 1, ..., start + len - 1 (mod q).

    It may start below 0 or run past q - 1, and is indexed in increasing residue order, like
    the sorted pool of the equal set, so a range and its set draw the same targets."""

    def __init__(self, r: range, q: int) -> None:
        if len(r) > q:
            raise ValueError(f"accepted range {r} is longer than q = {q}")
        self.start, self.size, self.q = r.start % q, len(r), q
        self.wrapped = max(0, self.start + self.size - q)  # residues 0 .. wrapped - 1 come first

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, k: int) -> int:
        if not 0 <= k < self.size:
            raise IndexError(k)
        return k if k < self.wrapped else self.start + k - self.wrapped

    def __contains__(self, x: object) -> bool:
        return isinstance(x, int) and (x - self.start) % self.q < self.size


_MATERIALIZE_LIMIT = 10**6


def _integer(value: object, where: str) -> int:
    """value as an int; ValueError for anything not integral (a float or a str is never truncated)."""
    if not isinstance(value, numbers.Integral):
        raise ValueError(f"{where} must hold integers, got {value!r}")
    return int(value)


def _isprime(q: int) -> bool:
    import sympy  # deterministic below 2^64

    return bool(sympy.isprime(q))


def _independent_rows(rows: list[list[int]], order: Sequence[int], n: int, q: int) -> list[int]:
    """The first n rows in `order` that are linearly independent mod q, or all independent ones
    found when there are fewer (rank below n)."""
    basis: list[tuple[int, list[int]]] = []  # (pivot column, row reduced and scaled to 1 there)
    chosen: list[int] = []
    for i in order:
        v = rows[i]
        for pivot, row in basis:
            if v[pivot]:
                f = v[pivot]
                v = [(a - f * b) % q for a, b in zip(v, row)]
        lead = next((j for j, a in enumerate(v) if a), None)
        if lead is None:
            continue
        inverse = pow(v[lead], -1, q)
        basis.append((lead, [a * inverse % q for a in v]))
        chosen.append(int(i))
        if len(chosen) == n:
            return chosen
    return chosen


def _solve(rows: list[list[int]], rhs: list[int], q: int, n: int) -> list[int]:
    """Gauss-Jordan solution mod q of an r x n system of full row rank r, free variables 0."""
    aug = [row + [v] for row, v in zip(rows, rhs)]
    pivots: list[int] = []
    for col in range(n):
        top = len(pivots)
        if top == len(aug):
            break
        pivot = next((r for r in range(top, len(aug)) if aug[r][col]), None)
        if pivot is None:
            continue
        aug[top], aug[pivot] = aug[pivot], aug[top]
        inverse = pow(aug[top][col], -1, q)
        aug[top] = [a * inverse % q for a in aug[top]]
        for r in range(len(aug)):
            if r != top and aug[r][col]:
                f = aug[r][col]
                aug[r] = [(a - f * b) % q for a, b in zip(aug[r], aug[top])]
        pivots.append(col)
    x = [0] * n
    for r, col in enumerate(pivots):
        x[col] = aug[r][n]
    return x


def prange_restarts(
    B: np.ndarray, accepted: Sequence[Collection[int]], q: int, restarts: int = 1, seed: int | None = None
) -> dict:
    """Best-of-`restarts` Prange completion; returns {"best", "scores", "restarts", "m", "n", "q", "rank"}.

    One np.random.default_rng(seed) drives every restart in turn, so the first k scores of a
    longer run equal a k-restart run with the same seed. Each restart solves on rank(B)
    independent rows (fewer than n when B is rank deficient). ValueError when q is not prime
    or B has no rows or no columns."""
    q = int(q)
    if q < 2 or not _isprime(q):
        raise ValueError(f"q must be prime, got {q}")
    if restarts < 1:
        raise ValueError(f"restarts must be at least 1, got {restarts}")
    matrix = np.asarray(B)
    if matrix.ndim != 2 or matrix.dtype.kind not in "iuO":
        raise ValueError("B must be a two-dimensional integer array")
    m, n = matrix.shape
    if m < 1 or n < 1:
        raise ValueError(f"B must have at least one row and one column, got shape {matrix.shape}")
    if len(accepted) != m:
        raise ValueError(f"need one accepted set per row: {len(accepted)} sets for {m} rows")
    rows = [[_integer(a, "B") % q for a in row] for row in matrix.tolist()]
    pools: list[Sequence[int]] = []  # indexable, in a fixed order, for drawing targets
    members: list[Collection[int]] = []  # fast membership, for scoring
    for coll in accepted:
        if isinstance(coll, (str, bytes, bytearray)):
            raise ValueError(f"accepted sets must be collections of integers, got {coll!r}")
        if isinstance(coll, range) and coll.step == 1:
            arc = _Arc(coll, q)
            pools.append(arc)
            members.append(arc)
        else:
            if isinstance(coll, range) and len(coll) > _MATERIALIZE_LIMIT:
                raise ValueError(f"accepted range {coll} has step {coll.step}: give a step-1 range or a set")
            if len(coll) > _MATERIALIZE_LIMIT:
                raise ValueError(f"accepted collection is too large to materialize (limit {_MATERIALIZE_LIMIT}); "
                                 "use a step-1 range for a contiguous modular arc")
            values = sorted({_integer(v, "accepted sets") % q for v in coll})
            pools.append(values)
            members.append(set(values))
        if not len(pools[-1]):
            raise ValueError("every accepted set must be non-empty")

    rank = len(_independent_rows(rows, range(m), n, q))
    rng = np.random.default_rng(seed)
    scores: list[float] = []
    for _ in range(restarts):
        chosen = _independent_rows(rows, rng.permutation(m), rank, q)  # always `rank` rows: they span the row space
        targets = [int(pools[i][int(rng.integers(len(pools[i])))]) % q for i in chosen]
        x = _solve([rows[i] for i in chosen], targets, q, n)
        hits = sum(sum(a * b for a, b in zip(row, x)) % q in members[i] for i, row in enumerate(rows))
        scores.append(hits / m)
    return {"best": max(scores), "scores": scores, "restarts": restarts, "m": m, "n": n, "q": q, "rank": rank}
