"""Classical filter for the actual exposed input P^p - P Q^(p-1).

Only full UT_D(F_p) and explicit polynomial atoms are implemented. Formal
polynomials are never replaced by their functions on the prime field.
The large norm is not expanded. See RESULT.md for both strict guards.
"""

from dataclasses import dataclass
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "power-product-filter-2026-10-24"))
from power_product import exp_upper, transformed


@dataclass(frozen=True)
class PencilResult:
    status: str
    reason: str
    prime: int
    dimension: int
    atom_degrees: tuple
    formal_degree_upper_bound: int
    gradient_separation_bound: int
    infinitesimal_bound: int
    constraint_rows: int
    lie_basis: tuple
    translation_coefficients: tuple
    group_generators: tuple


def pencil_translation(numerator, denominator, matrix):
    """Return b if Q(gx)=Q and P(gx)=P+bQ, otherwise None."""
    if transformed(denominator, matrix) != denominator:
        return None
    difference = transformed(numerator, matrix) - numerator
    monomial, coefficient = denominator.terms()[0]
    prime = int(denominator.get_modulus())
    value = int(difference.coeff_monomial(monomial)) * pow(int(coefficient), -1, prime) % prime
    # Poly.mul_ground(0) can retain noncanonical nested zeros in SymPy 1.14.
    expected = sp.Poly(value * denominator.as_expr(), *denominator.gens, modulus=prime)
    return value if difference == expected else None


def solve_ut_pencil_norm(numerator, denominator, prime, variables):
    """Compute full stabilizer generators under the proved strict bounds.

    P and Q are public input, not factors supplied as hidden advice for an
    unrelated circuit. Runtime is not claimed polynomial in arbitrary
    arithmetic-circuit size: the atom polynomials are expanded here.
    """
    variables = tuple(variables)
    d = len(variables)
    if (type(prime) is not int or prime < 3 or not sp.isprime(prime)
            or not d or len(set(variables)) != d
            or any(not isinstance(x, sp.Symbol) for x in variables)):
        raise ValueError("distinct variables and an odd caller-verified prime required")
    numerator = sp.Poly(numerator, *variables, modulus=prime)
    denominator = sp.Poly(denominator, *variables, modulus=prime)
    degrees = (int(numerator.total_degree()), int(denominator.total_degree()))
    separation = sum(degrees) + 1
    infinitesimal = max(d, (d - 1) * max(degrees))
    norm_degree = max(prime * degrees[0], degrees[0] + (prime - 1) * degrees[1])

    def unknown(reason):
        return PencilResult("OUT_OF_SCOPE", reason, prime, d, degrees,
                            norm_degree, separation, infinitesimal, 0, (), (), ())

    if numerator.is_zero or denominator.is_zero or not degrees[1]:
        return unknown("nonzero P and nonconstant Q required by this filter")
    if prime <= separation:
        return unknown("gradient multiplicity separation bound failed")
    if numerator.gcd(denominator).total_degree() != 0:
        return unknown("coprime P and Q required")
    if prime <= infinitesimal:
        return unknown("finite-to-infinitesimal atom degree bound failed")

    positions = [(i, j) for i in range(d) for j in range(i + 1, d)]
    columns = len(positions) + 1
    rows = []
    # The final unknown b allows a nontrivial permutation of pencil factors.
    for poly, final in ((denominator, {}), (numerator, (-denominator).as_dict())):
        coefficients = [sp.Poly(poly.diff(variables[i]).as_expr() * variables[j],
                                *variables, modulus=prime).as_dict()
                        for i, j in positions] + [final]
        monomials = sorted(set().union(*(set(value) for value in coefficients)))
        rows.extend([[int(value.get(monomial, 0)) % prime for value in coefficients]
                     for monomial in monomials])
    nullspace = DomainMatrix.from_list(rows, sp.GF(prime)).nullspace().to_Matrix().tolist()
    basis, translations = [], []
    for vector in nullspace:
        assert len(vector) == columns
        matrix = sp.zeros(d)
        for (i, j), value in zip(positions, vector[:-1]):
            matrix[i, j] = int(value) % prime
        if matrix.is_zero_matrix:
            raise ArithmeticError("spurious auxiliary-only kernel vector")
        basis.append(tuple(tuple(int(value) for value in row) for row in matrix.tolist()))
        translations.append(int(vector[-1]) % prime)
    generators = tuple(exp_upper(matrix, prime) for matrix in basis)
    for generator, value in zip(generators, translations):
        if pencil_translation(numerator, denominator, generator) != value:
            raise ArithmeticError("finite pencil-generator verification failed")
    return PencilResult("CLASSICALLY_SOLVED", "coprime pencil and both strict degree bounds",
                        prime, d, degrees, norm_degree, separation, infinitesimal,
                        len(rows), tuple(basis), tuple(translations), generators)
