"""Uniform prime-field scalar diagonal cancellation, with explicit caps.

This is a classical arithmetic primitive, not a quantum receiver. The large
field branch uses a Fermat-curve point bound and a smooth-part root algorithm;
only fields bounded by 16*g**4 are enumerated. See SCALAR_CANCELLATION.md.
"""

from dataclasses import dataclass, asdict
from fractions import Fraction
from math import gcd, prod
import random

from flint import fmpz


class TrialBudgetExceeded(RuntimeError):
    """An explicitly capped randomized step failed; no witness is returned."""


def positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"positive integer {name} required")


def check_prime(prime):
    if type(prime) is not int or prime < 3 or not fmpz(prime).is_prime():
        raise ValueError("an odd prime field is required")


def prime_factors(number):
    """Factor the degree, NEVER the unrestricted integer p-1."""
    positive(number, "degree")
    factors = []
    divisor = 2
    while divisor*divisor <= number:
        if number % divisor == 0:
            factors.append(divisor)
            while number % divisor == 0:
                number //= divisor
        divisor += 1
    if number > 1:
        factors.append(number)
    return tuple(factors)


def draw(rng, start, stop):
    value = rng.randrange(start, stop)
    if type(value) is not int or not start <= value < stop:
        raise ValueError("random source returned a noncanonical field element")
    return value


@dataclass
class Counters:
    generator_draws: int = 0
    root_calls: int = 0
    pohlig_hellman_digits: int = 0
    scalar_calls: int = 0
    curve_trials: int = 0
    small_field_elements: int = 0
    sumset_transitions: int = 0
    zero_coefficient_solves: int = 0
    linear_solves: int = 0
    small_field_solves: int = 0
    large_field_solves: int = 0


class SmoothPowerRoots:
    """g-th roots for g | p-1 using only degree-smooth discrete logarithms.

    Randomness is confined to a capped search for a generator of the
    degree-smooth subgroup. All subsequent loops have explicit finite bounds.
    """

    def __init__(self, prime, degree, *, rng=None, attempt_cap=256, counters=None):
        check_prime(prime)
        positive(degree, "degree")
        positive(attempt_cap, "generator attempt cap")
        if (prime-1) % degree:
            raise ValueError("root degree must divide p-1")
        self.p, self.g = prime, degree
        self.stats = counters if counters is not None else Counters()
        self.factors = prime_factors(degree)
        self.components = []
        rough = prime-1
        for ell in self.factors:
            power, exponent = 1, 0
            while rough % ell == 0:
                rough //= ell
                power *= ell
                exponent += 1
            self.components.append((ell, power, exponent))
        self.rough, self.smooth = rough, (prime-1)//rough
        self.generator_success_probability = prod(
            (Fraction(ell-1, ell) for ell in self.factors), start=Fraction(1))
        self.abort_bound = (1-self.generator_success_probability)**attempt_cap
        if degree == 1:
            self.generator, self.tables = 1, []
            return
        rng = rng if rng is not None else random.SystemRandom()
        for _ in range(attempt_cap):
            self.stats.generator_draws += 1
            generator = pow(draw(rng, 1, prime), rough, prime)
            if all(pow(generator, self.smooth//ell, prime) != 1 for ell in self.factors):
                break
        else:
            raise TrialBudgetExceeded("smooth-subgroup generator cap exhausted")
        self.generator = generator
        self.tables = []
        for ell, power, exponent in self.components:
            base = pow(generator, self.smooth//power, prime)
            digit_base = pow(base, power//ell, prime)
            table, value = {}, 1
            for digit in range(ell):
                table[value] = digit
                value = value*digit_base % prime
            if len(table) != ell:
                raise ArithmeticError("invalid small-order digit table")
            self.tables.append((ell, power, exponent, base, table))

    def root(self, value):
        """Return an exactly checked root, or None for a genuine nonresidue."""
        p, g = self.p, self.g
        if type(value) is not int or not 0 <= value < p:
            raise ValueError("canonical field value required")
        self.stats.root_calls += 1
        if not value or g == 1:
            return value
        if pow(value, (p-1)//g, p) != 1:
            return None
        smooth, rough = self.smooth, self.rough
        smooth_value = pow(value, rough*pow(rough, -1, smooth), p)
        residues = []
        for ell, power, exponent, base, table in self.tables:
            target = pow(smooth_value, smooth//power, p)
            logarithm, place = 0, 1
            for j in range(exponent):
                residual = target*pow(base, -logarithm, p) % p
                digit_value = pow(residual, ell**(exponent-1-j), p)
                if digit_value not in table:
                    raise ArithmeticError("smooth discrete-log digit missing")
                logarithm += table[digit_value]*place
                place *= ell
                self.stats.pohlig_hellman_digits += 1
            if pow(base, logarithm, p) != target:
                raise ArithmeticError("smooth discrete logarithm failed verification")
            residues.append((logarithm, power))
        logarithm = sum(a*(smooth//m)*pow(smooth//m, -1, m)
                        for a, m in residues) % smooth
        if logarithm % g or pow(self.generator, logarithm, p) != smooth_value:
            raise ArithmeticError("invalid smooth-part root certificate")
        smooth_root = pow(self.generator, logarithm//g, p)
        rough_root = 1
        if rough > 1:
            rough_value = pow(value, smooth*pow(smooth, -1, rough), p)
            rough_root = pow(rough_value, pow(g, -1, rough), p)
        root = smooth_root*rough_root % p
        if pow(root, g, p) != value:
            raise ArithmeticError("final power-root check failed")
        return root


def verify_scalar(prime, degree, coefficients, weights):
    if len(weights) != len(coefficients) or not any(weights):
        raise ArithmeticError("nonzero scalar witness of correct length required")
    if any(type(x) is not int or not 0 <= x < prime for x in weights):
        raise ArithmeticError("noncanonical scalar witness")
    if sum(a*pow(x, degree, prime) for a, x in zip(coefficients, weights)) % prime:
        raise ArithmeticError("scalar diagonal moment did not vanish")


class ScalarBackend:
    """Callable backend for central_rank.compressed_witness.

    The failure bound assumes independent uniform draws, including when the
    coefficients depend on earlier public history. Seeded replays only test
    correctness. The declared call budget is enforced, not silently enlarged.
    """

    def __init__(self, prime, degree, *, max_scalar_calls=1, security_bits=64, rng=None):
        check_prime(prime)
        positive(degree, "reduced degree")
        positive(max_scalar_calls, "scalar call budget")
        positive(security_bits, "security bits")
        if (prime-1) % degree:
            raise ValueError("reduced degree must divide p-1")
        self.p, self.g = prime, degree
        self.max_calls, self.security_bits = max_scalar_calls, security_bits
        # (calls+1)*2^-bits <= 2^-security_bits, including one shared setup.
        self.bits = security_bits + max_scalar_calls.bit_length()
        self.curve_cap = 2*degree*self.bits
        self.generator_cap = degree*self.bits
        self.rng = rng if rng is not None else random.SystemRandom()
        self.randomness = "system_random" if rng is None else "caller_supplied_replay_or_rng"
        self.stats = Counters()
        self.roots = None
        self.powers = None
        self.failed = False

    @property
    def abort_bound(self):
        if self.g == 1 or self.p <= 16*self.g**4:
            return Fraction(0)
        return Fraction(1, 2**self.security_bits)

    def __call__(self, coefficients, degree, prime):
        if self.failed:
            raise TrialBudgetExceeded("backend already aborted; start a new accounted attempt")
        coefficients = tuple(coefficients)
        if prime != self.p or degree != self.g or len(coefficients) != degree+1:
            raise ValueError("backend field, reduced degree and exact scalar arity must match")
        if any(type(a) is not int or not 0 <= a < prime for a in coefficients):
            raise ValueError("canonical scalar coefficients required")
        if self.stats.scalar_calls >= self.max_calls:
            raise TrialBudgetExceeded("declared scalar call budget exhausted")
        self.stats.scalar_calls += 1
        try:
            weights = self._solve(coefficients)
        except TrialBudgetExceeded:
            self.failed = True
            raise
        verify_scalar(prime, degree, coefficients, weights)
        return tuple(weights)

    def _solve(self, coefficients):
        p, g = self.p, self.g
        if 0 in coefficients:
            self.stats.zero_coefficient_solves += 1
            weights = [0]*(g+1)
            weights[coefficients.index(0)] = 1
            return weights
        if g == 1:
            self.stats.linear_solves += 1
            return [-coefficients[1]*pow(coefficients[0], -1, p) % p, 1]
        if p <= 16*g**4:
            self.stats.small_field_solves += 1
            return self._small_field(coefficients)
        self.stats.large_field_solves += 1
        if self.roots is None:
            self.roots = SmoothPowerRoots(p, g, rng=self.rng,
                                         attempt_cap=self.generator_cap, counters=self.stats)
        a, b, c = coefficients[:3]
        inverse_b = pow(b, -1, p)
        for _ in range(self.curve_cap):
            self.stats.curve_trials += 1
            x = draw(self.rng, 0, p)
            y = self.roots.root(-(a*pow(x, g, p)+c)*inverse_b % p)
            if y is not None:
                return [x, y, 1]+[0]*(g-2)
        raise TrialBudgetExceeded("Fermat-curve trial cap exhausted")

    def _small_field(self, coefficients):
        p, g = self.p, self.g
        if p > 16*g**4:
            raise ValueError("field enumeration forbidden outside the polynomial degree bound")
        if self.powers is None:
            self.powers = {}
            for x in range(p):
                self.powers.setdefault(pow(x, g, p), x)
            self.stats.small_field_elements += p
            if len(self.powers) != (p-1)//g+1:
                raise ArithmeticError("power image has the wrong cardinality")
        # Fix the last coordinate at one. Cauchy-Davenport guarantees that
        # the sum of g scaled power images covers F_p, including this target.
        target = -coefficients[-1] % p
        reachable, histories = {0}, []
        for coefficient in coefficients[:-1]:
            parents = {}
            for previous in sorted(reachable):
                for power, x in self.powers.items():
                    self.stats.sumset_transitions += 1
                    residue = (previous+coefficient*power) % p
                    parents.setdefault(residue, (previous, x))
                    if residue == target:
                        break
                if target in parents:
                    break
            histories.append(parents)
            if target in parents:
                weights = [0]*g+[1]
                current = target
                for j in range(len(histories)-1, -1, -1):
                    current, weights[j] = histories[j][current]
                if current != 0:
                    raise ArithmeticError("broken sumset predecessor chain")
                return weights
            reachable = set(parents)
        raise ArithmeticError("Cauchy-Davenport coverage failed")

    def report(self):
        return {
            "prime": self.p, "reduced_degree": self.g,
            "declared_scalar_call_cap": self.max_calls,
            "curve_attempt_cap_per_call": self.curve_cap,
            "shared_generator_attempt_cap": self.generator_cap,
            "whole_backend_abort_bound": str(self.abort_bound),
            "bound_requires_iid_uniform_draws": True,
            "randomness": self.randomness,
            "enumeration_allowed_only_when_p_at_most": 16*self.g**4,
            "full_p_minus_1_factorization_used": False,
            "black_box_polynomial_root_solver_used": False,
            "failed": self.failed, "counters": asdict(self.stats),
        }


def scalar_call_cap(reduced_degree, rank):
    positive(reduced_degree, "reduced degree")
    if type(rank) is not int or rank < 0:
        raise ValueError("nonnegative rank required")
    return 0 if reduced_degree == 1 else ((reduced_degree+1)**rank-1)//reduced_degree


def reduced_degree(prime, degree):
    check_prime(prime)
    positive(degree, "degree")
    return gcd(degree, prime-1)
