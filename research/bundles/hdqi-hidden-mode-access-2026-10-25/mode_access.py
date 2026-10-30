"""Exact spectral-access certificates for native path-power Pauli Hamiltonians.

This computes classical certificates and conservative filter ledgers. It is
not a quantum compiler, a sampler, or an asymptotic advantage certificate.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt

import sympy as sp


X = sp.Symbol("x")


class Inconclusive(ValueError):
    """The finite precision budget did not certify the required promises."""


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, Q)):
        raise TypeError("exact int/Fraction inputs required")
    return Q(value)


def fraction(value):
    return Q(int(sp.numer(value)), int(sp.denom(value)))


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __post_init__(self):
        if self.lo > self.hi:
            raise ValueError("reversed interval")

    def __add__(self, other):
        return Interval(self.lo + other.lo, self.hi + other.hi)

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __mul__(self, other):
        values = [a*b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(values), max(values))

    def inverse(self):
        if self.lo <= 0 <= self.hi:
            raise Inconclusive("division interval contains zero")
        return Interval(1/self.hi, 1/self.lo)

    @property
    def width(self):
        return self.hi-self.lo

    @property
    def midpoint(self):
        return (self.lo+self.hi)/2


def point(value):
    return Interval(Q(value), Q(value))


def dyadic_enclosure(value, bits):
    scale = 1 << bits
    return Interval(Q((value.lo*scale).__floor__(), scale),
                    Q((value.hi*scale).__ceil__(), scale))


def sqrt_interval(value, bits):
    if value.lo < 0:
        raise Inconclusive("square-root interval is negative")
    scale = 1 << bits
    low = isqrt((value.lo.numerator * scale**2) // value.lo.denominator)
    high = isqrt((value.hi.numerator * scale**2) // value.hi.denominator)
    if Q(high, scale)**2 < value.hi:
        high += 1
    return Interval(Q(low, scale), Q(high, scale))


def evaluate(poly, value):
    total = point(0)
    for coefficient in poly.all_coeffs():
        total = total*value + point(fraction(coefficient))
    return total


def independence_polynomial(couplings, radius):
    """P(x)=sum_independent_S (-x)^|S| prod_{i in S} J_i^2."""
    polys = [sp.Poly(1, X, domain=sp.QQ)]
    for i, coupling in enumerate(couplings, start=1):
        j = rational(coupling)
        term = sp.Poly(sp.Rational(j.numerator, j.denominator)**2 * X, X)
        polys.append(polys[-1] - term * polys[max(0, i-radius-1)])
    return polys[-1]


def validate_input(couplings, radius, probe_size):
    couplings = tuple(rational(j) for j in couplings)
    if len(couplings) < 2 or any(not j or abs(j) > 1 for j in couplings):
        raise ValueError("need at least two nonzero couplings of magnitude <=1")
    if type(radius) is not int or not 1 <= radius < len(couplings):
        raise ValueError("radius must be in [1,m-1]")
    if type(probe_size) is not int or not 1 <= probe_size <= radius+1:
        raise ValueError("probe must be a nonempty prefix simplicial clique")
    return couplings


def spectral_intervals(couplings, radius, probe_size, bits):
    couplings = validate_input(couplings, radius, probe_size)
    poly = independence_polynomial(couplings, radius)
    residual = independence_polynomial(couplings[probe_size:], radius)
    energy_squared = sp.Poly.from_list(list(reversed(poly.all_coeffs())), X, domain=sp.QQ)
    residual_reciprocal = sp.Poly.from_list(list(reversed(residual.all_coeffs())), X, domain=sp.QQ)
    degree_drop = poly.degree()-residual.degree()
    if degree_drop not in (0, 1):
        raise ArithmeticError("removing a clique must drop independence number by at most one")
    roots = energy_squared.intervals(eps=sp.Rational(1, 1 << bits))
    if len(roots) != poly.degree() or any(mult != 1 for _, mult in roots):
        raise Inconclusive("simple real spectrum not certified")
    rows = []
    for (low, high), _ in roots:
        squared = Interval(fraction(low), fraction(high))
        if squared.lo <= 0:
            raise Inconclusive("positive energy not yet separated from zero")
        # Cancel reciprocal powers at a root before interval evaluation.
        denominator = evaluate(energy_squared.diff(), squared)
        if degree_drop == 0:
            denominator = squared * denominator
        weight_squared = dyadic_enclosure(
            evaluate(residual_reciprocal, squared) * denominator.inverse(), bits)
        if weight_squared.lo <= 0 or weight_squared.lo > 1:
            raise Inconclusive("positive probe weight not certified")
        rows.append({"energy": sqrt_interval(squared, bits),
                     "weight_squared": weight_squared,
                     "weight": sqrt_interval(weight_squared, bits)})
    zero_weight = (fraction(residual.LC()/poly.LC())
                   if residual.degree() == poly.degree() else Q(0))
    total = point(zero_weight)
    for row in rows:
        total += row["weight_squared"]
    if not 0 <= zero_weight <= 1 or not total.lo <= 1 <= total.hi:
        raise ArithmeticError("probe-weight normalization identity failed")
    return poly, residual, rows, zero_weight


def ceil(value):
    return -(-value.numerator // value.denominator)


def filter_ledger(rows, beta, error, norm_bound, bits):
    """Conservative pre-QSVT finite-time filter counts; not elementary gates."""
    alpha = len(rows)
    omitted, active, omission_squared, linear_bound = [], [], Q(0), Q(0)
    for i, row in enumerate(rows):
        cost = beta*row["energy"].hi/2
        if sqrt_interval(point(omission_squared+cost**2), bits).hi <= error/8:
            omitted.append(i)
            omission_squared += cost**2
            linear_bound += cost
        else:
            active.append(i)
    mode_error = error/(64*max(1, alpha))
    angle_error = beta*sum((rows[i]["energy"].width for i in active), Q(0))/4
    if angle_error > error/8:
        raise Inconclusive("energy precision insufficient for the thermal angles")
    budgets = []
    for i in active:
        row = rows[i]
        gaps = [2*row["energy"].lo]
        for j, other in enumerate(rows):
            if i != j:
                gaps.append(2*max(row["energy"].lo-other["energy"].hi,
                                  other["energy"].lo-row["energy"].hi))
        gap = min(gaps)
        weight = row["weight"].lo
        if gap <= 0 or weight <= 0:
            raise Inconclusive("frequency/probe separation needs more precision")
        time = ceil(32*(alpha+1)/(mode_error*weight*gap))
        steps = ceil(64*norm_bound*time/(mode_error*weight))
        if row["energy"].width > mode_error*weight/(32*time):
            raise Inconclusive("frequency precision insufficient for the filter time")
        budgets.append({"mode": i, "frequency_gap_lower": gap,
                        "probe_weight_lower": weight, "filter_time": time,
                        "midpoint_terms": steps,
                        "singular_value_lower": weight/4,
                        "polar_query_scale_not_gate_count": ceil(4/weight),
                        "frequency_error_bound": 4*time*row["energy"].width,
                        "window_error_bound": Q(4*(alpha+1), time)/gap,
                        "quadrature_error_bound": 8*norm_bound*time/steps})
    return {"active_modes": active, "omitted_modes": omitted,
            "omitted_squared_state_distance_upper": omission_squared,
            "omitted_state_distance_upper": sqrt_interval(point(omission_squared), bits).hi,
            "omitted_linear_state_distance_upper": linear_bound,
            "thermal_angle_error_upper": angle_error,
            "per_mode_unitary_error_target": mode_error, "filters": budgets}


def certify(couplings, radius, probe_size, *, beta=Q(1), error=Q(1, 100),
            initial_bits=32, max_bits=512):
    couplings = validate_input(couplings, radius, probe_size)
    beta, error = rational(beta), rational(error)
    if beta < 0 or not 0 < error <= Q(1, 4):
        raise ValueError("need beta>=0 and 0<error<=1/4")
    if type(initial_bits) is not int or type(max_bits) is not int or not 8 <= initial_bits <= max_bits:
        raise ValueError("invalid precision budget")
    bits = initial_bits
    while True:
        try:
            poly, residual, rows, zero = spectral_intervals(couplings, radius, probe_size, bits)
            ledger = filter_ledger(rows, beta, error, sum(map(abs, couplings)), bits)
            return {"couplings": couplings, "radius": radius, "probe_size": probe_size,
                    "beta": beta, "error": error, "precision_bits": bits,
                    "independence_coefficients_high_first": tuple(map(fraction, poly.all_coeffs())),
                    "residual_coefficients_high_first": tuple(map(fraction, residual.all_coeffs())),
                    "zero_mode_weight_squared": zero, "modes": rows, **ledger,
                    "native_input": "canonical independent path-power Pauli Hamiltonian",
                    "quantum_circuit_compiled": False, "quantum_advantage_claim": False,
                    "uniform_polynomial_parameter_bound_proved": False,
                    "normalization_and_root_separation_are_charged": True}
        except Inconclusive:
            if bits == max_bits:
                raise
            bits = min(2*bits, max_bits)
