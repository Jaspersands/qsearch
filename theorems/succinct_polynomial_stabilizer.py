"""Exact fingerprint budget for FORMAL polynomial orbits.

This is parameter arithmetic, not an HSP solver or a circuit extractor.
The caller must supply a genuine degree bound, an explicit division-free
circuit, and an action of a supplied subgroup of GL(dimension, p).
No hardness or correctness of the proposed class-four receiver follows.
"""

from dataclasses import dataclass
from fractions import Fraction

from flint import fmpz


@dataclass(frozen=True)
class OrbitFingerprintPlan:
    prime: int
    dimension: int
    degree_bound: int
    error_budget: Fraction
    extension_degree: int

    @property
    def group_order_upper_bound(self):
        # A deliberately loose bound, requiring neither order nor generators.
        return self.prime ** (self.dimension**2)

    @property
    def field_size(self):
        return self.prime**self.extension_degree

    @property
    def collision_probability_upper_bound(self):
        return min(Fraction(1), Fraction(
            self.degree_bound * self.group_order_upper_bound**2,
            self.field_size,
        ))

    @property
    def label_bits_upper_bound(self):
        return self.extension_degree * self.prime.bit_length()

    @property
    def fixed_point_bits_upper_bound(self):
        return self.dimension * self.label_bits_upper_bound


def plan_orbit_fingerprint(prime, dimension, degree_bound,
                           error_budget=Fraction(1, 100)):
    """One fixed uniform extension-field point separates the entire orbit.

    The union bound is over all group pairs, not just queries made so far.
    Field construction, quantum receiver error, and circuit execution are
    separate costs. The prime>4 restriction belongs to the intended HSP
    application; the fingerprint argument itself is more general.
    """
    if type(prime) is not int or prime <= 4 or not fmpz(prime).is_prime():
        raise ValueError("prime p>4 required for the intended application")
    if type(dimension) is not int or dimension < 1:
        raise ValueError("positive integer matrix dimension required")
    if type(degree_bound) is not int or degree_bound < 0:
        raise ValueError("nonnegative integer formal degree bound required")
    if not isinstance(error_budget, Fraction) or not 0 < error_budget < 1:
        raise ValueError("exact rational error budget in (0,1) required")
    numerator = degree_bound * prime ** (2 * dimension**2)
    extension_degree, field_size = 1, prime
    while numerator * error_budget.denominator > field_size * error_budget.numerator:
        extension_degree += 1
        field_size *= prime
    return OrbitFingerprintPlan(prime, dimension, degree_bound,
                                error_budget, extension_degree)


def white_box_derivative_guard(prime, dimension, degree_bound):
    """Sufficient regime for the written classical matrix-p-group attack.

    The group is PROMISED to be a supplied matrix p-group. Its Lie basis,
    the circuit/gradient and sampling must actually be computed. Passing
    this guard is not an implementation or a semantic promise checker.
    """
    plan_orbit_fingerprint(prime, dimension, degree_bound)
    path_degree = (dimension-1)*degree_bound
    threshold = max(dimension, path_degree)
    if prime <= threshold:
        raise ValueError("requires p>max(D,(D-1)*degree) for this attack")
    return {
        "parameter_degree_bound": path_degree,
        "strict_characteristic_threshold": threshold,
        "derivative_total_degree_bound": degree_bound,
        "unknown_dimension_upper_bound": dimension**2,
        "extension_field_samples_suffice": dimension**2,
        "degree_expansion_required": False,
        "circuit_gradient_access_required": True,
    }
