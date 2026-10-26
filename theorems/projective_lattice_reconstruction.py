"""Classical reconstruction given an explicit positive integral Hom lattice.

The input is ALREADY coordinates in a supplied lattice basis, not geometric
torsion points. This neither computes Hom(A,B) nor breaks the weak-isogeny
source without that extra input. See SIEGEL_HOM_LATTICE_BASELINE.md.
"""

from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from math import gcd, prod

from flint import fmpz, fmpz_mat


@dataclass(frozen=True)
class ProjectiveReconstruction:
    status: str
    primitive_vector: tuple[int, ...] | None
    squared_norm: int | None
    product_level: int
    lll_verified: bool
    reason: str


def _ldl(gram):
    """Exact Gram-Schmidt coefficients and squared lengths for a Gram matrix."""
    n = len(gram)
    mu = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    lengths = []
    for i in range(n):
        for j in range(i):
            mu[i][j] = (Fraction(gram[i][j]) - sum(
                mu[i][k] * mu[j][k] * lengths[k] for k in range(j)
            )) / lengths[j]
        length = Fraction(gram[i][i]) - sum(mu[i][k]**2 * lengths[k] for k in range(i))
        if length <= 0:
            raise ValueError("Gram matrix must be positive definite")
        lengths.append(length)
    return mu, lengths


def _inputs(gram, marks, squared_norm_bound):
    gram = tuple(tuple(row) for row in gram)
    n = len(gram)
    if not n or any(len(row) != n for row in gram):
        raise ValueError("Gram matrix must be nonempty and square")
    if any(type(x) is not int for row in gram for x in row):
        raise ValueError("Gram entries must be integers")
    if any(gram[i][j] != gram[j][i] for i in range(n) for j in range(n)):
        raise ValueError("Gram matrix must be symmetric")
    _ldl(gram)
    if type(squared_norm_bound) is not int or squared_norm_bound < 1:
        raise ValueError("squared norm bound must be a positive integer")
    checked, primes = [], set()
    for prime, vector in marks:
        if type(prime) is not int or prime < 2 or not fmpz(prime).is_prime():
            raise ValueError("each auxiliary modulus must be prime")
        if prime in primes:
            raise ValueError("auxiliary primes must be distinct")
        vector = tuple(vector)
        if len(vector) != n or any(type(x) is not int for x in vector):
            raise ValueError("each mark needs one integer per lattice coordinate")
        vector = tuple(x % prime for x in vector)
        if not any(vector):
            raise ValueError("zero marks do not define projective lines")
        checked.append((prime, vector))
        primes.add(prime)
    if not checked:
        raise ValueError("at least one nonzero projective mark is required")
    return gram, tuple(checked)


def _matches(vector, marks):
    for prime, mark in marks:
        pivot = next(i for i, x in enumerate(mark) if x != 0)
        scalar = vector[pivot] * pow(mark[pivot], -1, prime) % prime
        if scalar == 0 or any((x - scalar*y) % prime for x, y in zip(vector, mark)):
            return False
    return True


def _line_lattice(n, marks):
    """Row basis for integer vectors whose residues lie in the marked lines.

    Zero residues are allowed in the lattice. They are NOT valid projective
    marks; primitive-vector verification below separately rejects them.
    """
    basis = [[int(i == j) for j in range(n)] for i in range(n)]
    for prime, mark in marks:
        pivot = next(i for i, x in enumerate(mark) if x != 0)
        for coordinate in range(n):
            if coordinate == pivot:
                continue
            values = [(mark[pivot]*row[coordinate] - mark[coordinate]*row[pivot]) % prime
                      for row in basis]
            index = next((i for i, x in enumerate(values) if x != 0), None)
            if index is None:
                continue
            old = basis[index][:]
            inverse = pow(values[index], -1, prime)
            for i in range(n):
                if i != index:
                    multiple = values[i] * inverse % prime
                    basis[i] = [x - multiple*y for x, y in zip(basis[i], old)]
            basis[index] = [prime*x for x in old]
    return fmpz_mat(basis)


def _exact_lll_check(reduced, transform, original):
    n = original.nrows()
    if abs(int(transform.det())) != 1 or transform * original * transform.transpose() != reduced:
        return False
    try:
        mu, lengths = _ldl([[int(reduced[i, j]) for j in range(n)] for i in range(n)])
    except ValueError:
        return False
    # Conservative rational checks below FLINT's requested (0.99, 0.51).
    # delta - eta^2 = 0.54 > 1/2 gives the usual 2^(n-1) squared-length bound.
    return (all(abs(mu[i][j]) <= Fraction(3, 5) for i in range(n) for j in range(i))
            and all(lengths[i] >= (Fraction(9, 10) - mu[i][i-1]**2) * lengths[i-1]
                    for i in range(1, n)))


def reconstruct_projective_vector(gram, marks, squared_norm_bound):
    """Recover a primitive bounded vector up to one GLOBAL sign, or UNKNOWN.

    marks contains (prime, nonzero coordinate vector), with a separate
    unknown unit scalar at every prime. A UNIQUE_PRIMITIVE_LINE result
    certifies uniqueness only in this supplied integral lattice and norm
    bound. It does not verify the lattice's geometric provenance, fullness,
    the original isogeny promise, or the ability to evaluate basis maps.
    """
    gram, marks = _inputs(gram, marks, squared_norm_bound)
    n, level = len(gram), prod(prime for prime, _ in marks)
    basis = _line_lattice(n, marks)
    original = basis * fmpz_mat(gram) * basis.transpose()
    reduced, transform = original.lll(transform=True, rep="gram", gram="exact")
    verified = _exact_lll_check(reduced, transform, original)
    if not verified:
        return ProjectiveReconstruction("UNKNOWN", None, None, level, False,
                                        "exact LLL certificate failed")
    row = transform * basis
    vector = tuple(int(row[0, i]) for i in range(n))
    divisor = reduce(gcd, vector, 0)
    if divisor == 0:
        return ProjectiveReconstruction("UNKNOWN", None, None, level, True,
                                        "zero reduction output")
    vector = tuple(x // divisor for x in vector)
    if next(x for x in vector if x != 0) < 0:
        vector = tuple(-x for x in vector)
    norm = sum(vector[i] * gram[i][j] * vector[j] for i in range(n) for j in range(n))
    if not _matches(vector, marks):
        return ProjectiveReconstruction("UNKNOWN", vector, norm, level, True,
                                        "primitive normalization lost a projective mark")
    if norm > squared_norm_bound:
        return ProjectiveReconstruction("UNKNOWN", vector, norm, level, True,
                                        "candidate exceeds the supplied norm bound")
    if level**2 <= squared_norm_bound * norm:
        return ProjectiveReconstruction("UNKNOWN", vector, norm, level, True,
                                        "strict exterior-product separation is not certified")
    return ProjectiveReconstruction("UNIQUE_PRIMITIVE_LINE", vector, norm, level, True,
                                    "unique primitive bounded vector up to global sign")
