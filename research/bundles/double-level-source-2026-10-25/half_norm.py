"""Integral certificates in Z[A], A=(H-I)/2, conditional on actual divisibility."""

from dataclasses import dataclass
import sys

from double_level_source import ROOT

sys.path.insert(0, str(ROOT / "smooth-repolarization-2026-10-23"))
from smooth_repolarization import _four_square_witness, matmul, norm_matrix, transpose


@dataclass(frozen=True)
class HalfQuadratic:
    """u+v*A where A^2=2*s*A+s. This includes the boundary s=0."""

    s: int
    u: int = 0
    v: int = 0

    def __post_init__(self):
        if type(self.s) is not int or self.s < 0 or type(self.u) is not int or type(self.v) is not int:
            raise ValueError("nonnegative integer s and integral coefficients required")

    def _coerce(self, other):
        if type(other) is int:
            return HalfQuadratic(self.s, other)
        if not isinstance(other, HalfQuadratic) or other.s != self.s:
            raise ValueError("incompatible half-norm rings")
        return other

    def __add__(self, other):
        other = self._coerce(other)
        return HalfQuadratic(self.s, self.u+other.u, self.v+other.v)

    __radd__ = __add__

    def __neg__(self):
        return HalfQuadratic(self.s, -self.u, -self.v)

    def __sub__(self, other):
        return self+(-self._coerce(other))

    def __mul__(self, other):
        other = self._coerce(other)
        return HalfQuadratic(self.s, self.u*other.u+self.s*self.v*other.v,
                             self.u*other.v+self.v*other.u+2*self.s*self.v*other.v)

    __rmul__ = __mul__


def half_certificate(trace, multiplier):
    if type(trace) is not int or trace < 2 or trace % 4 != 2:
        raise ValueError("trace >= 2 congruent to 2 modulo4 required")
    s = (trace-2)//4
    if type(multiplier) is not int or multiplier < 1 or multiplier % 2 != 1 or multiplier < s*(s+1):
        raise ValueError("positive odd multiplier at least s(s+1) required")
    x = multiplier % s if s else multiplier
    y = (multiplier-(s+1)*x)//s if s else 0
    if min(x, y) < 0 or (s+1)*x+s*y != multiplier:
        raise ArithmeticError("half-norm coin identity failed")
    rx, ry = _four_square_witness(x), _four_square_witness(y)
    a, one = HalfQuadratic(s, 0, 1), HalfQuadratic(s, 1)
    c = norm_matrix(tuple(r*(a+one) for r in rx)+tuple(r*a for r in ry))
    inverse_h = HalfQuadratic(s, trace-1, -2)
    f = tuple(tuple(inverse_h*z for z in row) for row in transpose(c))
    return {"trace": trace, "multiplier": multiplier, "coin_x": x, "coin_y": y,
            "four_squares_x": rx, "four_squares_y": ry, "C": c, "F": f}


def verify_half_certificate(record):
    t, d = record["trace"], record["multiplier"]
    if type(t) is not int or t < 2 or t % 4 != 2:
        raise ValueError("invalid half-norm trace")
    s = (t-2)//4
    one, zero, h = HalfQuadratic(s, 1), HalfQuadratic(s), HalfQuadratic(s, 1, 2)
    diagonal = lambda x: tuple(tuple(x if i == j else zero for j in range(8)) for i in range(8))
    c, f = record["C"], record["F"]
    hf = tuple(tuple(h*z for z in row) for row in f)
    return {
        "coin": (s+1)*record["coin_x"]+s*record["coin_y"] == d,
        "four_squares": all(sum(x*x for x in record[key]) == record[value]
                            for key, value in (("four_squares_x", "coin_x"),
                                               ("four_squares_y", "coin_y"))),
        "C_star_C": matmul(transpose(c), c) == diagonal(d*h),
        "C_C_star": matmul(c, transpose(c)) == diagonal(d*h),
        "F_star_H_F": matmul(transpose(f), hf) == diagonal(d*one),
        "F_C": matmul(f, c) == diagonal(d*one),
        "C_F": matmul(c, f) == diagonal(d*one),
    }
