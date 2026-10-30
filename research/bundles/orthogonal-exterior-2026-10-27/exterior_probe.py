"""Exterior-square probes for orthogonal HSP: prime-field reference only.

The native controller uses an opaque oracle. Its dense Fourier reference
costs p**binomial(n,2) CLASSICAL queries per probe, not quantum polynomial
time. The theorem's quantum resource ledger is a separate analytic object.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent /
                       "orthogonal-three-probe-2026-10-23"))
import orthogonal_probe as op


def gaussian_binomial(n, j, q):
    if not 0 <= j <= n:
        return 0
    result = Fraction(1)
    for i in range(j):
        result *= Fraction(q**(n-i)-1, q**(j-i)-1)
    assert result.denominator == 1
    return result.numerator


def skew_matrix(coordinates, n, p):
    pairs = tuple(combinations(range(n), 2))
    if len(coordinates) != len(pairs):
        raise ValueError("wrong exterior-square coordinate width")
    result = [[0]*n for _ in range(n)]
    for (i, j), a in zip(pairs, coordinates):
        result[i][j], result[j][i] = a % p, -a % p
    return tuple(tuple(row) for row in result)


def maximal_from_cell(x_space, tail_coordinates, n, p):
    """A Schubert cell relative to E; x_space=R intersection E is public."""
    x_space = op.basis(x_space, p)
    if any(len(v) != n for v in x_space):
        raise ValueError("wrong cell width")
    j = len(x_space)
    rows = list(x_space)
    for unit in op.eye(n):
        if len(op.basis(rows+[unit], p)) > len(rows):
            rows.append(unit)
    change = op.transpose(rows)
    dual = op.transpose(op.inverse(change, p))
    tail = skew_matrix(tail_coordinates, n-j, p)
    result = [v+(0,)*n for v in x_space]
    for col in range(n-j):
        x = (0,)*j+tuple(tail[row][col] for row in range(n-j))
        y = op.eye(n)[j+col]
        result.append(op.mv(change, x, p)+op.mv(dual, y, p))
    return op.basis(result, p)


def _randbelow(rng, bound, attempts):
    if bound == 1:
        return 0
    for _ in range(attempts):
        value = rng.getrandbits((bound-1).bit_length())
        if value < bound:
            return value
    raise RuntimeError("uniform integer sampler cap exhausted")


def sample_maximal(n, p, rng, *, row_attempts=128, integer_attempts=128):
    """Capped coupling to uniform sampling over BOTH maximal families.

    Cell j has [n choose j]_p * p**binomial(n-j,2) members. Conditional
    sampling is exact before caps; abort probabilities are charged in the
    proof rather than assuming globally uniform success-conditioned output.
    """
    if (type(n) is not int or n < 2 or type(row_attempts) is not int or row_attempts < 1
            or type(integer_attempts) is not int or integer_attempts < 1):
        raise ValueError("Witt rank >=2 and positive row cap required")
    op.make_probe(op.eye(2*n)[0], p)
    weights = [gaussian_binomial(n, j, p)*p**((n-j)*(n-j-1)//2)
               for j in range(n+1)]
    ticket = _randbelow(rng, sum(weights), integer_attempts)
    for j, weight in enumerate(weights):
        if ticket < weight:
            break
        ticket -= weight
    rows = []
    for _ in range(j):
        for _ in range(row_attempts):
            row = tuple(_randbelow(rng, p, integer_attempts) for _ in range(n))
            if len(op.basis(rows+[row], p)) > len(rows):
                rows.append(row)
                break
        else:
            raise RuntimeError("uniform maximal-space row sampler cap exhausted")
    count = (n-j)*(n-j-1)//2
    return maximal_from_cell(rows, tuple(_randbelow(rng, p, integer_attempts)
                                        for _ in range(count)), n, p)


@dataclass(frozen=True)
class ExteriorProbe:
    p: int
    frame: tuple
    undo: tuple

    @property
    def n(self):
        return len(self.frame)//2

    @property
    def width(self):
        return self.n*(self.n-1)//2

    def matrix(self, coordinates):
        n, p = self.n, self.p
        a = skew_matrix(coordinates, n, p)
        g = tuple(tuple(int(i == j)+(a[i][j-n] if i < n <= j else 0)
                        for j in range(2*n)) for i in range(2*n))
        return op.mm(op.mm(self.frame, g, p), self.undo, p)

    def image_support(self, kernel):
        columns = []
        for row in kernel:
            a = skew_matrix(row, self.n, self.p)
            columns.extend(op.mv(self.frame, col+(0,)*self.n, self.p)
                           for col in op.transpose(a))
        return op.basis(columns, self.p)


def make_probe(maximal, p):
    n = len(maximal)
    if n < 2:
        raise ValueError("Witt rank >=2 required")
    op.make_probe(op.eye(2*n)[0], p)
    frame = op.hyperbolic_frame(maximal, p)
    return ExteriorProbe(p, frame, op.inverse(frame, p))


def polar_complement(space, width, p):
    n = width//2
    return op.basis(op.nullspace(tuple(v[n:]+v[:n] for v in space), width, p), p)


def recover_reference(oracle, n, p, *, seed=157, probes=24, samples=24,
                      dimension_cap=1000, row_attempts=128):
    """Dense native oracle control, with no hidden subspace or rank input."""
    if type(n) is not int or n < 3 or type(probes) is not int or probes < 1:
        raise ValueError("Witt rank >=3 and positive probe cap required")
    if type(samples) is not int or samples < 1:
        raise ValueError("positive Fourier sample count required")
    op.make_probe(op.eye(2*n)[0], p)
    if p**(n*(n-1)//2) > dimension_cap:
        raise ValueError("dense reference dimension cap exceeded")
    rng, accumulated, inferred, records = random.Random(seed), (), None, []
    for _ in range(probes):
        maximal = sample_maximal(n, p, rng, row_attempts=row_attempts)
        probe = make_probe(maximal, p)
        kernel, record = op.dense_fourier_kernel(probe, oracle, rng, samples=samples,
                                                dimension_cap=dimension_cap)
        support = probe.image_support(kernel)
        record.update(kernel_rank=len(kernel), support_rank=len(support))
        records.append(record)
        if not 2 <= len(support) < n:
            record["screen"] = "uninformative_or_intersecting"
            continue
        k = n-len(support)
        if inferred is not None and k != inferred:
            raise RuntimeError("inconsistent rank: Fourier estimates not all exact")
        inferred = k
        accumulated = op.basis(accumulated+support, p)
        record.update(screen="proper_image_support", accumulated_rank=len(accumulated))
        if len(accumulated) > 2*n-k:
            raise RuntimeError("inconsistent accumulated rank")
        if len(accumulated) == 2*n-k:
            candidate = polar_complement(accumulated, 2*n, p)
            if (len(candidate) != k or any(op.quadratic(v, p) for v in candidate)
                    or any(op.polar(v, w, p) for v in candidate for w in candidate)):
                raise RuntimeError("candidate fails singular-space check")
            return {"candidate": candidate, "inferred_rank": inferred,
                    "records": records, "hidden_rank_supplied": False,
                    "quantum_algorithm_executed": False,
                    "certificate": "exact-kernel span theorem; not an oracle equality certificate"}
    raise RuntimeError("bounded exterior-probe attempts exhausted")


def recovery_budget(n, p, error_bits=40):
    if type(n) is not int or n < 3 or type(error_bits) is not int or error_bits < 1:
        raise ValueError("Witt rank >=3 and positive error bits required")
    op.make_probe(op.eye(2*n)[0], p)
    epsilon = Fraction(1, 2**error_bits)
    stage_attempts = 1
    while 2*n*Fraction(3, 8)**stage_attempts > epsilon/4:
        stage_attempts += 1
    probe_cap = 2*n*stage_attempts
    slack = 0
    while Fraction(probe_cap, (p-1)*p**slack) > epsilon/4:
        slack += 1
    row_cap = 1
    while Fraction(probe_cap*n, p**row_cap) > epsilon/8:
        row_cap += 1
    integer_calls = probe_cap*(1+n*n*row_cap+n*(n-1)//2)
    integer_cap = 1
    while Fraction(integer_calls, 2**integer_cap) > epsilon/8:
        integer_cap += 1
    samples = n*(n-1)//2+slack
    return {"n": n, "p": p, "hidden_rank_promise": [1, n-2],
            "hidden_rank_required": False, "error_target": str(epsilon),
            "stage_attempts": stage_attempts, "probe_cap": probe_cap,
            "fourier_samples_per_probe": samples, "row_attempt_cap": row_cap,
            "uniform_integer_call_cap": integer_calls, "uniform_integer_attempt_cap": integer_cap,
            "geometry_failure_bound": str(2*n*Fraction(3, 8)**stage_attempts),
            "all_rank_failure_bound": str(Fraction(probe_cap, (p-1)*p**slack)),
            "row_sampler_failure_bound": str(Fraction(probe_cap*n, p**row_cap)),
            "integer_sampler_failure_bound": str(Fraction(integer_calls, 2**integer_cap)),
            "original_oracle_query_cap": probe_cap*samples,
            "error_per_complete_instrument": str(epsilon/(4*probe_cap*samples)),
            "all_ranks_classical_lower_bound_proved": False,
            "hidden_line_lower_bound_document": "CLASSICAL_COMPARATOR.md",
            "quantum_algorithm_executed": False}
