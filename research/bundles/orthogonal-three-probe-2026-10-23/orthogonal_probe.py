"""Exact public controls for a proposed split-orthogonal parabolic reduction.

Prime-field implementation. The dense Fourier learner is an exponential-size
REFERENCE SIMULATOR, not a scalable quantum implementation. Controller code
has no hidden-subspace argument; the fixture oracle alone owns that data.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import random
import sys

import numpy as np
from flint import fmpz

WORK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORK / "central-rank-2026-10-23"))
from central_rank import row_basis


def basis(rows, p):
    rows = tuple(tuple(x % p for x in row) for row in rows)
    return row_basis(rows, p) if rows else ()


def eye(d):
    return tuple(tuple(int(i == j) for j in range(d)) for i in range(d))


def add(v, w, p):
    return tuple((a+b) % p for a, b in zip(v, w))


def scale(a, v, p):
    return tuple(a*x % p for x in v)


def dot(v, w, p):
    return sum(a*b for a, b in zip(v, w)) % p


def quadratic(v, p):
    n = len(v)//2
    return dot(v[:n], v[n:], p)


def polar(v, w, p):
    n = len(v)//2
    return (dot(v[:n], w[n:], p) + dot(v[n:], w[:n], p)) % p


def mv(matrix, v, p):
    return tuple(dot(row, v, p) for row in matrix)


def mm(left, right, p):
    return tuple(tuple(dot(row, column, p) for column in zip(*right)) for row in left)


def transpose(matrix):
    return tuple(zip(*matrix))


def inverse(matrix, p):
    n = len(matrix)
    reduced = basis([tuple(row)+unit for row, unit in zip(matrix, eye(n))], p)
    if len(reduced) != n or tuple(row[:n] for row in reduced) != eye(n):
        raise ValueError("invertible square matrix required")
    return tuple(row[n:] for row in reduced)


def nullspace(rows, width, p):
    reduced = basis(rows, p)
    pivots = [next(i for i, x in enumerate(row) if x) for row in reduced]
    result = []
    for free in range(width):
        if free in pivots:
            continue
        vector = [0]*width
        vector[free] = 1
        for pivot, row in zip(pivots, reduced):
            vector[pivot] = -row[free] % p
        result.append(tuple(vector))
    return tuple(result)


def intersection(left, right, width, p):
    equations = nullspace(left, width, p) + nullspace(right, width, p)
    return basis(nullspace(equations, width, p), p)


def span_coordinates(coefficients, rows, p):
    return tuple(sum(c*row[j] for c, row in zip(coefficients, rows)) % p
                 for j in range(len(rows[0])))


def image(matrix, subspace, p):
    return basis((mv(matrix, v, p) for v in subspace), p)


def is_maximal_singular(subspace, n, p):
    subspace = basis(subspace, p)
    return (len(subspace) == n and all(len(v) == 2*n and quadratic(v, p) == 0 for v in subspace)
            and all(polar(v, w, p) == 0 for v in subspace for w in subspace))


def is_orthogonal(matrix, p):
    d = len(matrix)
    if d % 2 or any(len(row) != d for row in matrix):
        return False
    columns = transpose(matrix)
    return (all(quadratic(v, p) == 0 for v in columns)
            and all(polar(columns[i], columns[j], p) == int(abs(i-j) == d//2)
                    for i in range(d) for j in range(d)))


def digits(value, width, p):
    result = []
    for _ in range(width):
        value, digit = divmod(value, p)
        result.append(digit)
    if value:
        raise ValueError("integer exceeds vector width")
    return tuple(result)


def random_singular(n, p, rng):
    """Uniform NONZERO singular vector, without 1/p rejection sampling."""
    if rng.randrange(p**(n-1)+1) == 0:
        return digits(rng.randrange(1, p**n), n, p) + (0,)*n
    y = digits(rng.randrange(1, p**n), n, p)
    pivot = next(i for i, value in enumerate(y) if value)
    x = [rng.randrange(p) if i != pivot else 0 for i in range(n)]
    x[pivot] = -dot(x, y, p)*pow(y[pivot], -1, p) % p
    return tuple(x) + y


@dataclass(frozen=True)
class Probe:
    p: int
    e: tuple
    dual: tuple
    complement: tuple

    @property
    def width(self):
        return len(self.complement)

    def matrix(self, coordinates):
        if len(coordinates) != self.width:
            raise ValueError("wrong probe coordinate width")
        w = span_coordinates(coordinates, self.complement, self.p)
        p, e, d = self.p, self.e, len(self.e)
        je = e[d//2:] + e[:d//2]
        jw = w[d//2:] + w[:d//2]
        q = quadratic(w, p)
        return tuple(tuple((int(i == j) + w[i]*je[j] - e[i]*jw[j]
                            - q*e[i]*je[j]) % p for j in range(d)) for i in range(d))

    def neighbor(self, kernel):
        if len(basis(kernel, self.p)) != len(self.e)//2-1:
            raise ValueError("probe did not return the expected complete kernel")
        rows = [self.e] + [span_coordinates(v, self.complement, self.p) for v in kernel]
        result = basis(rows, self.p)
        if not is_maximal_singular(result, len(self.e)//2, self.p):
            raise ValueError("learned neighbor is not maximal singular")
        return result


def make_probe(e, p):
    if type(p) is not int or p < 3 or not fmpz(p).is_prime():
        raise ValueError("odd prime field required by this implementation")
    e = tuple(e)
    d = len(e)
    if d % 2 or not any(e) or quadratic(e, p):
        raise ValueError("nonzero singular vector required")
    je = e[d//2:] + e[:d//2]
    pivot = next(i for i, value in enumerate(je) if value)
    v = [0]*d
    v[pivot] = pow(je[pivot], -1, p)
    dual = add(v, scale(-quadratic(v, p), e, p), p)
    jf = dual[d//2:] + dual[:d//2]
    complement = nullspace((je, jf), d, p)
    if len(complement) != d-2 or polar(e, dual, p) != 1 or quadratic(dual, p):
        raise ArithmeticError("hyperbolic probe frame failed")
    return Probe(p, e, dual, complement)


def reconstruct_neighbors(neighbors, n, p):
    if n < 3 or len(neighbors) != 3:
        raise ValueError("three probes and Witt rank at least three required")
    candidate = basis([v for i, j in combinations(range(3), 2)
                       for v in intersection(neighbors[i], neighbors[j], 2*n, p)], p)
    if not is_maximal_singular(candidate, n, p):
        raise ValueError("three-probe geometry was degenerate")
    return candidate


def hyperbolic_frame(candidate, p):
    """Complete a known maximal singular basis; no hidden data are used."""
    candidate = basis(candidate, p)
    n = len(candidate)
    if p == 2 or not is_maximal_singular(candidate, n, p):
        raise ValueError("odd-prime maximal singular candidate required")
    equations = tuple(v[n:]+v[:n] for v in candidate)
    duals = []
    for j in range(n):
        augmented = basis([row + (int(i == j),) for i, row in enumerate(equations)], p)
        v = [0]*(2*n)
        for row in augmented:
            pivot = next(i for i, value in enumerate(row[:-1]) if value)
            v[pivot] = row[-1]
        duals.append(tuple(v))
    gram = tuple(tuple(polar(v, w, p) for w in duals) for v in duals)
    half = pow(2, -1, p)
    corrected = [add(v, span_coordinates(tuple(-half*gram[j][i] % p for j in range(n)),
                                         candidate, p), p)
                 for i, v in enumerate(duals)]
    frame = transpose(candidate + tuple(corrected))
    if not is_orthogonal(frame, p):
        raise ArithmeticError("candidate hyperbolic completion failed")
    return frame


def certificate_matrices(candidate, p):
    n = len(candidate)
    if n < 2:
        raise ValueError("certificate requires Witt rank at least two")
    frame = hyperbolic_frame(candidate, p)
    undo = inverse(frame, p)
    tests = []
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            g = [list(row) for row in eye(2*n)]
            g[i][j] = 1
            g[n+j][n+i] = -1 % p
            tests.append(mm(mm(frame, g, p), undo, p))
    g = [list(row) for row in eye(2*n)]
    g[0][n+1], g[1][n] = 1, -1 % p
    tests.append(mm(mm(frame, g, p), undo, p))
    return tuple(tests)


def certify(candidate, oracle, p, identity_label=None):
    label = oracle(eye(2*len(candidate))) if identity_label is None else identity_label
    return all(oracle(g) == label for g in certificate_matrices(candidate, p))


class OpaqueFixtureOracle:
    """Test fixture only: f(g) is an opaque relabeling of gL, NOT L itself."""

    def __init__(self, hidden, p):
        self._hidden, self.p = basis(hidden, p), p
        self._labels = {}
        self.calls = 0

    def __call__(self, g):
        if not is_orthogonal(g, self.p):
            raise ValueError("oracle query is outside the orthogonal group")
        self.calls += 1
        key = image(g, self._hidden, self.p)
        if key not in self._labels:
            self._labels[key] = len(self._labels)
        return self._labels[key]


def dense_fourier_kernel(probe, oracle, rng, *, samples=18, dimension_cap=1000):
    """Execute the finite coset-source/QFT probability calculation.

    Charges p**width classical table queries. This is NOT the query count
    of the proposed scalable AHSP routine, which would query once per sample.
    """
    p, d = probe.p, probe.width
    size = p**d
    if size > dimension_cap:
        raise ValueError("dense reference dimension cap exceeded")
    fibers = {}
    points = tuple(product(range(p), repeat=d))
    for point in points:
        label = oracle(probe.matrix(point))
        fibers.setdefault(label, []).append(point)
    probabilities = np.zeros((p,)*d)
    for fiber in fibers.values():
        amplitude = np.zeros((p,)*d)
        for point in fiber:
            amplitude[point] = 1
        probabilities += np.abs(np.fft.fftn(amplitude))**2 / size**2
    flat = probabilities.ravel()
    if abs(float(flat.sum())-1) > 1e-10:
        raise ArithmeticError("Fourier probability normalization failed")
    frequencies = rng.choices(points, weights=flat, k=samples)
    kernel = basis(nullspace(frequencies, d, p), p)
    return kernel, {
        "classical_table_queries": size, "simulated_fourier_samples": samples,
        "fibers": len(fibers), "fiber_sizes": sorted({len(f) for f in fibers.values()}),
        "fourier_support_size": int(np.count_nonzero(flat > 1e-10)),
        "probability_sum": float(flat.sum()),
        "sampled_frequencies": frequencies,
        "recovered_additive_kernel": kernel,
    }


def recover_reference(oracle, n, p, *, seed=83, attempts=12, samples=18,
                      dimension_cap=1000):
    if n < 3 or p < 3:
        raise ValueError("odd-prime input and Witt rank at least three required")
    rng = random.Random(seed)
    identity_label = oracle(eye(2*n))
    records = []
    for attempt in range(attempts):
        neighbors, current = [], []
        for _ in range(3):
            probe = make_probe(random_singular(n, p, rng), p)
            kernel, record = dense_fourier_kernel(probe, oracle, rng, samples=samples,
                                                  dimension_cap=dimension_cap)
            record["probe_vector"] = probe.e
            record["kernel_rank"] = len(kernel)
            current.append(record)
            try:
                neighbors.append(probe.neighbor(kernel))
            except ValueError:
                break
        records.append(current)
        if len(neighbors) != 3:
            continue
        try:
            candidate = reconstruct_neighbors(neighbors, n, p)
        except ValueError:
            continue
        if certify(candidate, oracle, p, identity_label):
            return {"candidate": candidate, "attempts": attempt+1,
                    "records": records, "certificate_passed": True}
    raise RuntimeError("bounded reference attempts exhausted")


def recovery_budget(n, p, error_bits=40):
    """Proposed scalable AHSP schedule, NOT dense-reference runtime counts."""
    if type(n) is not int or n < 3 or type(error_bits) is not int or error_bits < 1:
        raise ValueError("rank >=3 and positive integer error bits required")
    if type(p) is not int or p < 3 or not fmpz(p).is_prime():
        raise ValueError("odd prime required")
    epsilon = Fraction(1, 2**error_bits)
    rounds = 1
    while Fraction(2, 3)**rounds > epsilon/4:
        rounds += 1
    surplus = 0
    while Fraction(1, (p-1)*p**surplus) > epsilon/(12*rounds):
        surplus += 1
    samples = 2*n-2+surplus
    fourier = 3*rounds*samples
    certificates = rounds*(n*(n-1)+1)
    return {
        "witt_rank": n, "prime": p, "total_error_target": str(epsilon),
        "trial_cap": rounds, "abelian_hsp_call_cap": 3*rounds,
        "fourier_samples_per_probe": samples,
        "total_fourier_instruments": fourier,
        "original_oracle_query_cap": fourier+certificates+1,
        "geometry_failure_bound": str(Fraction(2, 3)**rounds),
        "all_rank_failure_bound": str(Fraction(3*rounds, (p-1)*p**surplus)),
        "error_per_complete_fourier_instrument": str(epsilon/(4*fourier)),
        "global_classical_sampling_error_allowance": str(epsilon/4),
        "source_cost_per_fourier_sample": 1,
        "independent_proof_review_completed": False,
        "compiled_gate_count": None,
        "dense_reference_cost_is_this_budget": False,
    }
