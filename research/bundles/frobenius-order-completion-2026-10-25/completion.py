"""Exact controls for a public-endomorphism completion attack.

Local matrices and integral quaternion coordinates below are proof controls,
not secret-torsion or geometric-endomorphism access granted to an attacker.
The weak-action interface only consumes public auxiliary-torsion matrices.
"""

from itertools import product
from pathlib import Path
import sys

from flint import fmpz_mod_poly_ctx, fq_default_ctx
from sympy import Matrix, eye, isprime, zeros
from sympy.matrices.normalforms import hermite_normal_form
from sympy.ntheory.modular import crt

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/"product-corner-attack-2026-10-23"))
from product_corners import (alternating_form, integer_matrix, matrix_multiply, matrix_star,
                             mod, rank_mod, transport_generators)


def recover_frobenius_polynomial(q, records):
    """Reconstruct from genuine public auxiliary actions; no secret-prime points."""
    if type(q) is not int or q < 2:
        raise ValueError("positive field size required")
    primes, first, second = [], [], []
    form = alternating_form(2)
    for r, action in records:
        if type(r) is not int or r == 2 or not isprime(r) or q % r == 0 or r in primes:
            raise ValueError("distinct odd auxiliary primes coprime to q required")
        action = Matrix(action)
        if action.shape != (4, 4) or mod(action.T*form*action-q*form, r) != zeros(4):
            raise ValueError("invalid polarized Frobenius action")
        coefficients = [int(x) % r for x in action.charpoly().all_coeffs()]
        if coefficients[4] != q*q % r or coefficients[3] != q*coefficients[1] % r:
            raise ValueError("nonreciprocal auxiliary characteristic polynomial")
        primes.append(r)
        first.append(coefficients[1])
        second.append(coefficients[2])
    modulus = 1
    for r in primes:
        modulus *= r
    if modulus <= 12*q:
        return {"status": "UNKNOWN_INSUFFICIENT_CRT", "modulus": modulus,
                "required_strict_lower_bound": 12*q, "coefficients": None}
    centered = lambda residues: int(crt(primes, residues, symmetric=True)[0])
    a1, a2 = centered(first), centered(second)
    if a1*a1 > 16*q or abs(a2) > 6*q:
        raise ValueError("reconstructed coefficients violate Weil bounds")
    return {"status": "RECONSTRUCTED_CONDITIONAL", "modulus": modulus,
            "required_strict_lower_bound": 12*q,
            "coefficients": [q*q, q*a1, a2, a1, 1],
            "geometric_input_verified": False}


def spectral_gate(coefficients, multiplier, ell):
    """Sufficient all-Lagrangian criterion, conditional on genuine geometry."""
    if type(ell) is not int or ell == 2 or not isprime(ell):
        raise ValueError("odd prime ell required")
    if type(multiplier) is not int or multiplier % ell == 0:
        raise ValueError("integer multiplier coprime to ell required")
    if len(coefficients) != 5 or coefficients[-1] != 1:
        raise ValueError("monic degree-four characteristic polynomial required")
    ctx = fmpz_mod_poly_ctx(ell)
    polynomial = ctx(list(coefficients))
    if int(polynomial[0]) != multiplier**2 % ell:
        raise ValueError("wrong surface similitude determinant")
    _, factors = polynomial.factor()
    rows, issues = [], []
    reconstructed = ctx([1])
    for factor, multiplicity in factors:
        degree = factor.degree()
        constant_inverse = pow(int(factor[0]), -1, ell)
        dual = ctx([int(factor[degree-j])*pow(multiplier, degree-j, ell)*constant_inverse % ell
                    for j in range(degree+1)])
        self_dual = dual == factor
        rows.append({"factor": [int(factor[j]) for j in range(degree+1)],
                     "multiplicity": multiplicity, "degree": degree,
                     "self_reciprocal_for_multiplier": self_dual})
        reconstructed *= factor**multiplicity
        if multiplicity != 1:
            issues.append("repeated irreducible factor")
        if degree % 2:
            issues.append("odd-dimensional factor")
        if not self_dual:
            issues.append("reciprocally paired distinct factors")
    if reconstructed != polynomial:
        raise ArithmeticError("factorization reconstruction failed")
    rows.sort(key=lambda row: row["factor"])
    return {"ell": ell, "multiplier": multiplier,
            "all_lagrangians_cyclic_sufficient": not issues,
            "status": "SUFFICIENT_CONDITIONAL" if not issues else "UNKNOWN",
            "issues": sorted(set(issues)), "factors": rows,
            "geometric_input_verified": False}


def local_completion(plane, gamma, ell):
    """Check literal span of gamma^i N (gamma^dagger)^j at the secret prime."""
    if type(ell) is not int or ell == 2 or not isprime(ell):
        raise ValueError("odd prime ell required")
    plane, gamma, form = Matrix(plane), Matrix(gamma), alternating_form(2)
    if plane.shape != (4, 2) or gamma.shape != (4, 4):
        raise ValueError("surface matrices required")
    if rank_mod(plane, ell) != 2 or mod(plane.T*form*plane, ell) != zeros(2):
        raise ValueError("Lagrangian plane required")
    powers = [mod(gamma**i, ell) for i in range(3)]
    star = [mod(form.inv()*power.T*form, ell) for power in powers]
    ranks, span_ranks = [], []
    for cutoff in range(3):
        ranks.append(int(rank_mod(Matrix.hstack(*(power*plane for power in powers[:cutoff+1])), ell)))
        images = []
        for a, b in product(range(2), repeat=2):
            elementary = zeros(2)
            elementary[a, b] = 1
            base = plane*elementary*plane.T*form
            for i, j in product(range(cutoff+1), repeat=2):
                images.append(Matrix(list(mod(powers[i]*base*star[j], ell))))
        span_ranks.append(int(rank_mod(Matrix.hstack(*images), ell)))
    return {"cyclic_space_ranks": ranks, "literal_matrix_span_ranks": span_ranks,
            "full_after_two_powers": span_ranks[-1] == 16,
            "secret_plane_used_for_control_only": True}


def weak_completion_actions(source_actions, weak_action, gamma_action, ell, auxiliary_prime, multiplier):
    """No K, target order, Hom basis, or ell-torsion input."""
    r = auxiliary_prime
    if type(r) is not int or r == 2 or not isprime(r) or (ell*multiplier) % r == 0:
        raise ValueError("odd auxiliary prime coprime to ell and multiplier required")
    w, gamma = mod(Matrix(weak_action), r), mod(Matrix(gamma_action), r)
    if w.shape != (4, 4) or gamma.shape != (4, 4) or len(source_actions) != 16:
        raise ValueError("full surface action interface required")
    form = alternating_form(2)
    if mod(gamma.T*form*gamma-multiplier*form, r) != zeros(4):
        raise ValueError("public map is not a polarized similitude")
    inverse = w.inv_mod(r)
    star = mod(multiplier*gamma.inv_mod(r), r)
    powers, adjoints = [mod(gamma**i, r) for i in range(3)], [mod(star**i, r) for i in range(3)]
    actions = []
    for source in source_actions:
        transported = mod(ell*w*Matrix(source)*inverse, r)
        for i, j in product(range(3), repeat=2):
            actions.append(mod(powers[i]*transported*adjoints[j], r))
    return tuple(actions)


def integral_completion(order, phi, gamma):
    """HNF of the genuine integral map lattice in supplied reference coordinates."""
    unit = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    powers = [unit]
    for _ in range(2):
        powers.append(matrix_multiply(order, powers[-1], gamma))
    stars = [matrix_star(order, power) for power in powers]
    generators = []
    for transported in transport_generators(order, phi):
        for left, right in product(powers, stars):
            generators.append(matrix_multiply(order, matrix_multiply(order, left, transported), right))
    return hermite_normal_form(integer_matrix(Matrix.hstack(*generators)))


def lagrangians(ell, cap=1000):
    """Capped complete surface control in the block-diagonal symplectic basis."""
    if not isprime(ell) or ell == 2:
        raise ValueError("odd prime required")
    if (ell+1)*(ell*ell+1) > cap:
        raise ValueError("Lagrangian control exceeds enumeration cap")
    lines = [Matrix([1, 0])]+[Matrix([z, 1]) for z in range(ell)]
    for first, second in product(lines, repeat=2):
        plane = zeros(4, 2)
        plane[:2, 0], plane[2:, 1] = first, second
        yield plane
    for entries in product(range(ell), repeat=4):
        gluing = Matrix(2, 2, entries)
        if int(gluing.det()) % ell == ell-1:
            yield eye(2).col_join(gluing)


def curve_control():
    """Actual C/F_5: y^2=x^5+2x, not a supplied-isogeny execution."""
    p = 5
    ctx = fmpz_mod_poly_ctx(p)
    f = ctx([0, 2, 0, 0, 0, 1])
    assert f.gcd(f.derivative()) == 1
    powered = f**((p-1)//2)
    cartier = [[int(powered[p*i-j]) for j in (1, 2)] for i in (1, 2)]
    counts = []
    for degree in (1, 2):
        field = fq_default_ctx(p, degree, "u")
        generator = field.gen()
        elements = [sum((field(c)*generator**j for j, c in enumerate(coefficients)), field(0))
                    for coefficients in product(range(p), repeat=degree)]
        q = p**degree
        count = 1
        direct = 1
        for x in elements:
            value = x**5+2*x
            if value == 0:
                character = 0
            else:
                power = value**((q-1)//2)
                assert power == 1 or power == -1
                character = 1 if power == 1 else -1
            count += 1+character
            direct += sum(y*y == value for y in elements)
        assert count == direct
        counts.append(count)
    a1 = counts[0]-p-1
    numerator = counts[1]-p*p-1+a1*a1
    assert numerator % 2 == 0
    a2 = numerator//2
    return {"p": p, "curve_coefficients": [0, 2, 0, 0, 0, 1],
            "smooth": True, "cartier_manin": cartier,
            "point_counts_degrees_one_two": counts,
            "characteristic_polynomial": [p*p, p*a1, a2, a1, 1],
            "supplied_weak_isogeny_constructed": False,
            "geometric_endomorphism_lattice_extracted": False}
