"""Exact tests of a proposed Rees-to-cyclotomic bridge, NOT a CCP solver.

Polynomial arithmetic is supplied by FLINT. Enumeration is confined to
capped algebraic controls of the published group, never native search.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import comb, gcd, lcm

from flint import fmpq_poly, fmpz, fmpz_mat, fmpz_mod_poly_ctx, fmpz_poly


def parameters(p, t, n=1):
    if type(p) is not int or p < 2 or not fmpz(p).is_prime():
        raise ValueError("a prime p is required")
    if type(t) is not int or t < 1 or type(n) is not int or n < 1:
        raise ValueError("positive integer exponent and dimension required")
    L = t*(p-1)
    return {"p": p, "t": t, "n": n, "q": p**t, "class": L,
            "class_less_than_p": L < p,
            "prime_field_exponent_p_input": t == 1,
            "group_order_log_p": n*L+1,
            "hidden_order_log_p": 1,
            "hidden_index_log_p": n*L,
            "normalizer_order_log_p": n+1,
            "derived_dimension_when_t_one": n*(p-2) if t == 1 else None,
            "q_at_most_two_to_class": p <= 2**(p-1),
            "growing_modulus_fixed_class_bridge_established": False}


def fermat_null_polynomial(p, t):
    """Nonzero positive-degree coefficients; zero function on Z/p^t."""
    data = parameters(p, t)
    if t < 2:
        raise ValueError("this filtered-grade obstruction uses t >= 2")
    q, a = data["q"], p**(t-1)
    coefficients = [0]*(p+1)
    coefficients[1], coefficients[p] = (-a) % q, a
    return coefficients


def evaluate_mod(coefficients, x, modulus):
    value = 0
    for c in reversed(coefficients):
        value = (value*x+c) % modulus
    return value


def newton_dilation(degree, scale):
    """Exact coefficients of binom(scale*T,degree) in binom(T,j)."""
    if type(degree) is not int or degree < 1:
        raise ValueError("positive integer degree required")
    if type(scale) is not int or scale < 1:
        raise ValueError("positive integer scale required")
    return [sum((-1)**(j-k)*comb(j, k)*comb(scale*k, degree)
                for k in range(j+1)) for j in range(degree+1)]


def newton_dilation_matrix(degree, scale):
    """Columns are dilated positive-degree Newton basis vectors."""
    columns = [newton_dilation(j, scale) for j in range(1, degree+1)]
    if not columns:
        raise ValueError("positive integer degree required")
    return fmpz_mat([[column[i] if i < len(column) else 0 for column in columns]
                     for i in range(1, degree+1)])


@dataclass
class CyclotomicRing:
    p: int
    t: int

    def __post_init__(self):
        data = parameters(self.p, self.t)
        self.q, self.L = data["q"], data["class"]
        self.ctx = fmpz_mod_poly_ctx(self.q)
        self.modulus = self.ctx([1]*self.p)
        self.zero, self.one = (0,)*(self.p-1), (1,)+(0,)*(self.p-2)
        self.zeta = self.canonical(self.ctx.gen())
        self.pi = self.sub(self.zeta, self.one)
        self.rational_modulus = fmpq_poly([1]*self.p)
        generator = fmpq_poly([0, 1])
        divisor, inverse, _ = (generator-1).xgcd(self.rational_modulus)
        if divisor != 1:
            raise ArithmeticError("cyclotomic rational inverse failed")
        self.dual_scale = (inverse**(self.L-1) % self.rational_modulus)/self.p

    def canonical(self, polynomial):
        polynomial = polynomial % self.modulus
        return tuple(int(polynomial[i]) for i in range(self.p-1))

    def element(self, values):
        if len(values) != self.p-1 or any(type(x) is not int or not 0 <= x < self.q for x in values):
            raise ValueError("canonical coefficient tuple required")
        return tuple(values)

    def scalar(self, value):
        return (value % self.q,)+(0,)*(self.p-2)

    def add(self, x, y):
        return self.canonical(self.ctx(list(self.element(x)))+self.ctx(list(self.element(y))))

    def sub(self, x, y):
        return self.canonical(self.ctx(list(self.element(x)))-self.ctx(list(self.element(y))))

    def mul(self, x, y):
        return self.canonical(self.ctx(list(self.element(x)))*self.ctx(list(self.element(y))))

    def power(self, x, exponent):
        if type(exponent) is not int or exponent < 0:
            raise ValueError("nonnegative exponent required")
        return self.canonical(self.ctx(list(self.element(x))).pow_mod(exponent, self.modulus))

    def elements(self, cap=4096):
        if self.q**(self.p-1) > cap:
            raise ValueError("finite ring control exceeds enumeration cap")
        return tuple(product(range(self.q), repeat=self.p-1))

    def ideal(self, power, cap=4096):
        generator = self.power(self.pi, power)
        return {self.mul(generator, x) for x in self.elements(cap)}

    def lam(self, j):
        if type(j) is not int or not 0 <= j <= self.p:
            raise ValueError("j in [0,p] required")
        value = self.zero
        for k in range(j):
            value = self.add(value, self.power(self.zeta, k))
        return value

    def group_mul(self, g, h):
        x, a = g
        y, b = h
        if type(a) is not int or type(b) is not int or not 0 <= a < self.p or not 0 <= b < self.p:
            raise ValueError("canonical F_p coordinate required")
        return self.add(x, self.mul(self.power(self.zeta, a), y)), (a+b) % self.p

    def group_inverse(self, g):
        x, a = g
        return self.sub(self.zero, self.mul(self.power(self.zeta, (-a) % self.p), x)), (-a) % self.p

    def commutator(self, g, h):
        return self.group_mul(self.group_mul(g, h),
                              self.group_mul(self.group_inverse(g), self.group_inverse(h)))

    def hidden(self, secret):
        return {(self.mul(self.lam(j), self.scalar(secret)), j) for j in range(self.p)}

    def character_exponent(self, x, y):
        """Tr(x*y/(p*pi^(L-1))) modulo 1, retaining the ramified dual."""
        polynomial = (fmpq_poly(list(self.element(x)))*fmpq_poly(list(self.element(y)))
                      *self.dual_scale) % self.rational_modulus
        value = (self.p-1)*polynomial[0]-sum(polynomial[j] for j in range(1, self.p-1))
        return Fraction(int(value.numerator), int(value.denominator)) % 1

    def pairing_matrix(self):
        basis = [self.power(self.zeta, j) for j in range(self.p-1)]
        rows = []
        for x in basis:
            row = []
            for y in basis:
                entry = self.q*self.character_exponent(x, y)
                if entry.denominator != 1:
                    raise ArithmeticError("character exceeds the additive exponent")
                row.append(entry.numerator % self.q)
            rows.append(row)
        if gcd(int(fmpz_mat(rows).det()), self.q) != 1:
            raise ArithmeticError("degenerate cyclotomic pairing")
        return rows

    def phase(self, label, secret):
        return tuple(self.character_exponent(label, self.mul(self.lam(j), self.scalar(secret)))
                     for j in range(self.p))


def exact_phase_fidelity(left, right, denominator_cap=81):
    if len(left) != len(right) or not left:
        raise ValueError("equal nonempty phase lists required")
    phases = [Fraction(b-a) % 1 for a, b in zip(left, right)]
    denominator = lcm(*(x.denominator for x in phases))
    if denominator > denominator_cap:
        raise ValueError("exact cyclotomic control exceeds denominator cap")
    coefficients = [0]*denominator
    for a in phases:
        for b in phases:
            coefficients[int((a-b)*denominator) % denominator] += 1
    modulus = fmpq_poly(list(fmpz_poly.cyclotomic(denominator)))
    answer = (fmpq_poly(coefficients)/len(phases)**2) % modulus
    if answer.degree() > 0:
        raise ValueError("this control's fidelity is algebraic rather than rational")
    value = answer[0]
    return Fraction(int(value.numerator), int(value.denominator))
