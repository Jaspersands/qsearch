"""Exact rational access and analytic ledgers for the line-graph flux chain.

The all-size gap is a LOCAL UNREVIEWED deduction in FLUX_GAP.md. This file
does not compile or execute a quantum circuit. No sector enumeration occurs.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import random
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hdqi-fermion-sampler-2026-10-24"))
from fermion_sampler import Root, coin, determinant, root


def rational(x):
    if isinstance(x, bool) or not isinstance(x, (int, F)):
        raise ValueError("native values must be exact integers or Fractions, not floats")
    return F(x)


def ceil_fraction(x):
    return -(-x.numerator // x.denominator)


def ceil_log2(x):
    if x <= 1:
        return 0
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    return k if F(1 << k) >= x else k + 1


@dataclass(frozen=True)
class Interval:
    lo: F
    hi: F

    def __post_init__(self):
        if not isinstance(self.lo, F) or not isinstance(self.hi, F) or self.lo > self.hi:
            raise ValueError("invalid exact interval")

    @property
    def width(self):
        return self.hi - self.lo

    @property
    def midpoint(self):
        return (self.lo + self.hi) / 2


def outward(interval, tolerance):
    bits = ceil_log2(8 / tolerance)
    denominator = 1 << bits
    lo = (interval.lo * denominator).__floor__()
    hi = ceil_fraction(interval.hi * denominator)
    return Interval(F(lo, denominator), F(hi, denominator))


def _atan_interval(x, tolerance):
    total, term, k = F(0), x, 0
    while True:
        total += (-1 if k % 2 else 1) * term / (2 * k + 1)
        k += 1
        term *= x * x
        error = term / (2 * k + 1)
        if error <= tolerance / 4:
            other = total + (-1 if k % 2 else 1) * error
            return outward(Interval(min(total, other), max(total, other)), tolerance)


@lru_cache(maxsize=64)
def pi_interval(tolerance):
    tolerance = rational(tolerance)
    if not 0 < tolerance <= 1:
        raise ValueError("need 0 < pi tolerance <= 1")
    a = _atan_interval(F(1, 5), tolerance / 64)
    b = _atan_interval(F(1, 239), tolerance / 64)
    result = outward(Interval(16 * a.lo - 4 * b.hi, 16 * a.hi - 4 * b.lo),
                     tolerance)
    assert result.width <= tolerance and 3 < result.lo < result.hi < 4
    return result


def _twice_atanh(q, tolerance):
    total, power, k = F(0), q, 0
    while True:
        total += 2 * power / (2 * k + 1)
        k += 1
        power *= q * q
        tail = 2 * power / ((2 * k + 1) * (1 - q * q))
        if tail <= tolerance / 4:
            return outward(Interval(total, total + tail), tolerance)


def log_interval(x, tolerance):
    x, tolerance = rational(x), rational(tolerance)
    if x <= 0 or not 0 < tolerance <= 1:
        raise ValueError("log needs x>0 and 0<tolerance<=1")
    k = x.numerator.bit_length() - x.denominator.bit_length()
    power = F(2) ** k
    if x < power:
        k -= 1
        power /= 2
    mantissa = x / power
    assert 1 <= mantissa < 2
    base = _twice_atanh(F(1, 3), tolerance / (8 * (abs(k) + 1)))
    part = _twice_atanh((mantissa - 1) / (mantissa + 1), tolerance / 8)
    endpoints = (k * base.lo, k * base.hi)
    result = outward(Interval(min(endpoints) + part.lo,
                             max(endpoints) + part.hi), tolerance)
    assert result.width <= tolerance
    return result


def exp_interval(x, tolerance):
    x, tolerance = rational(x), rational(tolerance)
    if abs(x) > 1 or not 0 < tolerance <= 1:
        raise ValueError("certified exponential is scoped to |x|<=1")
    if x < 0:
        positive = exp_interval(-x, tolerance / 4)
        return outward(Interval(1 / positive.hi, 1 / positive.lo), tolerance)
    total, term, k = F(1), F(1), 0
    while True:
        k += 1
        term *= x / k
        total += term
        tail = term * x / (k + 1) / (1 - x / (k + 2))
        if tail <= tolerance / 4:
            result = outward(Interval(total, total + tail), tolerance)
            assert result.width <= tolerance
            return result


@dataclass(frozen=True)
class Source:
    topology: Root
    couplings: tuple[F, ...]

    @property
    def r(self):
        return self.topology.cycle_rank

    @property
    def mass(self):
        return sum((j * j for j in self.couplings), F(0))

    @property
    def l1(self):
        return sum(map(abs, self.couplings), F(0))

    @property
    def chord_degree(self):
        degrees = [0] * self.topology.n
        for e in self.topology.chords:
            for u in self.topology.edges[e]:
                degrees[u] += 1
        return max(degrees)


def source(n, edges, couplings=None):
    edges = tuple(edges)
    js = tuple(F(1) for _ in edges) if couplings is None else tuple(map(rational, couplings))
    if len(js) != len(edges) or any(abs(j) > 1 for j in js):
        raise ValueError("need one exact coupling with |J|<=1 per edge")
    # The old object is used only for combinatorics; exact access uses js below.
    return Source(root(n, edges, [float(j) for j in js]), js)


def _check_flux(src, flux):
    if isinstance(flux, bool) or not isinstance(flux, int) or not 0 <= flux < 1 << src.r:
        raise ValueError("invalid flux label")


def skew(src, flux):
    _check_flux(src, flux)
    a = [[F(0) for _ in range(src.topology.n)] for _ in range(src.topology.n)]
    chord_index = {e: i for i, e in enumerate(src.topology.chords)}
    for e, ((u, v), j) in enumerate(zip(src.topology.edges, src.couplings)):
        if e in chord_index and (flux >> chord_index[e]) & 1:
            j = -j
        a[u][v], a[v][u] = j, -j
    return a


def gap_certificate(src, beta):
    beta = rational(beta)
    if beta < 0:
        raise ValueError("beta must be nonnegative")
    if src.r == 0:
        return {"status": "NO_FLUX_BITS", "cycle_rank": 0, "chord_degree": 0,
                "influence_upper": F(0), "gap_lower": None}
    kappa = 3 * src.chord_degree * beta * beta
    eligible = beta <= F(1, 8) and kappa < 1
    return {"status": "LOCAL_PROOF_BOUND" if eligible else "INCONCLUSIVE",
            "cycle_rank": src.r, "chord_degree": src.chord_degree,
            "influence_upper": kappa if eligible else None,
            "gap_lower": (1 - kappa) / src.r if eligible else None}


def log_partition(src, beta, flux, tolerance=F(1, 1024), max_terms=10000):
    """Certified log Z from rational determinants, Machin pi and cosh product.

    Tail length is charged explicitly. A cap failure returns no interval.
    """
    beta, tolerance = rational(beta), rational(tolerance)
    _check_flux(src, flux)
    if beta < 0 or not 0 < tolerance <= 1:
        raise ValueError("invalid beta or tolerance")
    if isinstance(max_terms, bool) or not isinstance(max_terms, int) or max_terms < 1:
        raise ValueError("need a positive explicit determinant-work cap")
    energy = src.mass * beta * beta
    if not energy:
        return {"interval": Interval(F(0), F(0)), "terms": 0,
                "determinant_dimension": src.topology.n}
    count = max(1, ceil_fraction(8 * energy / (9 * tolerance)))
    if count > max_terms:
        raise RuntimeError(f"INCONCLUSIVE: {count} determinants exceed cap {max_terms}")
    pi = pi_interval(tolerance / (16 * max(F(1), energy)))
    a = skew(src, flux)
    lo = hi = F(0)
    for k in range(count):
        t = 2 * beta / ((2 * k + 1) * pi.midpoint)
        value = determinant([[F(i == j) + t * a[i][j]
                              for j in range(len(a))] for i in range(len(a))])
        assert value >= 1
        part = log_interval(value, tolerance / (8 * count))
        lo, hi = lo + part.lo, hi + part.hi
    pi_error = energy * pi.width
    tail = 2 * energy / (9 * (2 * count - 1))
    result = Interval(max(F(0), lo - pi_error), hi + pi_error + tail)
    assert result.width <= tolerance
    return {"interval": result, "terms": count, "determinant_dimension": len(a)}


def conditional(src, beta, flux, bit, tolerance=F(1, 128), max_terms=10000):
    """Certified probability that chord bit is ONE, independent of its old value."""
    beta, tolerance = rational(beta), rational(tolerance)
    _check_flux(src, flux)
    if (isinstance(bit, bool) or not isinstance(bit, int) or not 0 <= bit < src.r
            or not 0 <= beta <= F(1, 8) or not 0 < tolerance <= F(1, 2)):
        raise ValueError("invalid conditional query or temperature")
    zero, one = flux & ~(1 << bit), flux | (1 << bit)
    f0 = log_partition(src, beta, zero, tolerance / 8, max_terms)
    f1 = log_partition(src, beta, one, tolerance / 8, max_terms)
    bound = 2 * beta * abs(src.couplings[src.topology.chords[bit]])
    low = max(-bound, f1["interval"].lo - f0["interval"].hi)
    high = min(bound, f1["interval"].hi - f0["interval"].lo)
    if low > high:
        raise ArithmeticError("certified physical log-odds bound contradicted")
    e0 = exp_interval(low, tolerance / 16)
    e1 = exp_interval(high, tolerance / 16)
    result = Interval(e0.lo / (1 + e0.lo), e1.hi / (1 + e1.hi))
    assert result.width <= tolerance and 0 < result.lo <= result.hi < 1
    return {"interval": result, "terms": f0["terms"] + f1["terms"],
            "native_probability_enclosed": True}


def sample_flux(src, beta, epsilon=F(1, 4), seed=None, max_terms=10000):
    """Approximate NATIVE classical flux sampling with a proved TV ledger.

    This is not coherent preparation and not sampling the final pilot word.
    """
    epsilon = rational(epsilon)
    if not 0 < epsilon < 1:
        raise ValueError("need 0<epsilon<1")
    cert = gap_certificate(src, beta)
    if cert["status"] == "NO_FLUX_BITS":
        return {"flux": 0, "steps": 0, "determinants": 0, "tv_bound": F(0)}
    if cert["status"] != "LOCAL_PROOF_BOUND":
        raise ValueError("no admitted mixing bound for this temperature")
    steps = ceil_fraction(F(ceil_log2(2 * src.r / epsilon)) / cert["gap_lower"])
    per_step = epsilon / (2 * steps)
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    flux, work = 0, 0
    for _ in range(steps):
        bit = rng.randrange(src.r)
        access = conditional(src, beta, flux, bit, per_step, max_terms)
        take = coin(access["interval"].midpoint, rng)
        flux = (flux | (1 << bit)) if take else (flux & ~(1 << bit))
        work += access["terms"]
    return {"flux": flux, "steps": steps, "determinants": work,
            "ideal_mixing_tv_bound": epsilon / 2,
            "numerical_tv_bound": steps * per_step,
            "tv_bound": epsilon, "native_conditional_access": True,
            "tv_bound_assumes_independent_random_bits": True,
            "seeded_reproducibility_control": seed is not None}


def coherent_ledger(src, beta, epsilon=F(1, 10)):
    beta, epsilon = rational(beta), rational(epsilon)
    if not 0 < epsilon < 1:
        raise ValueError("need 0<epsilon<1")
    cert = gap_certificate(src, beta)
    if cert["status"] != "LOCAL_PROOF_BOUND":
        return {"status": cert["status"], "quantum_execution": False}
    g = cert["gap_lower"]
    a = beta * src.l1 / 2
    b = beta * beta * (src.mass / 2 + src.l1 ** 2)
    adiabatic = (2 * a + b) / g ** 2 + 7 * a * a / g ** 3
    time = max(1, ceil_fraction(4 * adiabatic / epsilon))
    steps = ceil_fraction(16 * (time * time + time * a + 1) / epsilon)
    rotations = steps * src.r
    rotation_error = epsilon / (32 * rotations)
    conditional_tolerance = rotation_error / 16
    # conditional() requests each of its two log-partitions at tolerance/8.
    terms = (max(1, ceil_fraction(64 * src.mass * beta * beta
                                 / (9 * conditional_tolerance)))
             if src.mass * beta * beta else 0)
    return {"status": "LOCAL_IDEAL_POLYNOMIAL_CONSTRUCTION", "gap_lower": g,
            "first_derivative_bound": a, "second_derivative_bound": b,
            "adiabatic_error_coefficient": adiabatic, "evolution_time_upper": time,
            "first_order_product_steps": steps, "conditional_rotations": rotations,
            "rotation_error_budget": rotation_error,
            "conditional_interval_tolerance": conditional_tolerance,
            "determinants_per_rotation": 2 * terms,
            "determinant_dimension": src.topology.n,
            "total_determinants_upper": 2 * terms * rotations,
            "determinants_are_not_elementary_gate_counts": True,
            "polynomial_parameters": ["input_size", "1/epsilon", "1/(1-kappa)"],
            "polynomial_in_input_requires_inverse_polynomial_gap_slack": True,
            "exponential_flux_table_required": False, "quantum_execution": False,
            "compiled_gaussian_stage": False, "independent_review": False}
