"""Lossless all-one native reduction and exact fixed-carry norm search.

The carry polynomial is an EXTRA input, not obtained efficiently here.
Factor orientations can be exponential. All norm-one scalar multiples are
handled by a two-variable linear system without enumerating the field.
"""

from dataclasses import dataclass
from fractions import Fraction
import importlib.util
from itertools import product
from math import prod
from pathlib import Path
import sys

from flint import fq_default_ctx, fq_default_poly_ctx


ROOT = Path(__file__).resolve().parent
DEPENDENCY = ROOT.parent / "inverse-trace-norm-transfer-2026-10-23/norm_transfer.py"
SPEC = importlib.util.spec_from_file_location("modular_norm_dependency", DEPENDENCY)
OLD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = OLD
SPEC.loader.exec_module(OLD)


def encoded_element(x):
    return sum(int(bit) << j for j, bit in enumerate(x.to_list()))


@dataclass
class NativeInstance:
    bits: int
    modulus: int
    points: tuple

    def __post_init__(self):
        if type(self.bits) is not int or self.bits < 5 or self.bits % 2 == 0:
            raise ValueError("this reduction uses odd native field degree >= 5 and all-one targets")
        self.native, self.field, self.ring = OLD.contexts(self.bits, self.modulus)
        self.points = tuple(self.points)
        self.N, self.K = self.bits**2, self.bits**2 // 8
        if len(self.points) != self.N or len(set(self.points)) != self.N:
            raise ValueError("exact native length and distinct points required")
        for a in self.points:
            self.native.element(a)
        self.elements = tuple(self.element(a) for a in self.points)
        self.F = self.ring.one()
        for a in self.elements:
            self.F *= self.ring.gen() + a
        self.derivative = self.F.derivative()
        self.D = self.ring([self.derivative[2*j].sqrt()
                            for j in range(self.derivative.degree() // 2 + 1)])
        if self.D**2 != self.derivative or any(self.D(a) == 0 for a in self.elements):
            raise ArithmeticError("invalid squarefree interpolation modulus")

    def element(self, value):
        return OLD.element(self.field, value, self.bits)

    def interpolate(self, values):
        if len(values) != self.N:
            raise ValueError("one field value per original point required")
        out = self.ring.zero()
        for a, value in zip(self.elements, values):
            out += self.F.exact_division(self.ring.gen() + a) * (value / self.derivative(a))
        if any(out(a) != value for a, value in zip(self.elements, values)):
            raise ArithmeticError("interpolation failed")
        return out

    def verify_word(self, values):
        return OLD.NATIVE.verify(self.native, self.points, values, self.K,
                                 (1,) * self.N, (0,) * self.K)

    def word_from_Q(self, Q):
        P = Q**2 % self.F
        if P.degree() >= self.N - self.K or any(Q(a) == 0 for a in self.elements):
            return None
        values = tuple(encoded_element(P(a) / self.derivative(a)) for a in self.elements)
        return values if self.verify_word(values) else None

    def carry_from_witness(self, values):
        """A correctness control, NOT native acquisition of the unknown carry."""
        if not self.verify_word(values):
            raise ValueError("a verified all-one native witness is required for this control")
        P = self.interpolate([self.element(x) * self.derivative(a)
                              for x, a in zip(values, self.elements)])
        Q = self.interpolate([P(a).sqrt() for a in self.elements])
        roots = []
        for a in self.elements:
            z = self.D(a) / Q(a) + 1
            h, term = self.field.zero(), z
            for _ in range((self.bits + 1) // 2):
                h += term
                term = term**4
            if h**2 + h != z:
                raise ArithmeticError("Artin-Schreier half-trace failed")
            roots.append(Q(a) * h)
        U = self.interpolate(roots)
        A = U + self.D
        numerator = A**2 + A*Q + Q**2 + self.D**2
        W, residue = divmod(numerator, self.F)
        if not residue.is_zero() or W.degree() > self.N - 2 or Q**2 % self.F != P:
            raise ArithmeticError("lossless modular norm reduction failed")
        return {"P": P, "Q": Q, "A": A, "W": W,
                "carry_was_derived_from_known_witness": True}


class QuadraticExtension:
    """Explicitly checked embedding into FLINT's binary degree-2n field."""

    def __init__(self, instance):
        self.instance = instance
        self.bits, self.q = instance.bits, instance.native.order
        self.field = fq_default_ctx(2, 2*self.bits, "w")
        self.ring = fq_default_poly_ctx(self.field)
        modulus = self.ring([(instance.modulus >> j) & 1 for j in range(self.bits + 1)])
        roots = modulus.roots(multiplicities=False)
        if len(roots) != self.bits or any(modulus(root) != 0 for root in roots):
            raise ArithmeticError("base-field embedding roots incomplete")
        self.beta = min(roots, key=encoded_element)
        self.basis = tuple(self.beta**j for j in range(self.bits))
        theta_roots = (self.ring.gen()**2 + self.ring.gen() + 1).roots(multiplicities=False)
        self.theta = min(theta_roots, key=encoded_element)
        if len(theta_roots) != 2 or self.theta**self.q != self.theta + 1:
            raise ArithmeticError("quadratic constant extension is not the required nonsplit one")
        self.inverse_basis = {}
        for j, element in enumerate(self.basis):
            mask, value = encoded_element(element), 1 << j
            while mask:
                pivot = mask.bit_length() - 1
                if pivot not in self.inverse_basis:
                    self.inverse_basis[pivot] = (mask, value)
                    break
                old_mask, old_value = self.inverse_basis[pivot]
                mask, value = mask ^ old_mask, value ^ old_value
            else:
                raise ArithmeticError("base-field embedding is not injective")

    def embed(self, value):
        bits = encoded_element(value)
        return sum((self.basis[j] for j in range(self.bits) if bits >> j & 1), self.field.zero())

    def descend(self, value):
        if value**self.q != value:
            raise ValueError("coefficient does not lie in the original field")
        mask, encoded = encoded_element(value), 0
        while mask:
            pivot = mask.bit_length() - 1
            if pivot not in self.inverse_basis:
                raise ArithmeticError("fixed-field coefficient outside the verified basis")
            old_mask, old_value = self.inverse_basis[pivot]
            mask, encoded = mask ^ old_mask, encoded ^ old_value
        out = self.instance.element(encoded)
        if self.embed(out) != value:
            raise ArithmeticError("coefficient descent failed")
        return out

    def embed_poly(self, polynomial):
        return self.ring([self.embed(c) for c in polynomial.coeffs()])

    def conjugate(self, polynomial):
        return self.ring([c**self.q for c in polynomial.coeffs()])

    def split(self, polynomial):
        Q = polynomial + self.conjugate(polynomial)
        A = polynomial + Q*self.theta
        return (self.instance.ring([self.descend(c) for c in A.coeffs()]),
                self.instance.ring([self.descend(c) for c in Q.coeffs()]))


def code_unit_kernel(instance, A, Q):
    """All norm-unit rotations satisfying the FULL modular code constraint."""
    left, right = A**2 % instance.F, Q**2 % instance.F
    pivot = None
    for j in range(instance.N - instance.K, instance.N):
        a, b = left[j].sqrt(), right[j].sqrt()
        if a == 0 and b == 0:
            continue
        if pivot is None:
            pivot = (a, b)
        elif a*pivot[1] + b*pivot[0] != 0:
            return 2, None
    if pivot is None:
        return 0, None
    return 1, (pivot[1], pivot[0])


def normalized_units(instance, A, Q):
    """At most N+1 exact trials, covering every necessary scalar possibility.

    In rank zero a finite hitting set suffices for existence, not enumeration
    of all answers. In rank one the norm-one point is unique. Rank two is empty.
    """
    rank, direction = code_unit_kernel(instance, A, Q)
    if rank == 2:
        return rank, []
    if rank == 1:
        r, s = direction
        norm = r*r + r*s + s*s
        if norm == 0:
            raise ArithmeticError("anisotropic norm vanished on a nonzero direction")
        scale = norm.sqrt()**-1
        return rank, [(r*scale, s*scale)]
    one, zero = instance.field.one(), instance.field.zero()
    units = [(zero, one)]
    for value in range(instance.N):
        t = instance.element(value)
        denominator = t*t + t + one
        units.append((one/denominator, t*t/denominator))
    if any(r*r+r*s+s*s != one for r, s in units):
        raise ArithmeticError("norm-one parametrization failed")
    return rank, units


def fixed_carry(instance, W, orientation_cap=4096):
    """Exact existence decision for one supplied carry, or explicitly UNKNOWN."""
    if type(orientation_cap) is not int or orientation_cap < 1:
        raise ValueError("positive orientation cap required")
    if W.degree() > instance.N - 2:
        raise ValueError("carry is outside the lossless reduced-degree domain")
    R = instance.D**2 + instance.F*W
    base = {"scope": "ONE_SUPPLIED_CARRY_ALL_ONE_NATIVE_RELATION", "W": OLD.encoded(W),
            "native_carry_acquisition_implemented": False, "quantum_advantage": False,
            "field_units_enumerated": False, "orientation_cap": orientation_cap,
            "orientations_checked": 0, "unit_trials": 0, "witness": None}
    if R.degree() % 2:
        return {**base, "status": "NO_SOLUTION_FOR_THIS_CARRY", "reason": "ODD_NORM_DEGREE"}
    extension = QuadraticExtension(instance)
    Rex = extension.embed_poly(R)
    unit, factors = Rex.factor()
    reconstructed = extension.ring(unit)
    for f, e in factors:
        if not f.is_irreducible():
            raise ArithmeticError("uncertified factor")
        reconstructed *= f**e
    if reconstructed != Rex:
        raise ArithmeticError("factorization incomplete")
    factor_map = {str(f): (f, e) for f, e in factors}
    used, pairs = set(), []
    common = extension.ring(extension.embed(R.leading_coefficient().sqrt()))
    for key in sorted(factor_map):
        if key in used:
            continue
        f, e = factor_map[key]
        conjugate = extension.conjugate(f)
        if conjugate == f:
            if e % 2:
                return {**base, "status": "NO_SOLUTION_FOR_THIS_CARRY",
                        "reason": "INERT_FACTOR_ODD_MULTIPLICITY", "inert_degree": f.degree()}
            common *= f**(e//2)
            used.add(key)
        else:
            partner = factor_map.get(str(conjugate))
            if partner is None or partner[1] != e:
                raise ArithmeticError("conjugate factor pair missing")
            pairs.append((f, conjugate, e))
            used.update((key, str(conjugate)))
    count = prod(e+1 for _, _, e in pairs)
    base["orientation_count"] = count
    base["conjugate_pair_multiplicities"] = [e for _, _, e in pairs]
    if count > orientation_cap:
        return {**base, "status": "UNKNOWN_ORIENTATION_CAP", "reason": "NO_NEGATIVE_RESULT"}
    ranks = [0, 0, 0]
    for exponents in product(*(range(e+1) for _, _, e in pairs)):
        B = common
        for (f, g, e), exponent in zip(pairs, exponents):
            B *= f**exponent * g**(e-exponent)
        if B * extension.conjugate(B) != Rex:
            raise ArithmeticError("factor orientation is not a norm witness")
        A, Q = extension.split(B)
        if A**2 + A*Q + Q**2 != R:
            raise ArithmeticError("norm-coordinate conversion failed")
        rank, units = normalized_units(instance, A, Q)
        ranks[rank] += 1
        base["orientations_checked"] += 1
        for r, s in units:
            base["unit_trials"] += 1
            candidate_Q = r*A+s*Q
            candidate_A = (s+r)*A+r*Q
            if candidate_A**2 + candidate_A*candidate_Q + candidate_Q**2 != R:
                raise ArithmeticError("scalar normalization changed the norm")
            values = instance.word_from_Q(candidate_Q)
            if values is not None:
                return {**base, "status": "VERIFIED_NATIVE_WITNESS_FOR_SUPPLIED_CARRY",
                        "reason": "EXACT_NATIVE_PARITY_AND_TRACE_CHECK", "unit_kernel_ranks": ranks,
                        "witness": list(values), "Q": OLD.encoded(candidate_Q),
                        "A": OLD.encoded(candidate_A), "unit": [encoded_element(r), encoded_element(s)]}
        if rank == 0:
            raise ArithmeticError("finite norm-unit hitting set contradicted its nonzero-point guarantee")
    return {**base, "status": "NO_SOLUTION_FOR_THIS_CARRY",
            "reason": "ALL_FACTOR_ORIENTATIONS_AND_NORM_UNITS_EXCLUDED", "unit_kernel_ranks": ranks}


def uniform_carry_bound(bits, trials=1):
    """Exact union bound, not a bound for structured/adaptive carry generators.

    Every native witness has exactly 2^(N-1) distinct carries. Projection
    onto N-K free code coordinates bounds witnesses by (q/2)^(N-K).
    Dividing by q^(N-1) possible carries gives (2/q)^(K-1).
    """
    if type(bits) is not int or bits < 5 or bits % 2 == 0:
        raise ValueError("odd native field degree >= 5 required")
    if type(trials) is not int or trials < 0:
        raise ValueError("nonnegative integer draw count required")
    N, K, q = bits*bits, bits*bits // 8, 1 << bits
    exponent = (bits-1)*(K-1)
    return {"bits": bits, "N": N, "K": K,
            "witness_count_upper_bound": (q//2)**(N-K),
            "distinct_carries_per_witness": 1 << (N-1),
            "carry_space_size": q**(N-1),
            "inverse_success_bound_log2": exponent,
            "one_draw_upper_bound": Fraction(1, 1 << exponent),
            "trials": trials,
            "any_success_upper_bound": min(Fraction(1), Fraction(trials, 1 << exponent)),
            "scope": "UNIFORM_FULL_CARRY_SPACE_NOT_STRUCTURED_OR_ADAPTIVE_SEARCH",
            "native_hardness_established": False}
