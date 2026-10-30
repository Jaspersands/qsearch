"""Exact controls for a copy-only conjugation-symmetry obstruction.

This is a falsifier, not a candidate quantum algorithm. Enumeration is capped;
the asymptotic bounds use rational arithmetic and never enumerate a large state.
"""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import comb, isqrt, prod


def natural(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")
    return value


def exact(value):
    if isinstance(value, float):
        raise ValueError("use exact rational inputs, not floats")
    return F(value)


@dataclass(frozen=True)
class StripeFamily:
    buckets: int
    visibility: F = F(3, 4)
    order: int = 3

    def __post_init__(self):
        natural(self.buckets, "buckets", 1)
        natural(self.order, "order", 2)
        object.__setattr__(self, "visibility", exact(self.visibility))
        if not 0 < self.visibility <= 1:
            raise ValueError("visibility must lie in (0,1]")

    @property
    def dimension(self):
        return self.buckets * self.order**2

    @property
    def heavy(self):
        return 1 + (self.order - 1) * self.visibility

    @property
    def light(self):
        return 1 - self.visibility

    def metrics(self):
        p, v, d = self.order, self.visibility, self.dimension
        purity = (1 + (p - 1) * v**2) / d
        cross = (1 - v**2) / d
        return {
            "dimension": d,
            "rank": d if v < 1 else p * self.buckets,
            "heavy_eigenvalue": self.heavy / d,
            "heavy_multiplicity": p * self.buckets,
            "light_eigenvalue": self.light / d,
            "light_multiplicity": p * (p - 1) * self.buckets,
            "purity_both_cases": purity,
            "signal_trace_distance_nonidentity": v,
            "signal_absolute_hs_distance_squared": 2 * (purity - cross),
            "signal_normalized_hs_overlap": cross / purity,
            "signal_density_vector_nontrivial_character_probability":
                F(p - 1, p) * (1 - cross / purity),
            "nonidentity_scalar_expectation_both_cases": F(0),
        }

    def alphabet(self):
        if self.dimension > 4096:
            raise ValueError("finite diagnostic alphabet exceeds cap")
        return tuple(product(range(self.buckets), range(self.order), range(self.order)))

    def _case(self, case):
        if case not in ("null", "signal"):
            raise ValueError("case must be null or signal")
        return 1 if case == "null" else 2

    def _sample(self, sample):
        if len(sample) != 3:
            raise ValueError("sample must be (bucket,row,column)")
        b, a, r = sample
        for x, size in zip((b, a, r), (self.buckets, self.order, self.order)):
            natural(x, "coordinate")
            if x >= size:
                raise ValueError("coordinate outside alphabet")

    def distribution(self, orientation, case):
        axis = self._case(case)
        if len(orientation) != self.buckets:
            raise ValueError("one fixed orientation is required per bucket")
        for x in orientation:
            natural(x, "orientation")
            if x >= self.order:
                raise ValueError("orientation outside cyclic group")
        return {
            x: (self.heavy if x[axis] == orientation[x[0]] else self.light)
            / self.dimension for x in self.alphabet()
        }

    def mixture_likelihood(self, samples, case):
        """Fixed unknown orientation across copies; likelihood relative to uniform."""
        axis = self._case(case)
        counts = {}
        for x in samples:
            self._sample(x)
            counts.setdefault(x[0], Counter())[x[axis]] += 1
        result = F(1)
        for row in counts.values():
            total = sum(row.values())
            result *= sum(
                self.heavy**row[j] * self.light**(total - row[j])
                for j in range(self.order)
            ) / self.order
        return result

    def direct_mixture_probability(self, samples, case):
        """Independent finite implementation by explicitly averaging hidden states."""
        self._case(case)
        for sample in samples:
            self._sample(sample)
        if self.order**self.buckets * self.dimension > 200000:
            raise ValueError("direct hidden-state enumeration exceeds cap")
        total = F(0)
        for orientation in product(range(self.order), repeat=self.buckets):
            state = self.distribution(orientation, case)
            total += prod((state[x] for x in samples), start=F(1))
        return total / self.order**self.buckets


def birthday_upper(buckets, copies):
    natural(buckets, "buckets", 1)
    natural(copies, "copies")
    return min(F(1), F(copies * (copies - 1), 2 * buckets))


def collision_probability(buckets, copies):
    natural(buckets, "buckets", 1)
    natural(copies, "copies")
    if copies > buckets:
        return F(1)
    if copies > 10000:
        raise ValueError("use birthday_upper for large-copy certificates")
    return 1 - prod((F(buckets - i, buckets) for i in range(copies)), start=F(1))


def mixture_chi_squared(family, copies):
    """Chi-square of E_theta rho_theta^T versus uniform^T, either case."""
    natural(copies, "copies")
    m, p, v = family.buckets, family.order, family.visibility
    if m > 1000 or copies > 1000:
        raise ValueError("exact binomial sum exceeds diagnostic cap")
    return sum(
        F(comb(m, k) * (p - 1)**(m - k), p**m)
        * (1 + v**2 * (F(p * k, m) - 1))**copies
        for k in range(m + 1)
    ) - 1


def hoeffding_exponent(family, copies):
    natural(copies, "copies")
    return F(family.order**2 * copies**2, 8 * family.buckets) * family.visibility**4


def tv_squared_upper(family, copies):
    """Rational upper bound for TV(null mixture, signal mixture)^2."""
    x = hoeffding_exponent(family, copies)
    chi_bound = min(F(1), x / (2 * (1 - x))) if x < 1 else F(1)
    return min(birthday_upper(family.buckets, copies)**2, chi_bound)


def ceil_sqrt_rational(value):
    value = exact(value)
    if value < 0:
        raise ValueError("square-root input must be nonnegative")
    n = isqrt(value.numerator // value.denominator)
    return n if n * n == value else n + 1


def necessary_copies(family, error=F(1, 3)):
    """Necessary lower bounds only, not sufficient sample counts."""
    error = exact(error)
    if not 0 <= error < F(1, 2):
        raise ValueError("error must lie in [0,1/2)")
    d = 1 - 2 * error
    rhs = 2 * family.buckets * d
    birthday = (1 + isqrt(1 + 4 * (rhs.numerator // rhs.denominator))) // 2
    while birthday * (birthday - 1) < rhs:
        birthday += 1
    chi_rhs = (16 * family.buckets * d**2
               / (family.order**2 * family.visibility**4 * (1 + 2 * d**2)))
    chi = ceil_sqrt_rational(chi_rhs)
    return {"birthday_necessary_copies": birthday,
            "rational_chi_necessary_copies": chi,
            "combined_necessary_copies": max(birthday, chi)}


def sqrt_interval(value, bits=64):
    value = exact(value)
    natural(bits, "bits", 1)
    if value < 0:
        raise ValueError("square-root input must be nonnegative")
    scale = 1 << bits
    floor = isqrt(value.numerator * scale**2 // value.denominator)
    low = F(floor, scale)
    return low, low if low**2 == value else F(floor + 1, scale)


def canonical_purification_gap(family):
    """Certified interval for nontrivial-character probability of |sqrt(rho)>>."""
    p = family.order
    low, high = sqrt_interval(family.heavy * family.light)
    overlap_low = (2 * low + (p - 2) * family.light) / p
    overlap_high = (2 * high + (p - 2) * family.light) / p
    return F(p - 1, p) * (1 - overlap_high), F(p - 1, p) * (1 - overlap_low)


def collision_score(samples):
    """Classical same-input test: positive selects null, negative selects signal."""
    rows = Counter((b, a) for b, a, r in samples)
    columns = Counter((b, r) for b, a, r in samples)
    return sum(comb(n, 2) for n in rows.values()) - sum(comb(n, 2) for n in columns.values())


def classical_moments(family, copies):
    natural(copies, "copies", 2)
    p, m, v = family.order, family.buckets, family.visibility
    s2 = (1 + (p - 1) * v**2) / p
    s3 = (family.heavy**3 + (p - 1) * family.light**3) / p**3
    pair_mean = v**2 * F(p - 1, p * m)
    pair_second = (s2 * (1 - F(2, p)) + F(1, p)) / m
    shared_second = (s3 - 2 * s2 / p + F(1, p**2)) / m**2
    mean = comb(copies, 2) * pair_mean
    variance = (comb(copies, 2) * (pair_second - pair_mean**2)
                + 6 * comb(copies, 3) * (shared_second - pair_mean**2))
    return {"null_mean": mean, "signal_mean": -mean,
            "variance_both_cases": variance,
            "error_upper_chebyshev": min(F(1), variance / mean**2)}


def classical_sufficient_copies(family):
    # Conservative constant makes the simple variance bound < 1/3 for all M>=1.
    return ceil_sqrt_rational(256**2 * family.buckets / family.visibility**4)


def exhaustive_control(family, copies):
    natural(copies, "copies")
    if family.dimension**copies > 20000:
        raise ValueError("joint-state enumeration exceeds diagnostic cap")
    mass = F(1, family.dimension**copies)
    tv = chi_null = chi_signal = cross = norm_null = norm_signal = F(0)
    for samples in product(family.alphabet(), repeat=copies):
        left = family.mixture_likelihood(samples, "null")
        right = family.mixture_likelihood(samples, "signal")
        if len({x[0] for x in samples}) == copies:
            assert left == right == 1
        norm_null += mass * left
        norm_signal += mass * right
        tv += mass * abs(left - right) / 2
        chi_null += mass * (left - 1)**2
        chi_signal += mass * (right - 1)**2
        cross += mass * left * right
    expected_chi = mixture_chi_squared(family, copies)
    assert norm_null == norm_signal == cross == 1
    assert chi_null == chi_signal == expected_chi
    assert tv <= collision_probability(family.buckets, copies)
    assert tv**2 <= expected_chi / 2
    assert tv**2 <= tv_squared_upper(family, copies)
    return {"buckets": family.buckets, "order": family.order,
            "visibility": family.visibility, "copies": copies,
            "enumerated_joint_words": family.dimension**copies,
            "tv": tv, "chi_squared_each_vs_uniform": expected_chi,
            "cross_likelihood_moment": cross,
            "collision_probability": collision_probability(family.buckets, copies)}
