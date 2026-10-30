"""Exact certificates, NOT a theta/isogeny backend.

Matrices live in Z[h]/(h^2-T*h+1). SymPy supplies finite four-square
witnesses, not a proof of polynomial runtime for its implementation.
"""

from dataclasses import dataclass
from math import gcd, isqrt


def _integer(x, name, minimum=0):
    if type(x) is not int or x < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


@dataclass(frozen=True)
class Quadratic:
    """u + v*h, with h^2 = trace*h - 1."""

    trace: int
    u: int = 0
    v: int = 0

    def __post_init__(self):
        _integer(self.trace, "trace", 3)
        if type(self.u) is not int or type(self.v) is not int:
            raise ValueError("coefficients must be integers")

    def _coerce(self, other):
        if type(other) is int:
            return Quadratic(self.trace, other)
        if not isinstance(other, Quadratic) or other.trace != self.trace:
            raise ValueError("incompatible quadratic rings")
        return other

    def __add__(self, other):
        other = self._coerce(other)
        return Quadratic(self.trace, self.u+other.u, self.v+other.v)

    __radd__ = __add__

    def __neg__(self):
        return Quadratic(self.trace, -self.u, -self.v)

    def __sub__(self, other):
        return self + (-self._coerce(other))

    def __mul__(self, other):
        other = self._coerce(other)
        return Quadratic(self.trace, self.u*other.u-self.v*other.v,
                         self.u*other.v+self.v*other.u+self.trace*self.v*other.v)

    __rmul__ = __mul__


def transpose(a):
    return tuple(zip(*a))


def matmul(a, b):
    if not a or not b or any(len(row) != len(b) for row in a):
        raise ValueError("incompatible matrix dimensions")
    if any(len(row) != len(b[0]) for row in b):
        raise ValueError("ragged matrix")
    return tuple(tuple(sum(x*y for x, y in zip(row, col)) for col in zip(*b)) for row in a)


def _qconj(a):
    return (a[0], -a[1], -a[2], -a[3])


def _qmul(a, b):
    w, x, y, z = a
    s, t, u, v = b
    return (w*s-x*t-y*u-z*v, w*t+x*s+y*v-z*u,
            w*u-x*v+y*s+z*t, w*v+x*u-y*t+z*s)


def _octmul(left, right):
    # Cayley-Dickson: (a,b)(c,d)=(ac-conj(d)b, da+b conj(c)).
    a, b, c, d = left[:4], left[4:], right[:4], right[4:]
    ac, db = _qmul(a, c), _qmul(_qconj(d), b)
    da, bc = _qmul(d, a), _qmul(b, _qconj(c))
    return tuple(x-y for x, y in zip(ac, db)) + tuple(x+y for x, y in zip(da, bc))


def norm_matrix(coefficients):
    """Left octonion multiplication: C^t C = sum(coefficients^2) I_8."""
    if len(coefficients) != 8:
        raise ValueError("eight commuting coefficients required")
    columns = [_octmul(coefficients, tuple(int(i == j) for i in range(8))) for j in range(8)]
    return transpose(columns)


def coin_witness(trace, denominator):
    """Find X,Y >= 0 with (T+2)X+(T-2)Y=D^2, without factoring T+-2."""
    _integer(trace, "trace", 3)
    _integer(denominator, "denominator", 2)
    if denominator % 2 or denominator*denominator < (trace+2)*(trace-2):
        raise ValueError("an even denominator with D^2 >= T^2-4 is required")
    divisor = gcd(trace+2, trace-2)
    a, b, target = (trace+2)//divisor, (trace-2)//divisor, denominator**2//divisor
    x = 0 if b == 1 else (target * pow(a, -1, b)) % b
    y = (target-a*x)//b
    assert x >= 0 and y >= 0 and (trace+2)*x + (trace-2)*y == denominator**2
    return x, y


def _four_square_witness(value):
    from sympy.solvers.diophantine.diophantine import sum_of_four_squares
    result = tuple(int(x) for x in sum_of_four_squares(value))
    if len(result) != 4 or sum(x*x for x in result) != value:
        raise ValueError("invalid four-square witness")
    return result


def certificate(trace, denominator):
    x, y = coin_witness(trace, denominator)
    roots_x, roots_y = _four_square_witness(x), _four_square_witness(y)
    one, h = Quadratic(trace, 1), Quadratic(trace, 0, 1)
    hinverse = Quadratic(trace, trace, -1)
    coefficients = tuple(a*(one+h) for a in roots_x) + tuple(b*(one-h) for b in roots_y)
    c = norm_matrix(coefficients)
    e = tuple(tuple(hinverse*z for z in row) for row in transpose(c))
    return {"trace": trace, "denominator": denominator, "coin_x": x, "coin_y": y,
            "four_squares_x": roots_x, "four_squares_y": roots_y, "C": c, "E": e}


def verify_certificate(record):
    """Check both adjoint identities, inverse transport, and witness arithmetic."""
    t, d = record["trace"], record["denominator"]
    one, zero, h = Quadratic(t, 1), Quadratic(t), Quadratic(t, 0, 1)
    identity = tuple(tuple(one if i == j else zero for j in range(8)) for i in range(8))
    scaled = lambda s: tuple(tuple(s*z for z in row) for row in identity)
    c, e = record["C"], record["E"]
    he = tuple(tuple(h*z for z in row) for row in e)
    return {
        "coin_identity": (t+2)*record["coin_x"]+(t-2)*record["coin_y"] == d*d,
        "four_square_witnesses": all(sum(a*a for a in record[name]) == record[coin]
                                    for name, coin in (("four_squares_x", "coin_x"),
                                                       ("four_squares_y", "coin_y"))),
        "C_adjoint_C": matmul(transpose(c), c) == scaled(d*d*h),
        "C_C_adjoint": matmul(c, transpose(c)) == scaled(d*d*h),
        "E_adjoint_H_E": matmul(transpose(e), he) == scaled(d*d*one),
        "E_C": matmul(e, c) == scaled(d*d*one),
        "C_E": matmul(c, e) == scaled(d*d*one),
    }


def evaluate(matrix, h):
    """Evaluate at an exact integer matrix, not geometric torsion points."""
    n = len(h)
    if not n or any(len(row) != n for row in h):
        raise ValueError("H must be square and nonempty")
    if any(type(x) is not int for row in h for x in row):
        raise ValueError("integer matrices only")
    trace = matrix[0][0].trace
    h2 = matmul(h, h)
    if any(h2[i][j]-trace*h[i][j]+int(i == j) for i in range(n) for j in range(n)):
        raise ValueError("H fails the quadratic identity")
    return tuple(tuple(matrix[i//n][j//n].u*int(i % n == j % n)
                       + matrix[i//n][j//n].v*h[i % n][j % n]
                       for j in range(len(matrix[0])*n)) for i in range(len(matrix)*n))


def _prime(n):
    return n >= 2 and all(n % k for k in range(2, isqrt(n)+1))


def resource_plan(trace_bound, ell, characteristic):
    """Uniform squarefree D and disjoint marks; ell, characteristic promised prime.

    This performs no point generation or large-input primality testing.
    """
    _integer(trace_bound, "trace_bound", 3)
    _integer(ell, "ell", 3)
    _integer(characteristic, "characteristic", 3)
    if ell % 2 == 0 or characteristic % 2 == 0 or gcd(ell, characteristic) != 1:
        raise ValueError("distinct coprime odd prime promises required")
    denominator, primes, r = 2, [2], 3
    while denominator <= trace_bound+2:
        if _prime(r) and gcd(r, ell*characteristic) == 1:
            primes.append(r)
            denominator *= r
        r += 2
    marks, marking_product = [], 1
    threshold = 8*16**3*ell**2
    while marking_product**2 <= threshold:
        if _prime(r) and gcd(r, ell*characteristic*denominator) == 1:
            marks.append(r)
            marking_product *= r
        r += 2
    return {"trace_bound": trace_bound, "denominator": denominator,
            "denominator_primes": primes, "quotient_multiplier": denominator**2,
            "weak_evaluation_orders": [r*r for r in primes],
            "marking_primes": marks, "marking_product": marking_product,
            "projective_bound_squared": threshold, "original_dimension": 2,
            "stabilized_dimension": 16, "large_prime_inputs_primality": "promised_not_tested",
            "geometric_backend_executed": False, "kernel_recovered": False,
            "quantum_speedup_admitted": False}
