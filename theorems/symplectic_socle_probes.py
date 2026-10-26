"""Public arithmetic for the proposed prime-square Siegel HSP reduction.

This is NOT an HSP/HPGP solver. The caller supplies a verified odd prime;
the checks below do not certify primality. Matrices use Python integers,
including for p**2. No hidden object enters construction of a query matrix.
"""

from __future__ import annotations

from collections.abc import Sequence

Matrix = tuple[tuple[int, ...], ...]


def eye(n: int) -> Matrix:
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


def transpose(a: Matrix) -> Matrix:
    return tuple(zip(*a))


def add(a: Matrix, b: Matrix, modulus: int) -> Matrix:
    return tuple(tuple((x + y) % modulus for x, y in zip(ar, br))
                 for ar, br in zip(a, b))


def scale(a: Matrix, scalar: int, modulus: int) -> Matrix:
    return tuple(tuple(scalar * x % modulus for x in row) for row in a)


def multiply(a: Matrix, b: Matrix, modulus: int) -> Matrix:
    bt = transpose(b)
    return tuple(tuple(sum(x * y for x, y in zip(row, col)) % modulus
                       for col in bt) for row in a)


def symplectic_form(n: int) -> Matrix:
    return tuple(tuple(int(i < n and j == i + n)
                       - int(i >= n and j == i - n)
                       for j in range(2 * n)) for i in range(2 * n))


def _scope(n: int, prime: int) -> None:
    if n < 2 or prime < 3 or prime % 2 == 0:
        raise ValueError("Requires n >= 2 and a supplied verified odd prime")


def _symmetric(a: Sequence[Sequence[int]], n: int, prime: int) -> Matrix:
    if len(a) != n or any(len(row) != n for row in a):
        raise ValueError("Wrong symmetric-matrix shape")
    result = tuple(tuple(int(x) % prime for x in row) for row in a)
    if result != transpose(result):
        raise ValueError("Matrix must be symmetric modulo p")
    return result


def elementary(n: int, i: int, j: int) -> Matrix:
    if not 0 <= i < n or not 0 <= j < n or i == j:
        raise ValueError("Requires distinct valid elementary indices")
    return tuple(tuple(int(r == i and c == j) for c in range(n))
                 for r in range(n))


def lower_socle(x: Sequence[Sequence[int]], prime: int) -> Matrix:
    n = len(x)
    _scope(n, prime)
    x = _symmetric(x, n, prime)
    return tuple(tuple(int(r == c) + (prime * x[r - n][c]
                       if r >= n and c < n else 0)
                       for c in range(2 * n)) for r in range(2 * n))


def query_matrix(x: Sequence[Sequence[int]], t: int, i: int, j: int,
                 prime: int) -> Matrix:
    """L(pX) diag(I+tE_ij, I-tE_ji), an actual symplectic ring matrix."""
    n = len(x)
    _scope(n, prime)
    e = elementary(n, i, j)
    t %= prime
    modulus = prime * prime
    a = add(eye(n), scale(e, t, modulus), modulus)
    ait = add(eye(n), scale(transpose(e), -t, modulus), modulus)
    diagonal = tuple(tuple(a[r][c] if r < n and c < n else
                           ait[r - n][c - n] if r >= n and c >= n else 0
                           for c in range(2 * n)) for r in range(2 * n))
    return multiply(lower_socle(x, prime), diagonal, modulus)


def graph_polynomial(s: Sequence[Sequence[int]], i: int, j: int,
                     prime: int) -> tuple[Matrix, Matrix]:
    """Proof/reference coefficients B,C; s is not available to the learner."""
    n = len(s)
    _scope(n, prime)
    s = _symmetric(s, n, prime)
    e = elementary(n, i, j)
    et = transpose(e)
    b = scale(add(multiply(et, s, prime), multiply(s, e, prime), prime),
              -1, prime)
    c = multiply(multiply(et, s, prime), e, prime)
    return b, c


def coefficient_verification_pairs(b: Matrix, c: Matrix, i: int, j: int,
                                   prime: int) -> tuple[tuple[Matrix, Matrix], ...]:
    """Four actual oracle queries certify a supplied quadratic, with P(0)=0.

    Each pair must have equal hiding labels. Testing only t=1 is insufficient.
    This uses the promised injectivity on lower socle matrices, not on G.
    """
    n = len(b)
    _scope(n, prime)
    b, c = _symmetric(b, n, prime), _symmetric(c, n, prime)
    zero = scale(eye(n), 0, prime)
    return tuple((query_matrix(zero, t, i, j, prime),
                  lower_socle(add(scale(b, t, prime), scale(c, t * t, prime),
                                  prime), prime)) for t in (1, prime - 1))


def recover_symmetric_matrix(linear_coefficients: Sequence[Matrix],
                             prime: int) -> Matrix:
    """Postprocess n CORRECT HPGP answers, using j=(i+1) mod n.

    Consistency checks are not a substitute for the HPGP success guarantee:
    another consistent set of coefficients can describe a different S.
    """
    n = len(linear_coefficients)
    _scope(n, prime)
    coefficients = [_symmetric(b, n, prime) for b in linear_coefficients]
    result = [[0] * n for _ in range(n)]
    inverse_two = pow(2, -1, prime)
    for i, b in enumerate(coefficients):
        j = (i + 1) % n
        for k in range(n):
            result[k][i] = -b[k][j] * (inverse_two if k == j else 1) % prime
    s = _symmetric(result, n, prime)
    for i, b in enumerate(coefficients):
        if graph_polynomial(s, i, (i + 1) % n, prime)[0] != b:
            raise ValueError("Inconsistent hidden-polynomial coefficients")
    return s


def lift_symplectic_matrix(residue_lift: Sequence[Sequence[int]],
                           prime: int) -> Matrix:
    """Correct a matrix symplectic mod p to one symplectic mod p**2."""
    dimension = len(residue_lift)
    if dimension % 2 or any(len(row) != dimension for row in residue_lift):
        raise ValueError("Requires an even square matrix")
    n = dimension // 2
    _scope(n, prime)
    modulus = prime * prime
    a = tuple(tuple(int(x) % modulus for x in row) for row in residue_lift)
    j = symplectic_form(n)
    gram = multiply(multiply(transpose(a), j, modulus), a, modulus)
    difference = add(gram, scale(j, -1, modulus), modulus)
    if any(x % prime for row in difference for x in row):
        raise ValueError("Input is not symplectic modulo p")
    defect = tuple(tuple(x // prime for x in row) for row in difference)
    correction = scale(multiply(j, defect, prime), pow(2, -1, prime), prime)
    lifted = multiply(a, add(eye(dimension), scale(correction, prime, modulus),
                             modulus), modulus)
    if multiply(multiply(transpose(lifted), j, modulus), lifted, modulus) != scale(j, 1, modulus):
        raise ArithmeticError("Symplectic correction failed")
    return lifted
