"""Supplied-secret algebra controls. NEVER use as the algorithm's learner."""

from itertools import product
import random

import general_rank as gr

op = gr.op


def coordinates(v, rows, p):
    equations = [tuple(column)+(value,) for column, value in zip(zip(*rows), v)]
    reduced = op.basis(equations, p)
    if any(not any(row[:-1]) and row[-1] for row in reduced):
        raise ValueError("outside the coordinate span")
    result = [0]*len(rows)
    for row in reduced:
        pivot = next(i for i, value in enumerate(row[:-1]) if value)
        result[pivot] = row[-1]
    return tuple(result)


def expected_kernel(probe, hidden):
    p, width = probe.p, len(probe.e)
    hidden = op.basis(hidden, p)
    if len(op.basis(hidden+(probe.e,), p)) == len(hidden):
        return op.eye(probe.width), "in_U"
    if all(op.polar(probe.e, u, p) == 0 for u in hidden):
        equations = [tuple(op.polar(u, w, p) for w in probe.complement) for u in hidden]
        return op.basis(op.nullspace(equations, probe.width, p), p), "perpendicular_not_in_U"
    perp = op.nullspace((probe.e[width//2:]+probe.e[:width//2],), width, p)
    section = op.intersection(hidden, perp, width, p)
    projected = [op.add(u, op.scale(-op.polar(probe.dual, u, p), probe.e, p), p)
                 for u in section]
    return op.basis((coordinates(v, probe.complement, p) for v in projected), p), "good"


def changed_frame(n, p, seed=170):
    rng, matrix = random.Random(seed), op.eye(2*n)
    for _ in range(5):
        probe = op.make_probe(op.random_singular(n, p, rng), p)
        step = probe.matrix(tuple(rng.randrange(p) for _ in range(probe.width)))
        matrix = op.mm(step, matrix, p)
    return matrix


def kernel_fiber_control(n, k, p, e):
    hidden = op.eye(2*n)[:k]
    probe = op.make_probe(e, p)
    kernel, kind = expected_kernel(probe, hidden)
    oracle = op.OpaqueFixtureOracle(hidden, p)
    origin, fibers, actual = oracle(op.eye(2*n)), {}, []
    for w in product(range(p), repeat=probe.width):
        label = oracle(probe.matrix(w))
        fibers.setdefault(label, []).append(w)
        assert (label == origin) == (len(op.basis(kernel+(w,), p)) == len(kernel))
        if label == origin:
            actual.append(w)
    assert op.basis(actual, p) == kernel
    for points in fibers.values():
        assert len(points) == p**len(kernel)
        for w in points:
            difference = op.add(w, op.scale(-1, points[0], p), p)
            assert len(op.basis(kernel+(difference,), p)) == len(kernel)
    return {"n": n, "hidden_rank": k, "p": p, "case": kind,
            "kernel_rank": len(kernel), "full_table_points": p**probe.width,
            "oracle_calls": oracle.calls, "all_fibers_checked": True}
