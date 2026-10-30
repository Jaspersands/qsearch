"""Public arithmetic for elliptic descent membership; no geometric backend.

The callback in the digit protocol is a proof obligation. Exact supplied-map
controls live separately and must never be installed as a native oracle.
"""

from dataclasses import dataclass
from math import gcd, prod
from pathlib import Path
import sys

from sympy import Matrix, eye, isprime, nextprime, zeros

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "double-level-source-2026-10-25"))
from double_level_source import checked_factors
from local_baseline import local_frame
from kernel_output import (
    check_split, coordinate_map, flat, integer_matrix, inverse_mod, mod,
)


def reduced_norm(order, alpha):
    alpha = integer_matrix(alpha)
    if alpha.shape != (4, 1):
        raise ValueError("four integral order coordinates required")
    value = order.multiply(order.star(alpha), alpha)
    indices = [i for i, x in enumerate(order.unit) if x]
    norm = value[indices[0]] / order.unit[indices[0]]
    if norm.q != 1 or norm < 0 or value != norm*order.unit:
        raise ValueError("positive definite integral quaternion norm required")
    return int(norm)


def embed_local(matrix, q, e, n, factors):
    """Prescribed FULL q^e residue, identity on other primary components."""
    factors = checked_factors(n, factors)
    if (q, e) not in factors:
        raise ValueError("component must match the original factorization")
    matrix = integer_matrix(matrix)
    if matrix.shape != (2, 2):
        raise ValueError("two by two query required")
    m, other = q**e, n//q**e
    idempotent = other*pow(other, -1, m)
    return mod(idempotent*matrix+(1-idempotent)*eye(2), n)


@dataclass(frozen=True)
class MembershipPlan:
    order: object
    actions: tuple
    n: int
    factors: tuple
    characteristic: int
    norm_bound: int
    primes: tuple
    coordinate_inverse: object

    @classmethod
    def create(cls, order, actions, n, factors, characteristic):
        factors = checked_factors(n, factors)
        p = characteristic
        if type(p) is not int or p <= 3 or not isprime(p) or gcd(n, p) != 1:
            raise ValueError("prime characteristic > 3 coprime to degree required")
        check_split(order, actions, n)
        b0 = sum(reduced_norm(order, eye(4)[:, j]) for j in range(4))
        bound = 4*(n*p)**2*b0
        primes, product, r = [], 1, 2
        while product <= 8*n*n*bound*bound:
            r = int(nextprime(r))
            if gcd(r, n*p) == 1:
                primes.append(r)
                product *= r
        return cls(order, tuple(actions), n, factors, p, bound, tuple(primes),
                   inverse_mod(coordinate_map(actions), n))

    def lift(self, matrix):
        """CRT to alpha=matrix mod n and alpha=1 mod p; no norm smoothness."""
        matrix = integer_matrix(matrix)
        if matrix.shape != (2, 2):
            raise ValueError("two by two query required")
        residues = mod(self.coordinate_inverse*flat(matrix), self.n)
        modulus = self.n*self.characteristic
        alpha = Matrix([
            int(x)+self.n*((int(u)-int(x))*pow(self.n, -1, self.characteristic)
                          % self.characteristic)
            for x, u in zip(residues, self.order.unit)
        ]).applyfunc(lambda x: (int(x)+modulus//2) % modulus-modulus//2)
        norm = reduced_norm(self.order, alpha)
        if not 0 < norm <= self.norm_bound or norm % self.characteristic != 1:
            raise ArithmeticError("public lift violates uniform norm contract")
        return alpha, norm

    def probe(self, matrix):
        alpha, norm = self.lift(matrix)
        retained = filter_transcript(self.primes, self.n, self.characteristic,
                                     norm, self.norm_bound)
        return {"alpha": alpha, "norm": norm, "primes": retained,
                "torsion_level": prod(retained)}


def filter_transcript(primes, n, characteristic, norm, norm_bound):
    """Use only a preselected transcript; never fetch extra adaptive levels."""
    primes = tuple(primes)
    if (type(norm) is not int or type(norm_bound) is not int
            or not 0 < norm <= norm_bound or gcd(norm, characteristic) != 1):
        raise ValueError("positive bounded prime-to-characteristic norm required")
    if (len(set(primes)) != len(primes) or not primes
            or any(type(r) is not int or r == 2 or not isprime(r)
                   or gcd(r, n*characteristic) != 1 for r in primes)):
        raise ValueError("distinct odd primes away from native degree/characteristic required")
    if prod(primes) <= 8*n*n*norm_bound*norm_bound:
        raise ValueError("finite transcript lacks the uniform completeness bound")
    retained = tuple(r for r in primes if norm % r)
    m = prod(retained)
    if m <= norm or m*m <= 8*n*n*norm or gcd(m, norm*n*characteristic) != 1:
        raise ArithmeticError("filtered transcript violates interpolation separation bound")
    return retained


def prefix_queries(vector, q, e, depth, digits):
    if (type(depth) is not int or type(digits) is not int
            or not 1 <= digits <= depth <= e):
        raise ValueError("1 <= digits <= depth <= exponent required")
    frame = local_frame(vector, q, e)
    s, modulus = q**(depth-digits), q**e
    upper = Matrix([[1, s], [0, 1]])
    projector = Matrix([[s, 0], [0, 0]])
    return tuple(mod(frame*a*inverse_mod(frame, modulus), modulus)
                 for a in (upper, projector))


def _answer(membership, matrix):
    answer = membership(matrix)
    if type(answer) is not bool:
        raise ValueError("exact boolean membership result required")
    return answer


def content_depth(q, e, membership):
    local_frame((1, 0), q, e)
    thresholds = []
    for row, col in ((0, 1), (1, 0)):
        outcomes = []
        for k in range(e+1):
            matrix = eye(2)
            matrix[row, col] = q**k
            outcomes.append(_answer(membership, mod(matrix, q**e)))
        if not outcomes[-1] or outcomes != sorted(outcomes):
            raise ValueError("nonmonotone membership thresholds")
        thresholds.append(outcomes.index(True))
    depth = max(thresholds)
    if (e-depth) % 2 or any(k and (depth-k) % 2 for k in thresholds):
        raise ValueError("invalid Smith-kernel threshold parities")
    return {"depth": depth, "content_exponent": (e-depth)//2,
            "thresholds": thresholds, "membership_calls": 2*(e+1)}


def local_direction(q, e, depth, membership, max_queries=4096):
    """Two SINGLE-factor containment probes per digit candidate, O(q*depth)."""
    local_frame((1, 0), q, e)
    if (type(depth) is not int or not 1 <= depth <= e
            or type(max_queries) is not int or max_queries < 0):
        raise ValueError("positive depth and nonnegative query budget required")
    bound = 2*(q*depth+1)
    if bound > max_queries:
        raise ValueError("digit search exceeds declared query budget")

    def accepted(vector, digits):
        outcomes = [_answer(membership, query)
                    for query in prefix_queries(vector, q, e, depth, digits)]
        return all(outcomes)

    winners = [v for v in [(z, 1) for z in range(q)]+[(1, 0)] if accepted(v, 1)]
    if len(winners) != 1:
        raise ValueError("membership violates unique direction promise")
    x, y = winners[0]
    affine, z = y == 1, x if y == 1 else y
    for digits in range(2, depth+1):
        winners = [t for t in (z+j*q**(digits-1) for j in range(q))
                   if accepted((t, 1) if affine else (1, t), digits)]
        if len(winners) != 1:
            raise ValueError("membership violates unique direction promise")
        z = winners[0]
    return {"vector": [z, 1] if affine else [1, z], "modulus": q**depth,
            "membership_calls": bound, "native_backend_verified": False}


def recover_local_data(n, factors, membership, max_queries=4096):
    """Caller supplies original-input membership, not labels on all cosets."""
    factors = checked_factors(n, factors)
    if type(max_queries) is not int or max_queries < 0:
        raise ValueError("nonnegative budget required")
    worst = sum(2*(e+1)+2*(q*e+1) for q, e in factors)
    if worst > max_queries:
        raise ValueError("worst-case protocol exceeds declared query budget")
    contents, directions, records = {}, {}, []
    for q, e in factors:
        local = lambda query: membership(embed_local(query, q, e, n, factors))
        info = content_depth(q, e, local)
        contents[q] = info["content_exponent"]
        direction = None
        if info["depth"]:
            direction = local_direction(q, e, info["depth"], local, max_queries)
            directions[q] = direction["vector"]
        records.append({"prime": q, "exponent": e, "content": info,
                        "direction": direction})
    return {"contents": contents, "directions": directions, "components": records,
            "membership_calls": sum(r["content"]["membership_calls"]+
                (r["direction"]["membership_calls"] if r["direction"] else 0)
                for r in records), "worst_case_calls": worst}
