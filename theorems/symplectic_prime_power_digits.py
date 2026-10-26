"""Public queries for Siegel HSP digit lifting over Z/p**length.

No HSP/HPGP learner is implemented. The caller supplies a verified odd
prime, a valid graph chart, and a previously certified digit prefix.
Query construction never receives the unknown next digit. Arithmetic
over general chain rings is a written reduction, not this backend.
"""
from itertools import combinations_with_replacement

from theorems.symplectic_socle_probes import (
    add, elementary, eye, multiply, scale, symplectic_form, transpose,
)


def _scope(prime, length):
    if type(prime) is not int or prime < 3 or prime % 2 == 0:
        raise ValueError("a supplied verified odd prime is required")
    if type(length) is not int or length < 2:
        raise ValueError("ring length must be an integer at least two")
    return prime**length


def _symmetric(matrix, modulus, n=None):
    result = tuple(tuple(row) for row in matrix)
    n = len(result) if n is None else n
    if n < 2 or len(result) != n or any(len(row) != n for row in result):
        raise ValueError("symmetric matrices of the declared rank >=2 required")
    if any(type(x) is not int or not 0 <= x < modulus for row in result for x in row):
        raise ValueError("canonical matrix entries required")
    if result != transpose(result):
        raise ValueError("symmetric matrix required")
    return result


def _scalar(t, prime):
    if type(t) is not int or not 0 <= t < prime:
        raise ValueError("canonical prime-field scalar required")


def _lower(matrix):
    n = len(matrix)
    return tuple(tuple(int(r == c) + (matrix[r-n][c] if r >= n and c < n else 0)
                       for c in range(2*n)) for r in range(2*n))


def _levi(a, inverse_transpose):
    n = len(a)
    return tuple(tuple(a[r][c] if r < n and c < n else
                       inverse_transpose[r-n][c-n] if r >= n and c >= n else 0
                       for c in range(2*n)) for r in range(2*n))


def socle_shift(x, prime, length):
    modulus = _scope(prime, length)
    x = _symmetric(x, prime)
    return _lower(scale(x, prime**(length-1), modulus))


def scalar_digit_query(prefix, x, t, digit, prime, length):
    """A lawful query with label F0(X-2*t*S_digit), for 1<=digit<length-1.

    The exact ring correction uses only the known prefix. Replacing it by
    its residue-field value discards carries and can change oracle fibers.
    """
    modulus = _scope(prime, length)
    if type(digit) is not int or not 1 <= digit < length-1:
        raise ValueError("scalar probes apply only to intermediate digits")
    prefix = _symmetric(prefix, prime**digit)
    x = _symmetric(x, prime, len(prefix))
    _scalar(t, prime)
    unit = (1 + prime**(length-1-digit)*t) % modulus
    inverse = pow(unit, -1, modulus)
    correction = scale(prefix, inverse*inverse-1, modulus)
    translation = add(scale(x, prime**(length-1), modulus),
                      scale(correction, -1, modulus), modulus)
    diagonal = _levi(scale(eye(len(x)), unit, modulus),
                     scale(eye(len(x)), inverse, modulus))
    return multiply(_lower(translation), diagonal, modulus)


def final_digit_query(prefix, x, t, i, j, prime, length):
    """Final-digit fibers F0(X+t*B+t**2*C), using elementary Levi matrices."""
    modulus = _scope(prime, length)
    prefix = _symmetric(prefix, prime**(length-1))
    x = _symmetric(x, prime, len(prefix))
    _scalar(t, prime)
    e = elementary(len(x), i, j)
    a = add(eye(len(x)), scale(e, t, modulus), modulus)
    inverse = add(eye(len(x)), scale(e, -t, modulus), modulus)
    conjugated = multiply(multiply(transpose(inverse), prefix, modulus), inverse, modulus)
    correction = add(conjugated, scale(prefix, -1, modulus), modulus)
    translation = add(scale(x, prime**(length-1), modulus),
                      scale(correction, -1, modulus), modulus)
    return multiply(_lower(translation), _levi(a, transpose(inverse)), modulus)


def recover_scalar_digit(kernel_vector, n, prime):
    """Normalize a SUPPLIED nonzero vector from the exact one-dimensional kernel.

    Coordinates are (t, upper triangle of X), with X=2*t*S_digit. Shape
    checks do not prove that an unknown-source HSP learner returned its kernel.
    """
    _scope(prime, 2)
    if type(n) is not int or n < 2:
        raise ValueError("rank at least two required")
    values = tuple(kernel_vector)
    if len(values) != 1+n*(n+1)//2 or any(
        type(x) is not int or not 0 <= x < prime for x in values
    ) or values[0] == 0:
        raise ValueError("nonzero exact-kernel vector with nonzero t required")
    inverse = pow(2*values[0], -1, prime)
    result = [[0]*n for _ in range(n)]
    for (i, j), x in zip(combinations_with_replacement(range(n), 2), values[1:]):
        result[i][j] = result[j][i] = x*inverse % prime
    return tuple(map(tuple, result))


def scalar_verification_pair(prefix, candidate, digit, prime, length):
    candidate = _symmetric(candidate, prime, len(prefix))
    zero = scale(eye(len(prefix)), 0, prime)
    return (scalar_digit_query(prefix, zero, 1, digit, prime, length),
            socle_shift(scale(candidate, -2, prime), prime, length))


def final_verification_pairs(prefix, b, c, i, j, prime, length):
    n = len(prefix)
    b, c = _symmetric(b, prime, n), _symmetric(c, prime, n)
    zero = scale(eye(n), 0, prime)
    return tuple((final_digit_query(prefix, zero, t, i, j, prime, length),
                  socle_shift(add(scale(b, t, prime), scale(c, t*t, prime), prime),
                              prime, length)) for t in (1, prime-1))


def lift_symplectic_matrix(residue_lift, prime, length):
    """Public Hensel correction of a symplectic residue matrix to Z/p**length."""
    modulus = _scope(prime, length)
    a = tuple(tuple(row) for row in residue_lift)
    dimension = len(a)
    if dimension < 4 or dimension % 2 or any(len(row) != dimension for row in a):
        raise ValueError("even square matrix of dimension >=4 required")
    if any(type(x) is not int or not 0 <= x < modulus for row in a for x in row):
        raise ValueError("canonical matrix entries required")
    j = symplectic_form(dimension//2)
    gram = multiply(multiply(transpose(a), j, prime), a, prime)
    if gram != scale(j, 1, prime):
        raise ValueError("input is not symplectic modulo p")
    for digit in range(1, length):
        current_modulus = prime**(digit+1)
        gram = multiply(multiply(transpose(a), j, current_modulus), a, current_modulus)
        difference = add(gram, scale(j, -1, current_modulus), current_modulus)
        if any(x % prime**digit for row in difference for x in row):
            raise ArithmeticError("previous symplectic precision was lost")
        defect = tuple(tuple(x//prime**digit for x in row) for row in difference)
        correction = scale(multiply(j, defect, prime), pow(2, -1, prime), prime)
        a = multiply(a, add(eye(dimension), scale(correction, prime**digit, current_modulus),
                            current_modulus), current_modulus)
    if multiply(multiply(transpose(a), j, modulus), a, modulus) != scale(j, 1, modulus):
        raise ArithmeticError("symplectic lift failed")
    return a
