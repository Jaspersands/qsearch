"""Exterior-probe secret-aware fixtures. NEVER used by the native learner."""

from itertools import combinations, product

import exterior_probe as ep

op = ep.op


def fixture_kernel(probe, hidden):
    width, p = len(probe.frame), probe.p
    annihilator = op.nullspace(hidden, width, p)
    columns = []
    for unit in op.eye(probe.width):
        g = probe.matrix(unit)
        columns.append(tuple(op.dot(a, op.add(op.mv(g, u, p), op.scale(-1, u, p), p), p)
                             for u in hidden for a in annihilator))
    return op.basis(op.nullspace(op.transpose(columns), probe.width, p), p)


def all_subspaces(n, j, p):
    for pivots in combinations(range(n), j):
        slots = tuple((i, col) for i, pivot in enumerate(pivots)
                      for col in range(pivot+1, n) if col not in pivots)
        for values in product(range(p), repeat=len(slots)):
            rows = [[int(col == pivot) for col in range(n)] for pivot in pivots]
            for (i, col), value in zip(slots, values):
                rows[i][col] = value
            yield tuple(tuple(row) for row in rows)


def all_maximal(n, p):
    for j in range(n+1):
        for x in all_subspaces(n, j, p):
            for tail in product(range(p), repeat=(n-j)*(n-j-1)//2):
                yield ep.maximal_from_cell(x, tail, n, p)


def native_fixture(n, k, p, seed):
    import random
    from flint import fmpz_mat
    frame = op.hyperbolic_frame(ep.sample_maximal(n, p, random.Random(seed)), p)
    hidden = op.image(frame, op.eye(2*n)[:k], p)
    oracle = op.OpaqueFixtureOracle(hidden, p)
    def special_oracle(g):
        if int(fmpz_mat(g).det()) % p != 1:
            raise ValueError("reference query outside SO")
        return oracle(g)
    result = ep.recover_reference(special_oracle, n, p, seed=seed+1)
    assert result["candidate"] == hidden
    assert oracle.calls == sum(r["classical_table_queries"] for r in result["records"])
    return {"n": n, "k": k, "p": p, "seed": seed,
            "native_valid": True, "oracle_domain": "SO, determinant checked on every query",
            "classical_oracle_queries": oracle.calls, **result}


def fixed_singular_line_fraction(matrix, p):
    from fractions import Fraction
    width = len(matrix)
    if not op.is_orthogonal(matrix, p):
        raise ValueError("isometry required")
    total = fixed = 0
    for line in all_subspaces(width, 1, p):
        if op.quadratic(line[0], p):
            continue
        total += 1
        fixed += op.image(matrix, line, p) == line
    return Fraction(fixed, total)


def universal_collision(left, right, p):
    ratio = op.mm(op.inverse(left, p), right, p)
    return ratio in (op.eye(len(left)), tuple(op.scale(-1, v, p) for v in op.eye(len(left))))
