"""Double-level integral source arithmetic, not a geometric label backend."""

from itertools import combinations, product
from math import gcd, prod
from pathlib import Path
import sys

from sympy import Matrix, eye, isprime, nextprime, zeros
from sympy.ntheory.modular import crt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernel-output-2026-10-23"))
from kernel_output import (
    alternating_form, check_split, coordinate_map, flat, integer_matrix,
    inverse_mod, matrix_multiply, matrix_star, mod,
)
from uniform_source_bound import elementary


def checked_factors(n, factors):
    factors = tuple(factors)
    if type(n) is not int or n < 2 or not factors:
        raise ValueError("degree >= 2 and prime-power factors required")
    if any(type(p) is not int or type(e) is not int or p < 2 or e < 1
           or not isprime(p) for p, e in factors):
        raise ValueError("prime-power factors required")
    if len({p for p, _ in factors}) != len(factors) or prod(p**e for p, e in factors) != n:
        raise ValueError("factorization does not match degree")
    return tuple(sorted(factors))


def _module_action(order, module, modulus):
    rows = next((rows for rows in combinations(range(4), 2)
                 if int(module[list(rows), :].det()) % 2), None)
    if rows is None:
        raise ValueError("rank-two direct summand required at 2")
    inverse = inverse_mod(module[list(rows), :], modulus)
    actions = []
    for i in range(4):
        image = Matrix.hstack(*(order.multiply(eye(4)[:, i], module[:, j]) for j in range(2)))
        coefficients = mod(inverse*image[list(rows), :], modulus)
        if mod(module*coefficients-image, modulus) != zeros(4, 2):
            raise ValueError("left ideal is not stable under the proposed order action")
        actions.append(coefficients)
    result = tuple(actions)
    check_split(order, result, modulus)
    return result


def split_at_two(order):
    """Constant-size search in O/2O, followed by a left-ideal action."""
    for bits in product((0, 1), repeat=4):
        e = Matrix(bits)
        if e in (zeros(4, 1), mod(order.unit, 2)):
            continue
        if mod(order.multiply(e, e)-e, 2) != zeros(4, 1):
            continue
        vectors = [mod(order.multiply(eye(4)[:, i], e), 2) for i in range(4)]
        for i, j in combinations(range(4), 2):
            try:
                return _module_action(order, Matrix.hstack(vectors[i], vectors[j]), 2)
            except ValueError:
                continue
    raise ValueError("order does not have the required full split reduction at 2")


def lift_dyadic_split(order, actions, modulus):
    """Preserve a SPECIFIED O/2^e split while extending it to O/2^(e+1)."""
    if type(modulus) is not int or modulus < 2 or modulus & (modulus-1):
        raise ValueError("positive dyadic modulus >= 2 required")
    check_split(order, actions, modulus)
    inverse = inverse_mod(coordinate_map(actions), modulus)
    e0 = mod(inverse*Matrix([1, 0, 0, 0]), modulus)
    square = order.multiply(e0, e0)
    e = mod(3*square-2*order.multiply(square, e0), 2*modulus)
    if mod(order.multiply(e, e)-e, 2*modulus) != zeros(4, 1):
        raise ValueError("idempotent lift failed")
    e21 = mod(inverse*Matrix([0, 0, 1, 0]), modulus)
    module = Matrix.hstack(e, mod(order.multiply(e21, e), 2*modulus))
    result = _module_action(order, module, 2*modulus)
    if any(mod(a-b, modulus) != zeros(2) for a, b in zip(result, actions)):
        raise ValueError("dyadic lift changed the supplied coordinates")
    return result


def extend_split_to_double(order, actions, n):
    """Compute O/2n action from O/n action, without torsion-point advice."""
    if type(n) is not int or n < 2:
        raise ValueError("integer degree >= 2 required")
    check_split(order, actions, n)
    dyadic, odd = 1, n
    while odd % 2 == 0:
        dyadic *= 2
        odd //= 2
    if dyadic == 1:
        two_actions = split_at_two(order)
    else:
        two_actions = lift_dyadic_split(order, tuple(mod(a, dyadic) for a in actions), dyadic)
    if odd == 1:
        result = two_actions
    else:
        result = tuple(Matrix(2, 2, [
            int(crt((2*dyadic, odd), (a[k], b[k]))[0]) for k in range(4)
        ]) for a, b in zip(two_actions, actions))
    check_split(order, result, 2*n)
    if any(mod(a-b, n) != zeros(2) for a, b in zip(result, actions)):
        raise ValueError("double-level split changed the supplied mod-n coordinates")
    return result


def symplectic_double_lift(matrix, n):
    matrix, form = integer_matrix(matrix), alternating_form(2)
    if type(n) is not int or n < 2 or matrix.shape != (4, 4):
        raise ValueError("degree >= 2 and a surface matrix required")
    matrix = mod(matrix, n)
    if mod(matrix.T*form*matrix-form, n) != zeros(4):
        raise ValueError("symplectic matrix required")
    if n % 2:
        lifted = mod(matrix+n*mod(eye(4)-matrix, 2), 2*n)
    else:
        error = mod((matrix.T*form*matrix-form)/n, 2)
        y = zeros(4)
        for i in range(4):
            for j in range(i+1, 4):
                y[i, j] = error[i, j]
        correction = mod(inverse_mod(matrix.T*form, 2)*y, 2)
        lifted = mod(matrix+n*correction, 2*n)
    if mod(lifted.T*form*lifted-form, 2*n) != zeros(4):
        raise ArithmeticError("symplectic double lift failed")
    return lifted


def sl_word(matrix, n, factors):
    """The earlier CRT unit-pivot compiler, now also permitting the prime 2."""
    factors = checked_factors(n, factors)
    matrix = integer_matrix(matrix)
    d = matrix.rows
    if d < 2 or matrix.cols != d or int(matrix.det()) % n != 1:
        raise ValueError("SL matrix required")
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
            choices = {p: None if int(work[col, col]) % p else next(
                row for row in range(col+1, d) if int(work[row, col]) % p) for p in primes}
            for row in range(col+1, d):
                left(col, row, int(crt(primes, [int(choices[p] == row) for p in primes])[0]))
        inverse = pow(int(work[col, col]), -1, n)
        for row in range(d):
            if row != col:
                left(row, col, -int(work[row, col])*inverse)
    word = [(i, j, -c) for i, j, c in operations]
    for i in range(d-1):
        a = int(work[i, i])
        if a == 1:
            continue
        word.extend([(i, d-1, a), (d-1, i, -pow(a, -1, n)), (i, d-1, a),
                     (i, d-1, -1), (d-1, i, 1), (i, d-1, -1)])
    word = tuple((i, j, c % n) for i, j, c in word if c % n)
    if len(word) > 3*d*(d-1)//2+6*(d-1):
        raise AssertionError("elementary word exceeds derived bound")
    return word


def congruence_lift(order, actions, matrix, n, factors):
    factors = dict(checked_factors(n, factors))
    factors[2] = factors.get(2, 0)+1
    doubled_actions = extend_split_to_double(order, actions, n)
    lifted_query = symplectic_double_lift(matrix, n)
    word = sl_word(lifted_query, 2*n, tuple(factors.items()))
    inverse_actions = inverse_mod(coordinate_map(doubled_actions), 2*n)
    cross = []
    for i, j, c in word:
        if i//2 != j//2:
            cross.append((i, j, c))
        else:
            k = next(k for k in range(4) if k//2 != i//2)
            cross.extend([(i, k, c), (k, j, 1), (i, k, -c), (k, j, -1)])
    factors = []
    for i, j, c in cross:
        image = zeros(2)
        image[i % 2, j % 2] = c
        coefficient = mod(inverse_actions*flat(image), 2*n)
        coefficient = coefficient.applyfunc(lambda x: int(x)-2*n if x > n else int(x))
        factors.append((i//2, j//2, coefficient))
    identity = Matrix.vstack(order.unit, zeros(4, 1), zeros(4, 1), order.unit)
    sigma, inverse = identity.copy(), identity.copy()
    for i, j, coefficient in factors:
        forward, backward = identity.copy(), identity.copy()
        forward[4*(2*i+j):4*(2*i+j)+4, :] += coefficient
        backward[4*(2*i+j):4*(2*i+j)+4, :] -= coefficient
        sigma = matrix_multiply(order, sigma, forward)
        inverse = matrix_multiply(order, backward, inverse)
    s = matrix_multiply(order, matrix_star(order, sigma), sigma)
    t = (order.traces*(s[:4, :]+s[12:, :]))[0]/2
    if mod(s-identity, 2*n) != zeros(16, 1) or t.q != 1 or t < 2 or int(t) % 4 != 2:
        raise ArithmeticError("double-level Gram congruence/trace failed")
    return {"sigma": sigma, "inverse": inverse, "S": s, "trace": int(t),
            "physical_length": len(word), "quaternion_factors": tuple(factors),
            "doubled_split": doubled_actions, "doubled_query": lifted_query}


def resource_plan(order, n, factors, characteristic):
    checked_factors(n, factors)
    if (type(characteristic) is not int or characteristic <= 3 or not isprime(characteristic)
            or gcd(characteristic, n) != 1):
        raise ValueError("prime characteristic > 3 coprime to degree required")
    norms = [(order.traces*order.multiply(order.star(eye(4)[:, i]), eye(4)[:, i]))[0]/2
             for i in range(4)]
    if any(x.q != 1 or x <= 0 for x in norms):
        raise ValueError("positive integral source norms required")
    bound = (2+4*n*n*int(sum(norms)))**144
    d, r, primes = 1, 3, []
    while d <= bound*bound:
        if gcd(r, n*characteristic) == 1:
            d *= r
            primes.append(r)
        r = int(nextprime(r))
    mark, marks, threshold = 1, [], 8*16**3*n*n
    while mark*mark <= threshold:
        if gcd(r, n*characteristic) == 1:
            mark *= r
            marks.append(r)
        r = int(nextprime(r))
    return {"trace_bound": bound, "multiplier": d, "quotient_primes": primes,
            "marking_primes": marks, "marking_product": mark,
            "marking_threshold_squared": threshold, "weak_query_exponent": 1,
            "physical_length_bound": 36, "quaternion_length_bound": 144,
            "stabilized_dimension": 16, "geometric_execution": False}
