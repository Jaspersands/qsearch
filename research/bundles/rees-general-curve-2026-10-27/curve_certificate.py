"""Exact public algebra certificates, not a quantum source or receiver."""

from dataclasses import dataclass
from fractions import Fraction
from math import ceil, factorial

from sympy import isprime


def positive_integer(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


class Span:
    def __init__(self, p):
        self.p = p
        self.rows = {}

    def add(self, vector):
        residual = {w: v % self.p for w, v in vector.items() if v % self.p}
        for pivot in sorted(self.rows):
            scale = residual.get(pivot, 0)
            if scale:
                for w, v in self.rows[pivot].items():
                    residual[w] = (residual.get(w, 0) - scale * v) % self.p
                    if not residual[w]:
                        del residual[w]
        if not residual:
            return False
        pivot = min(residual)
        inverse = pow(residual[pivot], -1, self.p)
        self.rows[pivot] = {w: v * inverse % self.p for w, v in residual.items()}
        return True

    def __len__(self):
        return len(self.rows)


class WeightedTensor:
    """Free associative words of TOTAL WEIGHT <= c; X_j has weight j."""

    def __init__(self, c, p):
        positive_integer(c, "c")
        positive_integer(p, "p")
        if p <= c or not isprime(p):
            raise ValueError("prime p > c is required")
        self.c, self.p = c, p
        self.one = {(): 1}

    def add(self, a, b):
        out = a.copy()
        for w, x in b.items():
            out[w] = (out.get(w, 0) + x) % self.p
            if not out[w]:
                del out[w]
        return out

    def scale(self, a, scalar):
        return {w: x * scalar % self.p for w, x in a.items() if x * scalar % self.p}

    def mul(self, a, b):
        out = {}
        for u, x in a.items():
            for v, y in b.items():
                if sum(u) + sum(v) <= self.c:
                    w = u + v
                    out[w] = (out.get(w, 0) + x * y) % self.p
        return {w: x for w, x in out.items() if x}

    def bracket(self, a, b):
        return self.add(self.mul(a, b), self.scale(self.mul(b, a), -1))

    def exp(self, a):
        if a.get((), 0):
            raise ValueError("exponential requires augmentation zero")
        out, power = self.one, self.one
        for k in range(1, self.c + 1):
            power = self.mul(power, a)
            out = self.add(out, self.scale(power, pow(factorial(k), -1, self.p)))
        return out

    def a(self, t):
        return {(j,): pow(t, j, self.p) for j in range(1, self.c + 1)
                if t % self.p}

    def a_prime(self, t):
        return {(j,): j * pow(t, j - 1, self.p) % self.p
                for j in range(1, self.c + 1)
                if j * pow(t, j - 1, self.p) % self.p}

    def gamma(self, t, sign=1):
        if sign not in (-1, 1):
            raise ValueError("sign must be -1 or 1")
        return self.exp(self.scale(self.a(t), sign))

    def tangent(self, t):
        """Right logarithmic derivative gamma'(t) gamma(t)^(-1)."""
        out, term = {}, self.a_prime(t)
        for k in range(self.c):
            out = self.add(out, self.scale(term, pow(factorial(k + 1), -1, self.p)))
            term = self.bracket(self.a(t), term)
        return out

    def exp_derivative(self, a, da):
        """Independent noncommutative product-rule differentiation of exp."""
        power, derivative, out = self.one, {}, {}
        for k in range(1, self.c + 1):
            derivative = self.add(self.mul(derivative, a), self.mul(power, da))
            power = self.mul(power, a)
            out = self.add(out, self.scale(derivative, pow(factorial(k), -1, self.p)))
        return out

    def adjoint(self, s, vector):
        return self.mul(self.mul(self.gamma(s), vector), self.gamma(s, -1))

    def lie_basis(self):
        graded = {}
        for weight in range(1, self.c + 1):
            span, vectors = Span(self.p), []
            candidates = [{(weight,): 1}]
            for j in range(1, weight):
                candidates.extend(self.bracket({(j,): 1}, v) for v in graded[weight - j])
            for vector in candidates:
                if span.add(vector):
                    vectors.append(vector)
            graded[weight] = vectors
        return graded


@dataclass(frozen=True)
class OrbitVector:
    t: int
    conjugator: tuple
    vector: dict


def orbit_basis(algebra):
    span, chosen = Span(algebra.p), []
    for t in range(algebra.c):
        vector = algebra.tangent(t)
        if span.add(vector):
            chosen.append(OrbitVector(t, (), vector))
    growth = [len(span)]
    while True:
        before = len(chosen)
        for old in tuple(chosen):
            for s in range(1, algebra.c + 1):
                vector = algebra.adjoint(s, old.vector)
                if span.add(vector):
                    chosen.append(OrbitVector(old.t, (s,) + old.conjugator, vector))
        if len(chosen) == before:
            return chosen, growth, sorted(span.rows)
        growth.append(len(chosen))


def alternating_witness(chosen):
    """(sign, base parameter, variable index or None); padding is gamma(0)."""
    word = []
    for i, item in enumerate(chosen):
        block = [(1, s, None) for s in item.conjugator]
        block += [(1, item.t, i), (-1, item.t, None)]
        block += [(-1, s, None) for s in reversed(item.conjugator)]
        for factor in block:
            expected = -1 if len(word) % 2 == 0 else 1
            if factor[0] != expected:
                word.append((expected, 0, None))
            word.append(factor)
    if len(word) % 2:
        word.append((1, 0, None))
    return word


def word_jacobian(algebra, word, variables):
    values = [algebra.gamma(t, sign) for sign, t, _ in word]
    prefixes = [algebra.one]
    for value in values:
        prefixes.append(algebra.mul(prefixes[-1], value))
    suffixes = [algebra.one for _ in range(len(word) + 1)]
    for j in range(len(word) - 1, -1, -1):
        suffixes[j] = algebra.mul(values[j], suffixes[j + 1])
    derivatives = [{} for _ in range(variables)]
    for j, (sign, t, variable) in enumerate(word):
        if variable is not None:
            dg = algebra.exp_derivative(algebra.scale(algebra.a(t), sign),
                                        algebra.scale(algebra.a_prime(t), sign))
            contribution = algebra.mul(algebra.mul(prefixes[j], dg), suffixes[j + 1])
            derivatives[variable] = algebra.add(derivatives[variable], contribution)
    return prefixes[-1], derivatives


def determinant(matrix, p):
    matrix = [list(row) for row in matrix]
    out = 1
    for i in range(len(matrix)):
        pivot = next((j for j in range(i, len(matrix)) if matrix[j][i] % p), None)
        if pivot is None:
            return 0
        if pivot != i:
            matrix[i], matrix[pivot] = matrix[pivot], matrix[i]
            out = -out
        value = matrix[i][i] % p
        out = out * value % p
        inverse = pow(value, -1, p)
        for j in range(i + 1, len(matrix)):
            ratio = matrix[j][i] * inverse % p
            for k in range(i + 1, len(matrix)):
                matrix[j][k] = (matrix[j][k] - ratio * matrix[i][k]) % p
    return out % p


def theorem_constants(c, dimension):
    positive_integer(c, "c")
    positive_integer(dimension, "dimension")
    m = 2 * dimension**2 + 1
    return {
        "alternating_pairs": m,
        "coordinate_degree_bound": c,
        "minor_degree_bound": dimension * (c - 1),
        "good_fiber_factor": c**dimension,
        "sufficient_prime_threshold": max(16 * c**dimension,
            4 * dimension * (c - 1), 4 * (c - 1)**2, c + 1),
        "gap_lower_bound": f"1/{4*m}",
    }


def certificate(c, p):
    algebra = WeightedTensor(c, p)
    graded = algebra.lie_basis()
    dimension = sum(map(len, graded.values()))
    chosen, growth, pivots = orbit_basis(algebra)
    if len(chosen) != dimension:
        raise ArithmeticError("adjoint orbit does not span the free Lie algebra")
    if max(map(lambda x: len(x.conjugator), chosen)) > dimension - 1:
        raise ArithmeticError("conjugator length exceeds the theorem bound")
    word = alternating_witness(chosen)
    value, derivatives = word_jacobian(algebra, word, dimension)
    if value != algebra.one or derivatives != [x.vector for x in chosen]:
        raise ArithmeticError("independent product derivative contradicts orbit witness")
    matrix = [[v.get(w, 0) for w in pivots] for v in derivatives]
    det = determinant(matrix, p)
    if not det:
        raise ArithmeticError("selected minor is singular")
    constants = theorem_constants(c, dimension)
    if len(word) > 2 * constants["alternating_pairs"]:
        raise ArithmeticError("alternating embedding exceeds the theorem bound")
    return {
        "scope": "finite public algebra certificate, not a quantum run or all-c proof",
        "c": c, "p": p, "dimension": dimension,
        "graded_dimensions": [len(graded[j]) for j in graded],
        "orbit_span_growth": growth,
        "selected_orbit_vectors": [{"t": v.t, "conjugator": list(v.conjugator)} for v in chosen],
        "alternating_word": [list(x) for x in word],
        "selected_tensor_coordinates": [list(w) for w in pivots],
        "derivative_minor_transpose": matrix,
        "minor_determinant_mod_p": det,
        "word_at_witness_is_identity": True,
        "independent_product_derivative_agrees": True,
        "constants": constants,
        "large_prime_gap_certified": p >= constants["sufficient_prime_threshold"],
        "native_source_prepared": False,
        "algorithmic_advantage_certified": False,
    }


def source_plan(c, dimension, p, delta, epsilon, leaves, address_bits, packet_size):
    """Conditional query bound. Does not certify supplied moment design or receiver."""
    WeightedTensor(c, p)
    for value, name in ((dimension, "dimension"), (leaves, "leaves"),
                        (address_bits, "address_bits"), (packet_size, "packet_size")):
        positive_integer(value, name)
    delta, epsilon = Fraction(delta), Fraction(epsilon)
    if not 0 < delta <= 1 or not 0 < epsilon < 1:
        raise ValueError("delta and epsilon must be in (0,1] and (0,1), respectively")
    # D <= 2^c-1 is universal; smaller dimensions require a separate certificate.
    if dimension < 2**c - 1:
        raise ValueError("source planner requires the safe universal dimension upper bound")
    constants = theorem_constants(c, dimension)
    if p < constants["sufficient_prime_threshold"]:
        raise ValueError("large-prime gap threshold is not met")
    gap = Fraction(1, 4 * constants["alternating_pairs"])
    gamma = gap * delta**2 / 2
    target = Fraction(4 * leaves, 1) / epsilon
    log_bound = max(0, target.numerator.bit_length() - target.denominator.bit_length())
    while 2**log_bound < target:
        log_bound += 1
    packets = ceil(Fraction(address_bits + log_bound, 1) / gamma)
    queries = leaves * packets * packet_size
    return {"gap_lower_bound": str(gap), "packet_contraction": str(gamma),
            "packets_per_leaf": packets, "native_copies": queries,
            "coherent_select_calls": queries, "per_select_half_diamond_error": str(epsilon / (8 * queries)),
            "conditional_on": ["pure IID native copies", "stated subgroup-twirl robustness",
                "valid nonzero zero-moment packet of supplied size", "valid receiver leaf cap",
                "address_bits >= log2(address dimension)", "discarded independent scale records"],
            "total_gate_bound_certified": False,
            "uncharged_here": ["native width q", "copy acquisition", "SELECT circuit cost",
                "public arithmetic", "moment design", "field sampling", "receiver"]}
