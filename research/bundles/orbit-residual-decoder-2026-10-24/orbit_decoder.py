"""Single-polynomial orbit decoding and exact finite success ledgers.

The Prony core adapts the existing prime_character_interleaved_probe algorithm
to the actual public orbit nodes. No source label enters decode(). Reference
field/table caps are computational limits, not quantum complexity claims.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from math import comb, isqrt

from flint import fmpz, nmod_mat


def integer(value, name, lo, hi):
    if type(value) is not int or not lo <= value <= hi:
        raise ValueError(f"{name} must be an integer in [{lo},{hi}]")
    return value


@lru_cache(maxsize=32)
def field(p):
    integer(p, "reference field", 3, 65537)
    if not fmpz(p).is_prime():
        raise ValueError("odd prime field required")
    return p


@dataclass(frozen=True)
class Geometry:
    p: int
    width: int
    root: int
    representatives: tuple[int, ...]
    row_length: int

    def __post_init__(self):
        field(self.p)
        integer(self.width, "orbit width", 2, 16)
        integer(self.root, "root", 1, self.p-1)
        if (pow(self.root, self.width, self.p) != 1
                or any(pow(self.root, j, self.p) == 1 for j in range(1, self.width))):
            raise ValueError("root must have exactly the declared order")
        if type(self.representatives) is not tuple or not self.representatives:
            raise ValueError("explicit nonempty orbit representatives required")
        for a in self.representatives:
            integer(a, "representative", 1, self.p-1)
        points = [a*pow(self.root, j, self.p) % self.p
                  for a in self.representatives for j in range(self.width)]
        if len(set(points)) != len(points):
            raise ValueError("public orbits must be disjoint")
        integer(self.row_length, "syndromes per row", 2, len(self.representatives))

    @property
    def dimension(self):
        return self.width*self.row_length

    @property
    def nodes(self):
        return tuple(pow(a, self.width, self.p) for a in self.representatives)

    @property
    def points(self):
        return tuple(tuple(a*pow(self.root, j, self.p) % self.p for j in range(self.width))
                     for a in self.representatives)


def geometry(p, width, row_length):
    field(p)
    integer(width, "width", 2, 16)
    if (p-1) % width:
        raise ValueError("orbit width must divide p-1")
    root = next((x for x in range(2, p) if pow(x, width, p) == 1
                 and all(pow(x, j, p) != 1 for j in range(1, width))), None)
    if root is None:
        raise ArithmeticError("root not found")
    unseen, representatives = set(range(1, p)), []
    while unseen:
        a = min(unseen)
        representatives.append(a)
        unseen.difference_update(a*pow(root, j, p) % p for j in range(width))
    return Geometry(p, width, root, tuple(representatives), row_length)


def canonical(rows, width, length, p):
    if len(rows) != width or any(len(row) != length for row in rows):
        raise ValueError("matrix dimensions disagree with public geometry")
    if any(type(x) is not int or not 0 <= x < p for row in rows for x in row):
        raise ValueError("canonical field entries required")


def fold(g, errors):
    canonical(errors, len(g.representatives), g.width, g.p)
    return [[pow(a, h, g.p)*sum(row[j]*pow(g.root, j*h, g.p)
                               for j in range(g.width)) % g.p
             for a, row in zip(g.representatives, errors)] for h in range(g.width)]


def syndrome(g, errors):
    folded = fold(g, errors)
    return [[sum(e*pow(z, j, g.p) for e, z in zip(row, g.nodes)) % g.p
             for j in range(g.row_length)] for row in folded]


def cap_rank(g, cap, rows):
    integer(cap, "cap", 1, g.row_length-1)
    canonical(rows, g.width, g.row_length, g.p)
    matrix = [[s[j+k] for k in range(cap)] for s in rows
              for j in range(g.row_length-cap)]
    return nmod_mat(matrix, g.p).rank()


def decode(g, cap, rows):
    """Whole-cap Prony certificate, based only on public geometry/syndromes."""
    d = cap_rank(g, cap, rows)
    common = {"cap": cap, "cap_rank": d, "extra_quantum_copies": 0,
              "output_polynomials": 1, "source_error_or_support_supplied": False}
    if d == 0 and all(not any(s) for s in rows):
        return {**common, "status": "VERIFIED_UNIQUE", "locator": [1],
                "errors": [[0]*g.width for _ in g.representatives], "support": []}
    if not 1 <= d <= cap:
        return {**common, "status": "ABSTAIN_RANK"}
    matrix = [[s[j+k] for k in range(d)] for s in rows for j in range(g.row_length-d)]
    if nmod_mat(matrix, g.p).rank() != d:
        return {**common, "status": "ABSTAIN_LOCATOR_RANK"}
    rhs = [(-s[j+d]) % g.p for s in rows for j in range(g.row_length-d)]
    reduced, rank = nmod_mat([row+[b] for row, b in zip(matrix, rhs)], g.p).rref()
    if rank != d:
        return {**common, "status": "ABSTAIN_INCONSISTENT"}
    locator = [int(reduced[i, d]) for i in range(d)]+[1]
    support = [i for i, z in enumerate(g.nodes)
               if sum(value*pow(z, j, g.p) for j, value in enumerate(locator)) % g.p == 0]
    if len(support) != d:
        return {**common, "status": "ABSTAIN_PUBLIC_ROOTS", "locator": locator}
    vandermonde = nmod_mat([[pow(g.nodes[i], j, g.p) for i in support] for j in range(d)], g.p)
    values = vandermonde.solve(nmod_mat([[s[j] for s in rows] for j in range(d)], g.p))
    errors = [[0]*g.width for _ in g.representatives]
    inverse_width = pow(g.width, -1, g.p)
    for column, i in enumerate(support):
        a = g.representatives[i]
        for j in range(g.width):
            errors[i][j] = inverse_width*sum(
                int(values[column, h])*pow(a, -h, g.p)*pow(g.root, -j*h, g.p)
                for h in range(g.width)) % g.p
    if syndrome(g, errors) != rows:
        return {**common, "status": "ABSTAIN_FULL_REPLAY"}
    return {**common, "status": "VERIFIED_UNIQUE", "locator": locator,
            "support": support, "errors": errors}


def rank_failure_bound(p, width, dimension, degree, cap, *, exact=True):
    field(p)
    integer(width, "width", 2, 16)
    integer(dimension, "dimension", 2*width, p-1)
    if dimension % width:
        raise ValueError("dimension must split into whole syndrome rows")
    integer(cap, "cap", 1, dimension//width-1)
    integer(degree, "degree", 0, cap)
    equations = dimension-width*cap
    if equations < degree:
        raise ValueError("not enough cap equations for the claimed source shells")
    if degree == 0:
        return F(0)
    if not exact:
        return min(F(1), F((p+1)**degree, (p-1)*p**equations))
    integer(degree, "exact projective-sum degree", 0, 256)
    bound = F(0)
    for t in range(1, degree+1):
        free_rank = min(equations, (width-1)*t)
        compatible_dimension = t-min(equations, width*t)+free_rank
        bound += F(comb(degree, t)*(p**compatible_dimension-1),
                   (p-1)*p**free_rank)
    return min(F(1), bound)


def upward(value, bits=256):
    value = F(value)
    scale = 1 << bits
    return F(-(-value.numerator*scale//value.denominator), scale)


def sqrt_upper(value, bits=256):
    value = F(value)
    if value < 0:
        raise ValueError("nonnegative radicand required")
    scale = 1 << bits
    lo = isqrt(value.numerator*scale*scale//value.denominator)
    return F(lo if lo*lo*value.denominator == value.numerator*scale*scale else lo+1, scale)


def binomial_tail(trials, probability, cutoff):
    integer(trials, "trials", 1, 8192)
    integer(cutoff, "cutoff", 0, trials)
    if not isinstance(probability, F) or not 0 < probability < 1:
        raise ValueError("exact probability in (0,1) required")
    a, d = probability.numerator, probability.denominator
    b = d-a
    term, total = b**trials, 0
    for j in range(trials+1):
        if j > cutoff:
            total += term
        if j < trials:
            numerator, divisor = term*(trials-j)*a, (j+1)*b
            term, remainder = divmod(numerator, divisor)
            if remainder:
                raise ArithmeticError("integer binomial recurrence failed")
    return F(total, d**trials)


def perfect_search_certificate(p=12289, M=4096, dimension=9828, degree=2375, width=3):
    field(p)
    integer(width, "width", 2, 16)
    integer(M, "number of predicates", 1, 8192)
    if (p-1) % width or not 1 <= M <= (p-1)//width or dimension > width*M:
        raise ValueError("not a valid public orbit family")
    cap = degree+1
    failure = rank_failure_bound(p, width, dimension, degree, cap, exact=False)
    tail = binomial_tail(M, F(p+1, 2*p), degree)
    # Include the failed degree-truncation preparation, not just its
    # conditioned state's error. Neither herald is retried for free.
    loss = min(F(1), tail+M*(failure+sqrt_upper(tail)+sqrt_upper(failure)))
    return {"p": p, "M": M, "width": width, "dimension": dimension,
            "rate": str(F(dimension, width*M)), "degree": degree, "guard_cap": cap,
            "cap_equations": dimension-width*cap,
            "rank_failure_upper_dyadic": str(upward(failure)),
            "discarded_source_mass_upper_dyadic": str(upward(tail)),
            "one_attempt_perfect_failure_upper_dyadic": str(upward(loss)),
            "input_halfsets": "every_explicit_halfset_of_size_(p-1)/2",
            "nondegenerate_quadratic_form_required": True,
            "source_truncation_preparation_success_lower": str(1-upward(tail)),
            "quantum_circuit_executed": False, "native_witness_produced": False,
            "gate_error_budget": "must_subtract_full_circuit_TV_from_success",
            "classical_separation_or_novelty_claimed": False}


def isotropic_ternary(p, coefficients):
    """Paid O(p) local classical flat witness, not a global codeword solver."""
    field(p)
    if len(coefficients) != 3:
        raise ValueError("three quadratic coefficients required")
    for x in coefficients:
        integer(x, "nonzero coefficient", 1, p-1)
    a, b, c = coefficients
    squares = {a*x*x % p: x for x in range(p)}
    for y in range(p):
        target = (-c-b*y*y) % p
        if target in squares:
            return (squares[target], y, 1)
    raise ArithmeticError("two sets larger than half the field failed to intersect")
