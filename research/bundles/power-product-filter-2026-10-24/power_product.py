"""Classical stabilizer filter for exposed power products, not circuit search.

The implemented ambient group is UT_D(F_p). Polynomial atoms are explicit
SymPy polynomials; positive exponents are binary integers and never expanded.
The caller's mathematical input contract includes primality of p.
"""

from dataclasses import dataclass
from math import factorial

import sympy as sp
from sympy.polys.matrices import DomainMatrix


@dataclass(frozen=True)
class StabilizerResult:
    status: str
    reason: str
    prime: int
    dimension: int
    atom_degrees: tuple
    total_degree: int
    radical_degree_upper_bound: int
    constraint_rows: int
    ambient_lie_dimension: int
    lie_basis: tuple
    group_generators: tuple


def _canonical_matrix(matrix, prime):
    return tuple(tuple(int(entry) % prime for entry in row) for row in sp.Matrix(matrix).tolist())


def exp_upper(matrix, prime):
    matrix = sp.Matrix(matrix)
    d = matrix.rows
    if matrix.cols != d or prime <= d or any(matrix[i, j] for i in range(d) for j in range(i+1)):
        raise ValueError("strict upper triangular matrix and p>D required")
    result, power = sp.eye(d), sp.eye(d)
    for k in range(1, d):
        power = (power*matrix).applyfunc(lambda x: int(x) % prime)
        result += pow(factorial(k), -1, prime)*power
    return _canonical_matrix(result, prime)


def full_ut_basis(d):
    result = []
    for i in range(d):
        for j in range(i+1, d):
            matrix = sp.zeros(d)
            matrix[i, j] = 1
            result.append(tuple(tuple(int(x) for x in row) for row in matrix.tolist()))
    return tuple(result)


def transformed(poly, matrix):
    matrix = sp.Matrix(matrix)
    variables = poly.gens
    if matrix.shape != (len(variables), len(variables)):
        raise ValueError("matrix dimension mismatch")
    substitutions = {x: sum(matrix[i, j]*variables[j] for j in range(len(variables)))
                     for i, x in enumerate(variables)}
    return sp.Poly(poly.as_expr().subs(substitutions, simultaneous=True), *variables,
                   modulus=poly.get_modulus())


def fixes_atoms(atoms, matrix, prime, variables):
    return all(transformed(sp.Poly(atom, *variables, modulus=prime), matrix)
               == sp.Poly(atom, *variables, modulus=prime) for atom in atoms)


def solve_ut_power_product(atoms, exponents, prime, variables):
    """Return generators only under both proved guards; otherwise UNKNOWN.

    The original input IS the exposed product of these atoms to these powers.
    No claim is made that an unrelated circuit has this factorization. The
    solver performs no group enumeration or high-power polynomial expansion.
    """
    atoms, exponents, variables = tuple(atoms), tuple(exponents), tuple(variables)
    d = len(variables)
    if (type(prime) is not int or prime < 3 or not sp.isprime(prime)
            or not d or len(set(variables)) != d
            or any(not isinstance(x, sp.Symbol) for x in variables)):
        raise ValueError("distinct variables and an odd caller-verified prime required")
    if len(atoms) != len(exponents) or any(type(e) is not int or e < 0 for e in exponents):
        raise ValueError("one nonnegative integer exponent per atom required")
    active = [(sp.Poly(atom, *variables, modulus=prime), e)
              for atom, e in zip(atoms, exponents) if e]
    if any(poly.is_zero for poly, _ in active):
        degrees, total, radical = (), 0, 0
        basis = full_ut_basis(d)
        # Adjacent transvections suffice for UT_D, even when p<=D.
        generators = []
        for i in range(d-1):
            matrix = sp.eye(d)
            matrix[i, i+1] = 1
            generators.append(_canonical_matrix(matrix, prime))
        return StabilizerResult("FULL_GROUP", "zero product", prime, d, degrees, total,
                                radical, 0, len(basis), basis, tuple(generators))
    active = [(poly, e) for poly, e in active if poly.total_degree()]
    degrees = tuple(int(poly.total_degree()) for poly, _ in active)
    total = sum(degree*e for degree, (_, e) in zip(degrees, active))
    radical = sum(degrees)
    ambient = d*(d-1)//2

    def unknown(reason):
        return StabilizerResult("OUT_OF_SCOPE", reason, prime, d, degrees, total,
                                radical, 0, ambient, (), ())

    if not active:
        basis = full_ut_basis(d)
        generators = []
        for i in range(d-1):
            matrix = sp.eye(d)
            matrix[i, i+1] = 1
            generators.append(_canonical_matrix(matrix, prime))
        return StabilizerResult("FULL_GROUP", "constant product", prime, d, (), 0, 0,
                                0, ambient, basis, tuple(generators))
    if radical >= prime:
        return unknown("factor-support bound is not strictly below p")
    if prime <= max(d, (d-1)*max(degrees)):
        return unknown("finite-to-infinitesimal atom degree guard failed")
    positions = [(i, j) for i in range(d) for j in range(i+1, d)]
    rows = []
    for poly, _ in active:
        derivatives = [sp.Poly(poly.diff(variables[i]).as_expr()*variables[j], *variables,
                               modulus=prime).as_dict() for i, j in positions]
        monomials = sorted(set().union(*(set(value) for value in derivatives))) if derivatives else []
        rows.extend([[int(value.get(monomial, 0)) % prime for value in derivatives]
                     for monomial in monomials])
    if not positions:
        nullspace = []
    elif not rows:
        nullspace = sp.eye(ambient).tolist()
    else:
        nullspace = DomainMatrix.from_list(rows, sp.GF(prime)).nullspace().to_Matrix().tolist()
    basis = []
    for vector in nullspace:
        matrix = sp.zeros(d)
        for (i, j), value in zip(positions, vector):
            matrix[i, j] = int(value) % prime
        basis.append(_canonical_matrix(matrix, prime))
    generators = tuple(exp_upper(matrix, prime) for matrix in basis)
    # Check every reported group generator against all original active atoms.
    if not all(fixes_atoms([poly.as_expr() for poly, _ in active], matrix, prime, variables)
               for matrix in generators):
        raise ArithmeticError("finite generator check failed")
    return StabilizerResult("CLASSICALLY_SOLVED", "strict factor and atom degree guards",
                            prime, d, degrees, total, radical, len(rows), ambient,
                            tuple(basis), generators)
