"""Unknown-rank orthogonal reduction: public prime-field reference controls.

The only learner below is an exponential dense Fourier reference. It is NOT
an implementation of a scalable quantum algorithm. No hidden U or rank is
an input to the controller or certificate.
"""

from fractions import Fraction
from itertools import combinations
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent /
                       "orthogonal-three-probe-2026-10-23"))
import orthogonal_probe as op


def singular(space, n, p):
    rows = tuple(tuple(v) for v in space)
    if any(len(v) != 2*n for v in rows):
        return False
    rows = op.basis(rows, p)
    return (len(rows) <= n and all(op.quadratic(v, p) == 0 for v in rows)
            and all(op.polar(v, w, p) == 0 for v in rows for w in rows))


def neighbor(probe, kernel):
    rows = tuple(tuple(v) for v in kernel)
    if any(len(v) != probe.width for v in rows):
        raise ValueError("wrong kernel coordinate width")
    rows = op.basis(rows, probe.p)
    n = len(probe.e)//2
    if not 2 <= len(rows) <= n-1:
        raise ValueError("kernel dimension outside unknown-rank gate")
    result = op.basis((probe.e,) + tuple(op.span_coordinates(v, probe.complement,
                                                           probe.p) for v in rows), probe.p)
    if len(result) != len(rows)+1 or not singular(result, n, probe.p):
        raise ValueError("neighbor is not singular of the required dimension")
    return result


def reconstruct(neighbors, n, p):
    if len(neighbors) != 3:
        raise ValueError("three neighbors required")
    neighbors = tuple(op.basis(s, p) for s in neighbors)
    r = len(neighbors[0])
    if not 3 <= r <= n or any(len(s) != r or not singular(s, n, p) for s in neighbors):
        raise ValueError("inconsistent neighbor ranks or nonsingular neighbor")
    candidate = op.basis((v for i, j in combinations(range(3), 2)
                          for v in op.intersection(neighbors[i], neighbors[j], 2*n, p)), p)
    if len(candidate) != r or not singular(candidate, n, p):
        raise ValueError("degenerate intersection reconstruction")
    return candidate


def witt_decomposition(candidate, p):
    candidate = op.basis(candidate, p)
    if not candidate:
        raise ValueError("nonempty singular candidate required")
    r, width = len(candidate), len(candidate[0])
    n = width//2
    if width % 2 or not 3 <= r <= n or not singular(candidate, n, p):
        raise ValueError("singular candidate of rank at least three required")
    # make_probe validates the reference implementation's prime-field contract.
    op.make_probe(candidate[0], p)
    equations = tuple(v[n:]+v[:n] for v in candidate)
    duals = []
    for j in range(r):
        augmented = op.basis((row+(int(i == j),) for i, row in enumerate(equations)), p)
        v = [0]*width
        for row in augmented:
            pivot = next(i for i, value in enumerate(row[:-1]) if value)
            v[pivot] = row[-1]
        duals.append(tuple(v))
    gram = tuple(tuple(op.polar(v, w, p) for w in duals) for v in duals)
    half = pow(2, -1, p)
    duals = tuple(op.add(v, op.span_coordinates(tuple(-half*gram[j][i] % p
                                                     for j in range(r)), candidate, p), p)
                  for i, v in enumerate(duals))
    middle = op.nullspace(tuple(v[n:]+v[:n] for v in candidate+duals), width, p)
    frame = op.transpose(candidate+middle+duals)
    undo = op.inverse(frame, p)
    return candidate, middle, duals, frame, undo


def certificate_matrices(candidate, p):
    candidate, middle, _, frame, undo = witt_decomposition(candidate, p)
    r, width = len(candidate), len(frame)
    offset = width-r
    tests = []
    for i in range(r):
        for j in range(r):
            if i == j:
                continue
            g = [list(row) for row in op.eye(width)]
            g[i][j], g[offset+j][offset+i] = 1, -1 % p
            tests.append(op.mm(op.mm(frame, g, p), undo, p))
    g = [list(row) for row in op.eye(width)]
    g[0][offset+1], g[1][offset] = 1, -1 % p
    tests.append(op.mm(op.mm(frame, g, p), undo, p))
    e = candidate[0]
    je = e[width//2:]+e[:width//2]
    for w in middle:
        jw = w[width//2:]+w[:width//2]
        q = op.quadratic(w, p)
        tests.append(tuple(tuple((int(i == j)+w[i]*je[j]-e[i]*jw[j]
                                  -q*e[i]*je[j]) % p for j in range(width))
                           for i in range(width)))
    return tuple(tests)


def certify_containment(candidate, oracle, p, identity_label=None):
    matrices = certificate_matrices(candidate, p)
    origin = oracle(op.eye(len(matrices[0]))) if identity_label is None else identity_label
    return all(oracle(g) == origin for g in matrices)


def recover_reference(oracle, n, p, *, seed=83, attempts=20, samples=22, dimension_cap=1000):
    """Dense finite reference controller, requiring no hidden-rank argument."""
    if type(n) is not int or n < 3 or type(attempts) is not int or attempts < 1:
        raise ValueError("Witt rank >=3 and positive trial cap required")
    if type(samples) is not int or samples < 1:
        raise ValueError("positive Fourier sample count required")
    op.make_probe(op.eye(2*n)[0], p)
    rng = random.Random(seed)
    origin, records = oracle(op.eye(2*n)), []
    for attempt in range(attempts):
        neighbors, current = [], []
        records.append(current)
        for _ in range(3):
            probe = op.make_probe(op.random_singular(n, p, rng), p)
            kernel, record = op.dense_fourier_kernel(probe, oracle, rng, samples=samples,
                                                    dimension_cap=dimension_cap)
            record.update(probe_vector=probe.e, kernel_rank=len(kernel))
            current.append(record)
            try:
                neighbors.append(neighbor(probe, kernel))
            except ValueError:
                break
        if len(neighbors) != 3:
            continue
        try:
            candidate = reconstruct(neighbors, n, p)
        except ValueError:
            continue
        if certify_containment(candidate, oracle, p, origin):
            return {"candidate": candidate, "inferred_rank": len(candidate),
                    "attempts": attempt+1, "records": records,
                    "containment_certificate_passed": True,
                    "quantum_algorithm_executed": False,
                    "hidden_rank_supplied_to_controller": False}
    raise RuntimeError("bounded reference attempts exhausted")


def geometry_probability(n, k, q):
    if not 3 <= k <= n or q < 3:
        raise ValueError("requires odd-field theorem range 3<=k<=n, q>=3")
    a = Fraction((q**k-1)*q**(2*n-k-1), (q**n-1)*(q**(n-1)+1))
    return a**3*Fraction((q**k-q)*(q**k-q*q), (q**k-1)**2)


def reflection_hit_probability(n, k, q):
    if not 1 <= k <= n or q < 3:
        raise ValueError("requires 1<=k<=n and q>=3")
    return Fraction(q**(n-k)-1, q**n-1)


def recovery_budget(n, p, error_bits=40):
    result = op.recovery_budget(n, p, error_bits)
    # The imported maximal-only budget has stale review metadata, not a cost.
    result.pop("independent_proof_review_completed", None)
    result.update(hidden_rank_required=False, hidden_rank_promise=[3, n],
                  certificate_claim="containment, with rank/probe provenance for equality",
                  arbitrary_rank_classical_lower_bound_proved=False,
                  quantum_algorithm_executed=False)
    return result
