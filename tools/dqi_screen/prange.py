"""Best-of-N Prange completion over a prime field: the finite-length classical baseline for DQI.

    from tools.dqi_screen.prange import prange_restarts
    prange_restarts(B, accepted, q, restarts=100, seed=0)["best"]

A max-LINSAT instance is an m x n matrix B over F_q and, for each row i, the accepted set
accepted[i]. One restart permutes the rows, takes the first n linearly independent ones,
draws a target from each of their accepted sets, solves for x and scores the fraction of
rows whose (Bx)_i lands in its accepted set. The rows chosen are always satisfied, so the
expected score is the screen's Q_Pr = rho + (1 - rho) alpha; the best of N restarts is the
finite-length number DQI has to beat (rule "restarts").

Arithmetic is on Python ints, so q up to 2^61 - 1 does not overflow int64.
"""

from __future__ import annotations

from collections.abc import Collection, Sequence

import numpy as np


def _isprime(q: int) -> bool:
    import sympy  # deterministic below 2^64

    return bool(sympy.isprime(q))


def _independent_rows(rows: list[list[int]], order: Sequence[int], n: int, q: int) -> list[int] | None:
    """The first n rows in `order` that are linearly independent mod q, or None."""
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
    return None


def _solve(rows: list[list[int]], rhs: list[int], q: int) -> list[int]:
    """Gauss-Jordan solution of an invertible n x n system mod q."""
    n = len(rows)
    aug = [row + [v] for row, v in zip(rows, rhs)]
    for col in range(n):
        pivot = next(r for r in range(col, n) if aug[r][col])
        aug[col], aug[pivot] = aug[pivot], aug[col]
        inverse = pow(aug[col][col], -1, q)
        aug[col] = [a * inverse % q for a in aug[col]]
        for r in range(n):
            if r != col and aug[r][col]:
                f = aug[r][col]
                aug[r] = [(a - f * b) % q for a, b in zip(aug[r], aug[col])]
    return [aug[r][n] for r in range(n)]


def prange_restarts(
    B: np.ndarray, accepted: Sequence[Collection[int]], q: int, restarts: int = 1, seed: int | None = None
) -> dict:
    """Best-of-`restarts` Prange completion; returns {"best", "scores", "restarts", "m", "n", "q", "singular"}.

    One np.random.default_rng(seed) drives every restart in turn, so the first k scores of a
    longer run equal a k-restart run with the same seed. A draw whose rows have rank below n
    scores 0 and counts in "singular". ValueError when q is not prime."""
    q = int(q)
    if q < 2 or not _isprime(q):
        raise ValueError(f"q must be prime, got {q}")
    if restarts < 1:
        raise ValueError(f"restarts must be at least 1, got {restarts}")
    matrix = np.asarray(B)
    if matrix.ndim != 2 or matrix.dtype.kind not in "iuO":
        raise ValueError("B must be a two-dimensional integer array")
    m, n = matrix.shape
    if len(accepted) != m:
        raise ValueError(f"need one accepted set per row: {len(accepted)} sets for {m} rows")
    rows = [[int(a) % q for a in row] for row in matrix.tolist()]
    pools: list[Sequence[int]] = []  # indexable, in a fixed order, for drawing targets
    members: list[Collection[int]] = []  # fast membership, for scoring
    for coll in accepted:
        if isinstance(coll, range):
            pools.append(coll)
            members.append(coll)
        else:
            values = sorted({int(v) % q for v in coll})
            pools.append(values)
            members.append(set(values))
        if not len(pools[-1]):
            raise ValueError("every accepted set must be non-empty")

    rng = np.random.default_rng(seed)
    scores: list[float] = []
    singular = 0
    for _ in range(restarts):
        chosen = _independent_rows(rows, rng.permutation(m), n, q)
        if chosen is None:
            scores.append(0.0)
            singular += 1
            continue
        targets = [int(pools[i][int(rng.integers(len(pools[i])))]) % q for i in chosen]
        x = _solve([rows[i] for i in chosen], targets, q)
        hits = sum(sum(a * b for a, b in zip(row, x)) % q in members[i] for i, row in enumerate(rows))
        scores.append(hits / m)
    return {"best": max(scores), "scores": scores, "restarts": restarts, "m": m, "n": n, "q": q, "singular": singular}
