"""Exact local controls for terminal interpolation closure and cross-map escape.

Matrices are supplied Tate-coordinate witnesses, not geometric computations.
No claim about native intermediate PPAV automorphisms is made.
"""

from math import gcd
from pathlib import Path
from random import SystemRandom
import sys

from sympy import Matrix, Rational, eye, isprime, kronecker_product, zeros

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "product-corner-attack-2026-10-23"))
from product_corners import rank_mod
sys.path.insert(0, str(ROOT / "source-algebra-splitting-2026-10-25"))
from source_split import square_root


def require_prime(q):
    if type(q) is not int or not isprime(q):
        raise ValueError("prime local level required")


def rational(value):
    value = Matrix(value)
    if any(x.is_Rational is not True for x in value):
        raise ValueError("exact rational matrix required")
    return value


def integral_at(value, q):
    require_prime(q)
    return all(x.q % q for x in rational(value))


def units():
    return tuple(Matrix(2, 2, [int(i == j) for i in range(4)]) for j in range(4))


def adjoint(value):
    value = rational(value)
    if value.rows != value.cols or value.rows % 2 or value.rows == 0:
        raise ValueError("nonempty square even-dimensional matrix required")
    j = kronecker_product(eye(value.rows//2), Matrix([[0, 1], [-1, 0]]))
    return -j*value.T*j


def target_basis(q):
    require_prime(q)
    e11, e12, e21, _ = units()
    return Matrix.hstack(*(Matrix(list(x)) for x in (eye(2), q*e11, q*q*e12, e21)))


def target_contains(value, q):
    value = rational(value)
    if value.shape != (2, 2):
        raise ValueError("elliptic target block required")
    return integral_at(target_basis(q).inv()*Matrix(list(value)), q)


def category_contains(value, q, copies=1):
    """Known block order for nonisomorphic curves and scalar target units."""
    require_prime(q)
    value = rational(value)
    if type(copies) is not int or copies < 1 or value.shape != (4*copies, 4*copies):
        raise ValueError("source/target product block dimensions disagree")
    phi, dual = Matrix.diag(q, 1), Matrix.diag(1, q)
    for i in range(2*copies):
        for j in range(2*copies):
            block = value[2*i:2*i+2, 2*j:2*j+2]
            if i < copies and j < copies:
                good = integral_at(block, q)
            elif i < copies:
                good = integral_at(block*dual.inv(), q)
            elif j < copies:
                good = integral_at(phi.inv()*block, q)
            else:
                good = target_contains(block, q)
            if not good:
                return False
    return True


def category_basis(q):
    require_prime(q)
    phi, dual = Matrix.diag(q, 1), Matrix.diag(1, q)
    result = []
    for i, j in ((0, 0), (0, 1), (1, 0), (1, 1)):
        values = units()
        if (i, j) == (0, 1):
            values = tuple(a*dual for a in values)
        elif (i, j) == (1, 0):
            values = tuple(phi*a for a in values)
        elif (i, j) == (1, 1):
            values = tuple(Matrix(2, 2, list(target_basis(q)[:, k])) for k in range(4))
        for a in values:
            matrix = zeros(4)
            matrix[2*i:2*i+2, 2*j:2*j+2] = a
            result.append(matrix)
    return tuple(result)


def interpolation_diamond(q, roots):
    require_prime(q)
    if len(roots) != 4 or any(type(x) is not int for x in roots):
        raise ValueError("four integer roots required")
    a, b, c, d = roots
    scalar = Matrix([[a, -b, -c, -d], [b, a, d, -c],
                     [c, -d, a, b], [d, c, -b, a]])
    multiplier = q+sum(x*x for x in roots)
    if multiplier <= q or gcd(multiplier, q) != 1:
        raise ValueError("positive auxiliary norm coprime to q required")
    phi, dual = Matrix.diag(q, 1), Matrix.diag(1, q)
    upper = kronecker_product(scalar, eye(2)).row_join(kronecker_product(eye(4), dual))
    lower = (-kronecker_product(eye(4), phi)).row_join(kronecker_product(scalar.T, eye(2)))
    psi = upper.col_join(lower)
    if adjoint(psi)*psi != multiplier*eye(16) or psi*adjoint(psi) != multiplier*eye(16):
        raise ArithmeticError("polarized interpolation identity failed")
    return psi, multiplier


def terminal_generators():
    """Controls for source-unit and within-type permutation ambiguities.

    The proof allows all source units. These are illustrative generators for
    a j=1728 source and a generic target with units +/-1, not native outputs.
    """
    result = []
    source_unit = eye(16)
    source_unit[:2, :2] = Matrix([[0, -1], [1, 0]])
    result.append(source_unit)
    target_unit = eye(16)
    target_unit[8:10, 8:10] = -eye(2)
    result.append(target_unit)
    for offset in (0, 4):
        for i in range(3):
            p = eye(8)
            p.row_swap(offset+i, offset+i+1)
            result.append(kronecker_product(p, eye(2)))
    return tuple(result)


def cross_completion_rank(eta, q):
    """Rank of 16 transported native-map patterns plus identity modulo q."""
    require_prime(q)
    eta = rational(eta)
    if eta.shape != (2, 2) or any(x.q != 1 for x in eta):
        raise ValueError("integral local cross-map matrix required")
    phi = Matrix.diag(q, 1)
    maps = [eye(2)]
    maps += [left*a*adjoint(right)
             for left in (phi, eta) for right in (phi, eta) for a in units()]
    return rank_mod(Matrix.hstack(*(Matrix(list(x)) for x in maps)), q)


def cross_is_new(eta, q):
    eta = rational(eta)
    if eta.shape != (2, 2) or not integral_at(eta, q):
        raise ValueError("q-integral local cross-map required")
    return not integral_at(Matrix.diag(Rational(1, q), 1)*eta, q)


def cross_escape_from_source_coordinates(phi_dual_eta, q):
    """Native use requires actual O0 coordinates of phi^dagger*eta."""
    require_prime(q)
    value = rational(phi_dual_eta)
    if value.shape != (4, 1) or any(x.q != 1 for x in value):
        raise ValueError("four integral source-order coordinates required")
    return any(int(x) % q for x in value)


def target_escape_from_source_coordinates(phi_dual_x_phi, q):
    """Requires actual source coordinates in a basis whose first element is 1."""
    require_prime(q)
    value = rational(phi_dual_x_phi)
    if value.shape != (4, 1) or any(x.q != 1 for x in value):
        raise ValueError("four integral source-order coordinates required")
    return bool(int(value[0]) % q or any(int(x) % (q*q) for x in value[1:]))


def residue(value, q):
    if not integral_at(value, q):
        raise ValueError("q-integral residue required")
    return rational(value).applyfunc(lambda x: int(x.p)*pow(int(x.q), -1, q) % q)


def normalize_line(vector, q):
    a, b = (int(x) % q for x in vector)
    if a:
        return (1, b*pow(a, -1, q) % q)
    if b:
        return (0, 1)
    raise ValueError("nonzero projective vector required")


def in_leaf(value, line, q):
    frame = Matrix([[1, 0], [line[1], q]]) if line[0] else Matrix.diag(q, 1)
    return integral_at(frame.inv()*value*frame, q)


def leaf_candidates(value, q, rng=None, trials=64):
    """At most two neighbors from one new endomorphism in CENTER coordinates.

    NO_NEW_LOCAL_INFORMATION does not enumerate all q+1 leaves. Empty results
    indicate an inconsistent local promise, not a native nonmembership proof.
    A sampling timeout propagates as UNKNOWN, never as an empty candidate set.
    """
    require_prime(q)
    if q == 2:
        raise ValueError("odd prime required for the quadratic-root selector")
    value = rational(value)
    if value.shape != (2, 2):
        raise ValueError("two-dimensional local matrix required")
    result = {"status": "INCONSISTENT_WITH_NEIGHBOR_PROMISE", "lines": [],
              "native_certification_performed": False}
    if not integral_at(value, q):
        if not integral_at(q*value, q):
            return result
        pole = residue(q*value, q)
        if residue(pole*pole, q) != zeros(2):
            return result
        column = next((pole[:, j] for j in range(2) if pole[:, j] != zeros(2, 1)), None)
        if column is None:
            raise ArithmeticError("nonintegral matrix has no residue pole")
        lines = [normalize_line(column, q)]
    else:
        reduced = residue(value, q)
        if reduced[0, 1] == reduced[1, 0] == 0 and reduced[0, 0] == reduced[1, 1]:
            result["status"] = "NO_NEW_LOCAL_INFORMATION"
            return result
        trace = int(reduced.trace()) % q
        discriminant = int(trace*trace-4*reduced.det()) % q
        if discriminant and pow(discriminant, (q-1)//2, q) != 1:
            return result
        root, _ = square_root(discriminant, q, rng or SystemRandom(), trials)
        eigenvalues = sorted({(trace+s*root)*pow(2, -1, q) % q for s in (-1, 1)})
        lines = []
        for eigenvalue in eigenvalues:
            shifted = residue(reduced-eigenvalue*eye(2), q)
            row = next(shifted[i, :] for i in range(2) if shifted[i, :] != zeros(1, 2))
            lines.append(normalize_line((-row[1], row[0]), q))
    lines = sorted(set(line for line in lines if in_leaf(value, line, q)))
    if lines:
        result.update(status="CANDIDATES", lines=lines)
    return result
