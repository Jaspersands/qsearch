"""Classical same-oracle attack using random isotropic restrictions.

The controller sees only opaque labels. Reference implementations of field
arithmetic are prime-field only. All actual oracle calls are counted.
"""

from fractions import Fraction
from math import isqrt
from pathlib import Path
import random
import sys

WORK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORK / "orthogonal-three-probe-2026-10-23"))
import orthogonal_probe as op


def coordinates(vector, rows, p):
    reduced = op.basis([tuple(column)+(value,) for column, value in zip(zip(*rows), vector)], p)
    if any(not any(row[:-1]) and row[-1] for row in reduced):
        raise ValueError("vector is not in the public coordinate span")
    answer = [0]*len(rows)
    for row in reduced:
        pivot = next(i for i, value in enumerate(row[:-1]) if value)
        answer[pivot] = row[-1]
    return tuple(answer)


def complement_frame(probe):
    """A public hyperbolic basis for the probe complement, in ambient rows."""
    p, e, ambient = probe.p, probe.e, len(probe.e)
    rank = ambient//2-1
    if rank == 0:
        return ()
    # The reference maximal singular subspace is PUBLIC, not the hidden L.
    reference = op.eye(ambient)[:ambient//2]
    a = op.intersection(probe.complement, op.basis(reference+(e,), p), ambient, p)
    if len(a) != rank:
        raise ArithmeticError("public singular section has incorrect rank")
    equations = tuple(tuple(op.polar(v, w, p) for w in probe.complement) for v in a)
    duals = []
    for j in range(rank):
        augmented = op.basis([row+(int(i == j),) for i, row in enumerate(equations)], p)
        coefficients = [0]*probe.width
        for row in augmented:
            pivot = next(i for i, value in enumerate(row[:-1]) if value)
            coefficients[pivot] = row[-1]
        duals.append(op.span_coordinates(coefficients, probe.complement, p))
    half = pow(2, -1, p)
    b = [op.add(v, op.span_coordinates(tuple(-half*op.polar(v, w, p) % p for w in duals), a, p), p)
         for v in duals]
    frame = a+tuple(b)
    if any(op.quadratic(v, p) for v in frame) or any(
            op.polar(v, w, p) != int(abs(i-j) == rank)
            for i, v in enumerate(frame) for j, w in enumerate(frame)):
        raise ArithmeticError("public complement frame is not hyperbolic")
    return frame


def random_maximal_singular(rank, p, rng):
    """Exactly uniform ideal-RNG sampler, by singular-line incidence recursion."""
    if type(rank) is not int or rank < 1:
        raise ValueError("positive rank required")
    e = op.random_singular(rank, p, rng)
    if rank == 1:
        return op.basis((e,), p)
    probe = op.make_probe(e, p)
    frame = complement_frame(probe)
    lower = random_maximal_singular(rank-1, p, rng)
    return op.basis((e,)+tuple(op.span_coordinates(v, frame, p) for v in lower), p)


def restriction(probe, rng):
    rank = probe.width//2
    frame = complement_frame(probe)
    ambient = [op.span_coordinates(v, frame, probe.p)
               for v in random_maximal_singular(rank, probe.p, rng)]
    return op.basis([coordinates(v, probe.complement, probe.p) for v in ambient], probe.p)


def query_schedule(n, p, error_bits=20):
    if type(n) is not int or n < 3 or type(error_bits) is not int or error_bits < 1:
        raise ValueError("rank >=3 and positive integer error bits required")
    # Reuse the exact prime-field guard, without allocating a large table.
    op.make_probe(op.eye(2*n)[0], p)
    r, index = n-1, p**(n-2)
    root = isqrt(index)
    if root*root < index:
        root += 1
    queries_per_round = min(p**r, 3*root+1)
    rounds = 0
    failure = Fraction(2**r)
    while failure > Fraction(1, 2**error_bits):
        rounds += 1
        failure *= Fraction(7, 8)
    return {"rank": n, "prime": p, "kernel_rank_if_probe_outside_hidden": r,
            "query_cap_per_round": queries_per_round, "round_cap": rounds,
            "probe_query_cap": rounds*queries_per_round,
            "conditional_rank_failure_bound": str(failure),
            "conditioning": "probe e is outside the hidden maximal singular L",
            "sampler_draws_have_expected_polynomial_overhead": True,
            "memory_labels_cap": queries_per_round}


def collision_round(probe, rows, oracle, rng, query_cap):
    """Sample DISTINCT restriction parameters; zero differences give no evidence."""
    p, rank = probe.p, len(rows)
    domain = p**rank
    seen_parameters, labels = set(), {}
    draws = calls = 0
    for _ in range(min(query_cap, domain)):
        # Sparse partial Fisher-Yates is unnecessary for the stated expected
        # arithmetic bound; rejection leaves exact uniform distinct samples.
        key = rng.randrange(domain)
        draws += 1
        while key in seen_parameters:
            key = rng.randrange(domain)
            draws += 1
        seen_parameters.add(key)
        w = op.span_coordinates(op.digits(key, rank, p), rows, p)
        label = oracle(probe.matrix(w))
        calls += 1
        if label in labels:
            difference = op.add(w, op.scale(-1, labels[label], p), p)
            if not any(difference):
                raise ArithmeticError("repeated parameter created a false collision")
            return difference, {"queries": calls, "parameter_draws": draws,
                                "labels_stored": len(labels), "collision": True}
        labels[label] = w
    return None, {"queries": calls, "parameter_draws": draws,
                  "labels_stored": len(labels), "collision": False}


def learn_probe(probe, oracle, rng, *, error_bits=20, max_queries=100000):
    n, p = len(probe.e)//2, probe.p
    schedule = query_schedule(n, p, error_bits)
    if schedule["probe_query_cap"] > max_queries:
        raise ValueError("classical query cap exceeds the execution safety limit")
    kernel, records = (), []
    for _ in range(schedule["round_cap"]):
        rows = restriction(probe, rng)
        vector, record = collision_round(probe, rows, oracle, rng, schedule["query_cap_per_round"])
        if vector is not None:
            kernel = op.basis(kernel+(vector,), p)
        record["observed_span_rank"] = len(kernel)
        records.append(record)
        if len(kernel) == n-1:
            break
    return kernel, {"schedule": schedule, "rounds": records,
                    "actual_queries": sum(row["queries"] for row in records),
                    "complete_rank": len(kernel) == n-1,
                    "hidden_subspace_supplied_to_controller": False}


def recover(oracle, n, p, *, seed=402, attempts=12, error_bits=20, max_probe_queries=100000):
    if type(attempts) is not int or attempts < 1:
        raise ValueError("positive integer recovery-attempt cap required")
    query_schedule(n, p, error_bits)
    rng = random.Random(seed)
    identity = oracle(op.eye(2*n))
    queries = 1
    records = []
    for _ in range(attempts):
        neighbors, current = [], []
        for _ in range(3):
            probe = op.make_probe(op.random_singular(n, p, rng), p)
            kernel, record = learn_probe(probe, oracle, rng, error_bits=error_bits,
                                         max_queries=max_probe_queries)
            queries += record["actual_queries"]
            record["probe_vector"] = probe.e
            record["kernel"] = kernel
            current.append(record)
            if not record["complete_rank"]:
                break
            try:
                neighbors.append(probe.neighbor(kernel))
            except ValueError:
                break
        records.append(current)
        if len(neighbors) < 3:
            continue
        try:
            candidate = op.reconstruct_neighbors(neighbors, n, p)
        except ValueError:
            continue
        accepted = True
        for g in op.certificate_matrices(candidate, p):
            queries += 1
            if oracle(g) != identity:
                accepted = False
                break
        if accepted:
            return {"candidate": candidate, "certificate_passed": True,
                    "actual_queries": queries, "records": records,
                    "quantum": False, "dense_table_constructed": False}
    return {"candidate": None, "certificate_passed": False,
            "actual_queries": queries, "records": records,
            "quantum": False, "dense_table_constructed": False}
