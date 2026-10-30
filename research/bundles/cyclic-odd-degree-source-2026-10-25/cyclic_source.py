"""Composite-modulus lift and kernel certificates; no geometric source backend."""

from math import gcd, prod
from pathlib import Path
import sys

from sympy import Matrix, eye, isprime, nextprime, zeros
from sympy.ntheory.modular import crt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernel-output-2026-10-23"))
from kernel_output import (
    _preimage_lattice, alternating_form, check_split, coordinate_map, flat,
    integer_matrix, inverse_mod, matrix_multiply, matrix_star, mod,
)
from uniform_source_bound import elementary


def checked_factors(n, factors):
    factors = tuple(factors)
    if type(n) is not int or n < 3 or n % 2 != 1 or not factors:
        raise ValueError("odd degree >= 3 and its prime-power factors required")
    if any(type(p) is not int or type(e) is not int or p < 3 or e < 1
           or not isprime(p) for p, e in factors):
        raise ValueError("distinct odd prime-power factors required")
    if len({p for p, _ in factors}) != len(factors) or prod(p**e for p, e in factors) != n:
        raise ValueError("factorization does not match degree")
    return tuple(sorted(factors))


def sl_ring_word(matrix, n, factors):
    """Bounded elementary word over Z/n, using CRT to obtain UNIT pivots."""
    factors = checked_factors(n, factors)
    matrix = integer_matrix(matrix)
    d = matrix.rows
    if d < 2 or matrix.cols != d or int(matrix.det()) % n != 1:
        raise ValueError("SL_d matrix required")
    work, operations = mod(matrix, n), []
    primes = [p for p, _ in factors]

    def left(i, j, c):
        nonlocal work
        c %= n
        if c:
            work = mod(elementary(d, i, j, c)*work, n)
            operations.append((i, j, c))

    for col in range(d):
        if gcd(int(work[col, col]), n) != 1:
            choices = {}
            for p in primes:
                choices[p] = None if int(work[col, col]) % p else next(
                    row for row in range(col+1, d) if int(work[row, col]) % p)
            for row in range(col+1, d):
                coefficient = int(crt(primes, [int(choices[p] == row) for p in primes])[0])
                left(col, row, coefficient)
        pivot_inverse = pow(int(work[col, col]), -1, n)
        for row in range(d):
            if row != col:
                left(row, col, -int(work[row, col])*pivot_inverse)
    word = [(i, j, -c) for i, j, c in operations]
    for i in range(d-1):
        a = int(work[i, i])
        word.extend([(i, d-1, a), (d-1, i, -pow(a, -1, n)), (i, d-1, a),
                     (i, d-1, -1), (d-1, i, 1), (i, d-1, -1)])
    word = tuple((i, j, c % n) for i, j, c in word if c % n)
    if len(word) > 3*d*(d-1)//2 + 6*(d-1):
        raise AssertionError("ring word exceeds derived bound")
    return word


def odd_ring_lift(order, split, matrix, n, factors):
    """Same Sp4 query modulo odd n, integral inverse, and odd trace."""
    matrix = integer_matrix(matrix)
    if matrix.shape != (4, 4):
        raise ValueError("surface-only four by four matrix required")
    j = alternating_form(2)
    if mod(matrix.T*j*matrix-j, n) != zeros(4):
        raise ValueError("symplectic matrix required")
    check_split(order, split, n)
    physical = sl_ring_word(matrix, n, factors)
    split_inverse = inverse_mod(coordinate_map(split), n)
    cross = []
    for i, j, c in physical:
        if i//2 != j//2:
            cross.append((i, j, c))
        else:
            k = next(k for k in range(4) if k//2 != i//2)
            cross.extend([(i, k, c), (k, j, 1), (i, k, -c), (k, j, -1)])
    quaternion_factors = []
    for i, j, c in cross:
        image = zeros(2)
        image[i % 2, j % 2] = c
        q = mod(pow(2, -1, n)*split_inverse*flat(image), n)
        q = q.applyfunc(lambda x: 2*(int(x)-n if 2*x > n else int(x)))
        quaternion_factors.append((i//2, j//2, q))
    quaternion_factors.append((0, 1, n*order.unit))
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    sigma, inverse = identity.copy(), identity.copy()
    for a, b, q in quaternion_factors:
        forward, backward = identity.copy(), identity.copy()
        forward[4*(2*a+b):4*(2*a+b)+4, :] += q
        backward[4*(2*a+b):4*(2*a+b)+4, :] -= q
        sigma = matrix_multiply(order, sigma, forward)
        inverse = matrix_multiply(order, backward, inverse)
    s = matrix_multiply(order, matrix_star(order, sigma), sigma)
    trace = (order.traces*(s[:4, :]+s[12:, :]))[0]/2
    if trace.q != 1 or trace < 3 or int(trace) % 2 != 1:
        raise ArithmeticError("odd trace invariant failed")
    return {"sigma": sigma, "inverse": inverse, "S": s, "trace": int(trace),
            "physical_length": len(physical), "quaternion_factors": tuple(quaternion_factors)}


def uniform_plan(order, n, factors, characteristic):
    checked_factors(n, factors)
    if (type(characteristic) is not int or characteristic <= 3
            or not isprime(characteristic) or gcd(characteristic, n) != 1):
        raise ValueError("prime characteristic > 3 coprime to degree required")
    norms = [(order.traces*order.multiply(order.star(eye(4)[:, i]), eye(4)[:, i]))[0]/2
             for i in range(4)]
    if any(x.q != 1 or x <= 0 for x in norms):
        raise ValueError("positive integral source basis norms required")
    u = 2+4*(n-1)**2*int(sum(norms))
    bound = u**144*(2+n*n)
    multiplier, r, primes = 1, 3, []
    while multiplier <= bound*bound:
        if gcd(r, n*characteristic) == 1:
            multiplier *= r
            primes.append(r)
        r = int(nextprime(r))
    mark_product, marks = 1, []
    threshold = 8*16**3*n*n
    while mark_product*mark_product <= threshold:
        if gcd(r, n*characteristic) == 1:
            mark_product *= r
            marks.append(r)
        r = int(nextprime(r))
    return {"physical_length_bound": 36, "quaternion_length_bound": 145,
            "trace_bound": bound, "multiplier": multiplier,
            "quotient_primes": primes, "marking_primes": marks,
            "marking_product": mark_product, "marking_threshold_squared": threshold,
            "weak_query_orders": primes+marks, "weak_query_exponent": 1,
            "stabilized_dimension": 16, "geometry_executed": False,
            "quantum_execution": False, "speedup_established": False}


def primitive_frame(vector, n, factors):
    """SL2 frame with the supplied primitive vector first, without points."""
    factors = checked_factors(n, factors)
    vector = mod(integer_matrix(vector), n)
    if vector.shape != (2, 1) or gcd(int(vector[0]), int(vector[1]), n) != 1:
        raise ValueError("primitive two-coordinate line required")
    moduli, xs, ys = [], [], []
    for p, e in factors:
        m = p**e
        x, y = (int(a) % m for a in vector)
        complement = (0, pow(x, -1, m)) if x % p else (-pow(y, -1, m), 0)
        moduli.append(m)
        xs.append(complement[0])
        ys.append(complement[1])
    w = Matrix([int(crt(moduli, xs)[0]), int(crt(moduli, ys)[0])])
    return mod(vector.row_join(w), n)


def certificate_queries(vector, n, factors):
    """Two Sp4 matrices fixing ONLY the candidate doubled primitive line."""
    c = primitive_frame(vector, n, factors)
    change = Matrix.diag(c, c)
    unipotent = eye(4)
    unipotent[0, 1] = 1
    mix = Matrix([[1, 0, 1, 0], [0, 1, 0, 0],
                  [0, 0, 1, 0], [0, -1, 0, 1]])
    inverse = inverse_mod(change, n)
    return tuple(mod(change*g*inverse, n) for g in (unipotent, mix))


def crt_query(local, local_modulus, n):
    """Embed a local matrix as identity on all other coprime components."""
    local = integer_matrix(local)
    if (type(n) is not int or type(local_modulus) is not int or local_modulus < 3
            or n < local_modulus or n % local_modulus
            or gcd(local_modulus, n//local_modulus) != 1
            or local.rows != local.cols):
        raise ValueError("full coprime primary component and square matrix required")
    other = n//local_modulus
    idempotent = 1 if other == 1 else other*pow(other, -1, local_modulus)
    return mod(eye(local.rows)+idempotent*(local-eye(local.rows)), n)


def affine_query(square_root, translation, modulus):
    """Public SL2 query acting as z -> square_root^2 z + translation."""
    if (type(modulus) is not int or modulus < 3 or modulus % 2 != 1
            or type(square_root) is not int or type(translation) is not int
            or gcd(square_root, modulus) != 1):
        raise ValueError("unit square root and integral translation required")
    inverse = pow(square_root, -1, modulus)
    return mod(Matrix([[square_root, translation*inverse], [0, inverse]]), modulus)


def combine_local_lines(n, factors, vectors):
    factors = checked_factors(n, factors)
    if len(vectors) != len(factors):
        raise ValueError("one line per sorted primary factor required")
    moduli, checked = [], []
    for (p, e), vector in zip(factors, vectors):
        primitive_frame(vector, p**e, ((p, e),))
        moduli.append(p**e)
        checked.append(integer_matrix(vector))
    return Matrix([int(crt(moduli, [v[i] for v in checked])[0]) for i in range(2)])


def cyclic_annihilator(order, split, vector, n, factors):
    """LEFT ideal of the supplied cyclic kernel, not a secret-kernel solver."""
    check_split(order, split, n)
    inverse = inverse_mod(primitive_frame(vector, n, factors), n)
    allowed = []
    for row in range(2):
        a = zeros(2)
        a[row, 1] = 1
        allowed.append(mod(a*inverse, n))
    return _preimage_lattice(coordinate_map(split), allowed, n)
