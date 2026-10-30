"""Finite algebra controls for a scoped Rees source/receiver obstruction.

This does not simulate a scalable quantum algorithm or certify hardness.
Character averages are exact elements of Q(zeta_p), represented in the
power basis of degree p-2. Only explicitly bounded groups are enumerated.
"""

from dataclasses import dataclass
from fractions import Fraction
from functools import cached_property
from itertools import product

from sympy import isprime


Element = tuple[int, int, int, int]


@dataclass(frozen=True)
class ReesHeisenberg:
    p: int

    def __post_init__(self):
        if not isinstance(self.p, int) or isinstance(self.p, bool):
            raise ValueError("p must be an odd prime integer")
        if self.p < 3 or self.p > 31 or not isprime(self.p):
            raise ValueError("finite controls require an odd prime at most 31")

    @cached_property
    def elements(self) -> tuple[Element, ...]:
        return tuple(product(range(self.p), repeat=4))

    @property
    def identity(self) -> Element:
        return (0, 0, 0, 0)

    def mul(self, a: Element, b: Element) -> Element:
        p = self.p
        x, y, w, z = a
        xx, yy, ww, zz = b
        return (
            (x + xx) % p,
            (y + yy) % p,
            (w + ww) % p,
            (z + zz + ((p + 1) // 2) * (x * yy - y * xx)) % p,
        )

    def inv(self, a: Element) -> Element:
        return tuple(-x % self.p for x in a)

    def conjugate(self, by: Element, a: Element) -> Element:
        return self.mul(self.mul(by, a), self.inv(by))

    def hidden(self, axis: str) -> tuple[Element, ...]:
        if axis == "X":
            return tuple((t, 0, 0, 0) for t in range(self.p))
        if axis == "Y":
            return tuple((0, t, 0, 0) for t in range(self.p))
        raise ValueError("axis must be X or Y")

    def sector_phase(self, axis: str, label: int, a: Element) -> int | None:
        """Exponent of Tr(rho_H,label R_a), or None for a zero trace."""
        self.hidden(axis)
        if not 0 <= label < self.p:
            raise ValueError("central label outside F_p")
        x, y, w, z = a
        in_hz = w == 0 and (y == 0 if axis == "X" else x == 0)
        return (label * z) % self.p if in_hz else None

    def conjugacy_kernel(self, axis: str, label: int, a: Element):
        # Central coordinates of a conjugator act trivially. Enumerate its
        # two noncentral coordinates, retaining the full exact average.
        counts = [0] * self.p
        for x, y in product(range(self.p), repeat=2):
            exponent = self.sector_phase(
                axis, label, self.conjugate((x, y, 0, 0), a)
            )
            if exponent is not None:
                counts[exponent] += 1
        return tuple(Fraction(c - counts[-1], self.p**2) for c in counts[:-1])

    def predicted_kernel(self, axis: str, label: int, a: Element):
        exponent = self.sector_phase(axis, label, a)
        if label and a[:3] != (0, 0, 0):
            exponent = None
        counts = [0] * self.p
        if exponent is not None:
            counts[exponent] = 1
        return tuple(Fraction(c - counts[-1]) for c in counts[:-1])

    def control_kernel(self, axis, label, a, b, aa, bb):
        # Anti-representation ordering: W(q')^* W(q) has relative word
        # a(q) a(q')^-1 b(q') b(q)^-1, not a^-1 a' b'^-1 b.
        word = self.mul(self.mul(self.mul(a, self.inv(aa)), bb), self.inv(b))
        return self.conjugacy_kernel(axis, label, word)


def evaluate_character(coefficients, p):
    """Numerical comparison helper, not used to assert exact vanishing."""
    import cmath

    return sum(float(c) * cmath.exp(2j * cmath.pi * j / p)
               for j, c in enumerate(coefficients))


def acquisition_bound(p: int, copies: int):
    if (not isinstance(p, int) or isinstance(p, bool)
            or p <= 2 or not isprime(p)):
        raise ValueError("p must be an odd prime")
    if not isinstance(copies, int) or isinstance(copies, bool) or copies < 0:
        raise ValueError("copies must be a nonnegative integer")
    event_bound = min(Fraction(1), Fraction(copies, p))
    return {
        "p": p,
        "source_cap": copies,
        "rare_event_union_bound": event_bound,
        "binary_success_upper_bound": (1 + event_bound) / 2,
        "necessary_sources_for_two_thirds": (p + 2) // 3,
        "original_queries_per_source": 2,
        "scope": "relative-product source; central labels; right actions; target discard",
        "is_hsp_query_lower_bound": False,
    }
