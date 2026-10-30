"""Exact fingerprint budget for FORMAL polynomial orbits.

This is parameter arithmetic, not an HSP solver or a circuit extractor.
The caller must supply a genuine degree bound, an explicit division-free
circuit, and an action of a supplied subgroup of GL(dimension, p).
No hardness or correctness of the proposed class-four receiver follows.
"""

from dataclasses import dataclass
from fractions import Fraction
from math import comb

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


def lcs_step_derivative_guard(
    prime: int, dimension: int, degree_bound: int, lcs_step: int = 1
) -> dict[str, object]:
    """Sufficient regime for the derivative attack restricted to an LCS subgroup.

    On the r-th lower central series subgroup Gamma_r = exp(gamma_r(u_D(F_p)))
    with r = lcs_step, every Lie generator has nilpotency power at most
    s_r = (dimension - 1) // lcs_step. Thus exp(-tA) has entry degree at most s_r,
    and t -> F(exp(-tA)x) has parameter degree at most s_r * degree_bound.
    This opens an intermediate-characteristic window where the derivative attack
    succeeds on Gamma_r even when the full-group guard fails.
    """
    plan_orbit_fingerprint(prime, dimension, degree_bound)
    if type(lcs_step) is not int or not 1 <= lcs_step < dimension:
        raise ValueError("lcs_step must be an integer in [1, D-1]")
    s_r = (dimension - 1) // lcs_step
    step_path_degree = s_r * degree_bound
    threshold = max(dimension, step_path_degree)
    if prime <= threshold:
        raise ValueError("requires p>max(D,((D-1)//lcs_step)*degree) for this LCS step derivative attack")
    return {
        "lcs_step": lcs_step,
        "nilpotent_power_bound": s_r,
        "parameter_degree_bound": step_path_degree,
        "strict_characteristic_threshold": threshold,
        "full_group_guard_passes": prime > max(dimension, (dimension - 1) * degree_bound),
        "recovers_subgroup_intersection_only": lcs_step > 1,
        "circuit_gradient_access_required": True,
    }


def artin_schreier_carry_counterexample(prime: int) -> dict[str, object]:
    """Demonstrates failure of naive Lie-algebraic derivatives at degree p (Artin-Schreier carry).

    Constructs F(x_1, x_2) = x_1^p - x_1 x_2^{p-1} of total degree Delta = p over F_p.
    The true stabilizer under unitriangular shear g_alpha: (x_1, x_2) -> (x_1 + alpha x_2, x_2)
    is the full group F_p (size p, dimension 1), but the naive chain-rule derivative kernel
    is trivial ({0}, size 1, dimension 0) because the derivative ignores the degree-p carry
    alpha^p t^p x_2^p which cancels -alpha t x_2^p on F_p.
    """
    if type(prime) is not int or prime <= 4 or not fmpz(prime).is_prime():
        raise ValueError("prime p>4 required")

    p = prime
    # Verify exact binomial coefficients vanish mod p: comb(p, j) = 0 mod p for 1 <= j <= p-1
    for j in range(1, p):
        assert comb(p, j) % p == 0

    stabilizer_alphas = []
    derivative_kernel_alphas = []

    for alpha in range(p):
        # 1. Full polynomial difference:
        # F(x_1 + alpha*x_2, x_2) - F(x_1, x_2) = (alpha^p - alpha) * x_2^p (mod p)
        # By Fermat's Little Theorem, (alpha^p - alpha) = 0 mod p for all alpha in F_p.
        diff_coeff = (pow(alpha, p, p) - alpha) % p
        if diff_coeff == 0:
            stabilizer_alphas.append(alpha)

        # 2. Naive derivative along 1-parameter curve t -> F(x_1 + t*alpha*x_2, x_2) - F(x_1, x_2):
        # The t^1 coefficient is -alpha mod p.
        # This vanishes iff alpha == 0 mod p.
        t1_coeff = (-alpha) % p
        if t1_coeff == 0:
            derivative_kernel_alphas.append(alpha)

    # 3. When reduced modulo t^p - t, the t^p coefficient (alpha^p) wraps into t^1:
    # (alpha^p - alpha) = 0 mod p for all alpha in F_p.
    assert len(stabilizer_alphas) == p
    assert derivative_kernel_alphas == [0]

    return {
        "prime": p,
        "polynomial": f"x_1^{p} - x_1*x_2^{p-1}",
        "total_degree": p,
        "group_dimension": 1,
        "true_stabilizer_size": p,
        "true_stabilizer_dimension": 1,
        "naive_derivative_kernel_size": 1,
        "naive_derivative_kernel_dimension": 0,
        "derivative_underestimates_stabilizer": True,
        "artin_schreier_carry_degree": p,
        "modulo_tp_minus_t_cancels": True,
        "orbit_module_rank_upper_bound": 2,
        "caught_by_orbit_module_filter": True,
        "hardness_claim": False,
    }
